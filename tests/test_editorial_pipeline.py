import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.editorial import Item, render_markdown
from scripts.emma_pipeline import (
    FEEDBACK_SCHEMA,
    GENERATOR,
    HANDOFF_SCHEMA,
    MODEL,
    prepare_bundle,
    publish_draft,
    validate_draft,
)


NOW = datetime(2026, 7, 16, 3, tzinfo=timezone.utc)


def item(item_id: str = "source-1") -> dict:
    return Item(
        item_id,
        "Aircraft engine design update",
        f"https://example.com/{item_id}",
        "Engine maker",
        "航空機エンジン",
        NOW.isoformat(),
        "Verified public metadata.",
        2.0,
        source_kind="technical_report",
        query="aircraft engine generative design",
        tags=["aircraft engine", "generative design"],
        metadata={"domain_groups": ["aircraft_engines"]},
    ).__dict__


def handoff(items: list[dict] | None = None, edition: str = "digest") -> dict:
    return {
        "schema": HANDOFF_SCHEMA,
        "batch_id": "20260716T030000Z-digest-abc123",
        "edition": edition,
        "generated_at": NOW.isoformat(),
        "expires_at": "2026-07-17T03:00:00+00:00",
        "timezone": "Asia/Tokyo",
        "max_items": 1,
        "editorial_note": "Official sources first.",
        "items": items or [item()],
        "collection": {"collected_count": 20, "candidate_count": 1},
    }


def draft() -> dict:
    return {
        "title": "Editorial brief",
        "description": "Description",
        "overview": "Overview",
        "items": [{
            "id": "source-1",
            "headline": "Headline",
            "summary": "Summary",
            "why_it_matters": "Reason",
            "citations": ["https://example.com/check"],
        }],
        "candidate_feedback": [{
            "id": "source-1",
            "relevance": 0.9,
            "quality": 0.8,
            "novelty": 0.7,
            "reason": "Strong engineering relevance",
        }],
    }


class EditorialPipelineTests(unittest.TestCase):
    def test_prepare_imports_versioned_handoff_and_filters_seen(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "handoff.json"
            output = root / "candidates.json"
            state = root / "seen.json"
            source.write_text(json.dumps(handoff([item("old"), item("new")])), encoding="utf-8")
            state.write_text(json.dumps({"ids": ["old"]}), encoding="utf-8")
            bundle = prepare_bundle(source, state, output, now=NOW)
        self.assertEqual(bundle["source_schema"], HANDOFF_SCHEMA)
        self.assertEqual([value["id"] for value in bundle["items"]], ["new"])
        self.assertEqual(bundle["batch_id"], "20260716T030000Z-digest-abc123")

    def test_prepare_rejects_wrong_or_expired_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "handoff.json"
            source.write_text(json.dumps({**handoff(), "schema": "other/v1"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "schema"):
                prepare_bundle(source, root / "seen.json", root / "out.json", now=NOW)
            source.write_text(json.dumps({**handoff(), "expires_at": "2026-07-15T00:00:00+00:00"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expired"):
                prepare_bundle(source, root / "seen.json", root / "out.json", now=NOW)
            source.write_text(json.dumps(handoff(edition="market")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "edition mismatch"):
                prepare_bundle(
                    source,
                    root / "seen.json",
                    root / "out.json",
                    now=NOW,
                    expected_edition="digest",
                )

    def test_prepare_rejects_private_or_local_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "handoff.json"
            for url in ("https://127.0.0.1/private", "https://service.internal/private"):
                value = item("private")
                value["url"] = url
                source.write_text(json.dumps(handoff([value])), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "public HTTPS"):
                    prepare_bundle(source, root / "seen.json", root / "out.json", now=NOW)

    def test_validate_requires_feedback_for_every_candidate(self):
        bundle = {"schema_version": 2, "max_items": 1, "items": [item()]}
        value = validate_draft(bundle, draft())
        self.assertEqual(value["items"][0]["id"], "source-1")
        invalid = draft()
        invalid["candidate_feedback"] = []
        with self.assertRaisesRegex(ValueError, "every candidate ID"):
            validate_draft(bundle, invalid)

    def test_publish_writes_article_and_feedback_event_only(self):
        bundle = {
            "schema_version": 2,
            "batch_id": "20260716T030000Z-digest-abc123",
            "generated_at": NOW.isoformat(),
            "timezone": "UTC",
            "max_items": 1,
            "items": [item()],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path = root / "bundle.json"
            draft_path = root / "draft.json"
            bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
            draft_path.write_text(json.dumps(draft()), encoding="utf-8")
            output = publish_draft(
                bundle_path,
                draft_path,
                root / "content",
                root / "seen.json",
                root / "result.json",
                root / "feedback",
            )
            events = list((root / "feedback").glob("*.json"))
            event = json.loads(events[0].read_text(encoding="utf-8"))
        self.assertEqual(output.name, "2026-07-16-daily-signal.md")
        self.assertEqual(len(events), 1)
        self.assertEqual(event["schema"], FEEDBACK_SCHEMA)
        self.assertEqual(event["selected_ids"], ["source-1"])
        self.assertEqual(event["candidate_signals"]["source-1"]["domain_groups"], ["aircraft_engines"])
        self.assertEqual(event["candidate_signals"]["source-1"]["source_kind"], "technical_report")

    def test_feedback_queue_failure_does_not_mutate_article_or_seen_state(self):
        bundle = {
            "schema_version": 2,
            "batch_id": "20260716T030000Z-digest-abc123",
            "generated_at": NOW.isoformat(),
            "timezone": "UTC",
            "max_items": 1,
            "items": [item()],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path = root / "bundle.json"
            draft_path = root / "draft.json"
            blocked_outbox = root / "not-a-directory"
            bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
            draft_path.write_text(json.dumps(draft()), encoding="utf-8")
            blocked_outbox.write_text("blocked", encoding="utf-8")
            with self.assertRaises(OSError):
                publish_draft(
                    bundle_path,
                    draft_path,
                    root / "content",
                    root / "seen.json",
                    root / "result.json",
                    blocked_outbox,
                )
            self.assertFalse((root / "content").exists())
            self.assertFalse((root / "seen.json").exists())

    def test_render_uses_anonymous_editorial_attribution(self):
        source = Item(**item())
        value = validate_draft({"schema_version": 2, "max_items": 1, "items": [item()]}, draft())
        output = render_markdown(value, [source], NOW, MODEL, generator=GENERATOR)
        self.assertIn('generated_by: "OpenClaw Editorial System"', output)
        self.assertNotIn("Emma", output)
        self.assertNotIn("エマ", output)


if __name__ == "__main__":
    unittest.main()
