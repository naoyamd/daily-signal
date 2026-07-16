#!/usr/bin/env python3
"""Prepare source candidates and publish an editorial Daily Signal brief."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from scripts.editorial import Item, load_seen, render_markdown


SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = {1, 2}
HANDOFF_SCHEMA = "daily-signal-candidates/v1"
FEEDBACK_SCHEMA = "daily-signal-feedback/v1"
MODEL = "openai/gpt-5.6-luna"
GENERATOR = "OpenClaw Editorial System"
SUNDAY_EDITORIAL_NOTE = (
    "日曜日版は過去7日間を振り返る週次レビューです。月曜日に航空宇宙系研究所の管理職へ"
    "共有できるよう、重要テーマ、継続トレンド、次週の確認事項を示してください。"
    "特にAIによる設計、民間・軍用航空機、航空機エンジン、CAD/CAEの経営・研究開発上の含意を重視します。"
)
IDENTITY_PATTERN = re.compile(r"Emma|エマ", re.IGNORECASE)
SELF_REFERENCE_PATTERN = re.compile(r"(?:私|わたし|筆者|執筆者)(?:は|が|の|として)")


def _is_public_https_url(value: str) -> bool:
    """Validate a boundary URL without issuing a DNS request."""

    try:
        parsed = urlsplit(value)
        hostname = (parsed.hostname or "").rstrip(".").lower()
        _ = parsed.port
    except ValueError:
        return False
    if parsed.scheme != "https" or not hostname or parsed.username or parsed.password:
        return False
    if hostname == "localhost" or hostname.endswith((".localhost", ".local", ".internal")):
        return False
    try:
        address = ipaddress.ip_address(hostname.strip("[]"))
    except ValueError:
        return "." in hostname
    return address.is_global


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_bundle(
    handoff_path: Path,
    state_path: Path,
    output_path: Path,
    now: datetime | None = None,
    expected_edition: str | None = None,
) -> dict[str, Any]:
    """Validate and import the collector's immutable candidate handoff."""

    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    if not isinstance(handoff, dict) or handoff.get("schema") != HANDOFF_SCHEMA:
        raise ValueError("unsupported collector handoff schema")
    batch_id = str(handoff.get("batch_id") or "")
    if not re.fullmatch(r"[a-zA-Z0-9._-]{8,128}", batch_id):
        raise ValueError("collector handoff batch_id is invalid")
    edition = str(handoff.get("edition") or "")
    if edition not in {"digest", "deep-dive", "market"}:
        raise ValueError("collector handoff edition is invalid")
    if expected_edition is not None and edition != expected_edition:
        raise ValueError("collector handoff edition mismatch")
    if not isinstance(handoff.get("items"), list):
        raise ValueError("collector handoff items must be a list")
    generated_at = datetime.fromisoformat(str(handoff.get("generated_at", "")))
    if generated_at.tzinfo is None:
        raise ValueError("collector handoff generated_at must include a timezone")
    expires_at = datetime.fromisoformat(str(handoff.get("expires_at", "")))
    if expires_at.tzinfo is None:
        raise ValueError("collector handoff expires_at must include a timezone")
    reference_now = now or datetime.now(generated_at.tzinfo)
    if reference_now.astimezone(expires_at.tzinfo) > expires_at:
        raise ValueError("collector handoff has expired")
    seen = load_seen(state_path)
    selected: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, value in enumerate(handoff["items"]):
        if not isinstance(value, dict):
            raise ValueError(f"collector handoff items[{index}] must be an object")
        item = Item(**value)
        if not _is_public_https_url(item.url):
            raise ValueError(f"collector handoff items[{index}] URL must be public HTTPS")
        if item.id in ids:
            raise ValueError(f"duplicate collector item id: {item.id}")
        ids.add(item.id)
        if item.id not in seen:
            selected.append(value)
    timezone_name = str(handoff.get("timezone") or "Asia/Tokyo")
    local_generated_at = generated_at.astimezone(ZoneInfo(timezone_name))
    editorial_note = SUNDAY_EDITORIAL_NOTE if local_generated_at.weekday() == 6 else ""
    bundle = {
        "schema_version": SCHEMA_VERSION,
        "source_schema": HANDOFF_SCHEMA,
        "batch_id": batch_id,
        "edition": edition,
        "generated_at": generated_at.isoformat(),
        "timezone": timezone_name,
        "max_items": int(handoff.get("max_items", 8)),
        "editorial_note": editorial_note,
        "items": selected,
        "collection": dict(handoff.get("collection_counts") or {}),
    }
    write_json(output_path, bundle)
    return bundle


def _text(value: Any, field: str, *, one_line: bool = False, max_chars: int = 2000) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    cleaned = value.strip()
    if one_line:
        cleaned = re.sub(r"\s+", " ", cleaned)
    if not cleaned:
        raise ValueError(f"{field} must not be empty")
    if len(cleaned) > max_chars:
        raise ValueError(f"{field} exceeds {max_chars} characters")
    return cleaned


def validate_editorial_voice(value: Any, field: str = "draft") -> None:
    """Reject public copy that exposes the internal writer or a first-person persona."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"id", "source_ids", "citations", "references", "source_url"}:
                continue
            validate_editorial_voice(item, f"{field}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            validate_editorial_voice(item, f"{field}[{index}]")
    elif isinstance(value, str) and (
        IDENTITY_PATTERN.search(value) or SELF_REFERENCE_PATTERN.search(value)
    ):
        raise ValueError(f"{field} must use an anonymous, non-first-person editorial voice")


def validate_candidate_feedback(
    bundle: dict[str, Any], draft: dict[str, Any], *, required: bool | None = None,
) -> list[dict[str, Any]]:
    expected_ids = [item["id"] for item in bundle.get("items", [])]
    values = draft.get("candidate_feedback")
    required = bundle.get("schema_version") == SCHEMA_VERSION if required is None else required
    if values is None and not required:
        return []
    if not isinstance(values, list):
        raise ValueError("draft.candidate_feedback must be a list")
    returned_ids = [item.get("id") for item in values if isinstance(item, dict)]
    if returned_ids != expected_ids:
        raise ValueError("candidate_feedback must cover every candidate ID in the original order")
    normalized: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ValueError(f"candidate_feedback[{index}] must be an object")
        row: dict[str, Any] = {"id": expected_ids[index]}
        for field in ("relevance", "quality", "novelty"):
            raw = value.get(field)
            if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
                raise ValueError(f"candidate_feedback[{index}].{field} must be between 0 and 1")
            row[field] = round(float(raw), 4)
        row["reason"] = _text(
            value.get("reason"), f"candidate_feedback[{index}].reason", one_line=True, max_chars=500,
        )
        normalized.append(row)
    return normalized


def validate_draft(bundle: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    schema_version = bundle.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported candidate bundle schema")
    source_items = bundle.get("items")
    draft_items = draft.get("items")
    if not isinstance(source_items, list) or not source_items:
        raise ValueError("candidate bundle has no items")
    if not isinstance(draft_items, list):
        raise ValueError("draft.items must be a list")
    expected_ids = [item["id"] for item in source_items]
    returned_ids = [item.get("id") for item in draft_items if isinstance(item, dict)]
    if schema_version == 1:
        if returned_ids != expected_ids:
            raise ValueError("draft must preserve every candidate ID in the original order")
    else:
        if not returned_ids:
            raise ValueError("draft.items must select at least one candidate")
        if len(returned_ids) > int(bundle.get("max_items", 8)):
            raise ValueError("draft.items exceeds bundle.max_items")
        if any(item_id not in expected_ids for item_id in returned_ids):
            raise ValueError("draft.items contains an unknown candidate ID")
        expected_subset = [item_id for item_id in expected_ids if item_id in set(returned_ids)]
        if returned_ids != expected_subset or len(returned_ids) != len(set(returned_ids)):
            raise ValueError("draft must preserve selected candidate IDs in the original order")

    normalized_items: list[dict[str, Any]] = []
    for index, item in enumerate(draft_items):
        if not isinstance(item, dict):
            raise ValueError(f"draft.items[{index}] must be an object")
        citations = item.get("citations", [])
        if not isinstance(citations, list) or len(citations) > 3:
            raise ValueError(f"draft.items[{index}].citations must contain at most three URLs")
        normalized_citations = []
        for citation in citations:
            citation = _text(citation, f"draft.items[{index}].citations", one_line=True, max_chars=1000)
            if not citation.startswith("https://"):
                raise ValueError(f"draft.items[{index}] contains a non-HTTPS citation")
            normalized_citations.append(citation)
        normalized_items.append({
            "id": returned_ids[index],
            "headline": _text(item.get("headline"), f"draft.items[{index}].headline", one_line=True, max_chars=180),
            "summary": _text(item.get("summary"), f"draft.items[{index}].summary", max_chars=1200),
            "why_it_matters": _text(
                item.get("why_it_matters"),
                f"draft.items[{index}].why_it_matters",
                max_chars=700,
            ),
            "citations": normalized_citations,
        })
    normalized = {
        "title": _text(draft.get("title"), "draft.title", one_line=True, max_chars=160),
        "description": _text(draft.get("description"), "draft.description", one_line=True, max_chars=240),
        "overview": _text(draft.get("overview"), "draft.overview", max_chars=1600),
        "items": normalized_items,
        "candidate_feedback": validate_candidate_feedback(bundle, draft),
        "cost_usd": 0,
    }
    validate_editorial_voice(normalized)
    return normalized


def write_collection_feedback(
    bundle: dict[str, Any],
    draft: dict[str, Any],
    article: Path,
    feedback_outbox: Path | None,
) -> None:
    """Write a versioned event; the collector owns all learning/Vault writes."""

    assessments = draft.get("candidate_feedback")
    if feedback_outbox is None or not isinstance(assessments, list) or not assessments:
        return
    selected_ids = [
        str(item["id"])
        for item in draft.get("items", [])
        if isinstance(item, dict) and item.get("id")
    ]
    if not selected_ids:
        selected_ids = [str(value) for value in draft.get("source_ids", [])]
    candidate_signals: dict[str, dict[str, Any]] = {}
    for item in bundle.get("items", []):
        if not isinstance(item, dict) or not item.get("id"):
            continue
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        supplied = item.get("candidate_signals") if isinstance(item.get("candidate_signals"), dict) else {}
        candidate_signals[str(item["id"])] = {
            "source": str(supplied.get("source") or item.get("source") or ""),
            "source_kind": str(supplied.get("source_kind") or item.get("source_kind") or ""),
            "matched_keywords": [
                str(value)
                for value in supplied.get("keywords", item.get("matched_keywords", item.get("tags", [])))
            ],
            "queries": [str(value) for value in supplied.get("queries", [])]
            or ([str(item.get("query") or metadata.get("query"))] if item.get("query") or metadata.get("query") else []),
            "domain_groups": [
                str(value) for value in supplied.get("domain_groups", metadata.get("domain_groups", []))
            ],
        }
    event_key = f"{bundle.get('batch_id')}:{article.as_posix()}"
    event_id = f"editorial:{hashlib.sha256(event_key.encode('utf-8')).hexdigest()[:24]}"
    event = {
        "schema": FEEDBACK_SCHEMA,
        "type": "editorial",
        "event_id": event_id,
        "batch_id": str(bundle.get("batch_id") or ""),
        "article_id": article.as_posix(),
        "selected_ids": selected_ids,
        "candidate_feedback": assessments,
        "candidate_signals": candidate_signals,
    }
    feedback_outbox.mkdir(parents=True, exist_ok=True)
    target = feedback_outbox / f"{event_id.replace(':', '-')}.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)


def publish_draft(
    bundle_path: Path,
    draft_path: Path,
    content_dir: Path,
    state_path: Path,
    result_path: Path | None = None,
    feedback_outbox: Path | None = None,
) -> Path:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    digest = validate_draft(bundle, draft)
    source_by_id = {item["id"]: item for item in bundle["items"]}
    selected = [Item(**source_by_id[item["id"]]) for item in digest["items"]]
    local_now = datetime.fromisoformat(bundle["generated_at"])
    if local_now.tzinfo is None:
        local_now = local_now.replace(tzinfo=ZoneInfo(bundle.get("timezone", "Asia/Tokyo")))
    output = content_dir / f"{local_now:%Y-%m-%d}-daily-signal.md"
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing article: {output}")
    markdown = render_markdown(digest, selected, local_now, MODEL, generator=GENERATOR)
    # The article and seen-state are not mutated unless the feedback event is
    # durably queued for the collector. This keeps publication and learning
    # outcomes consistent across the repository boundary.
    write_collection_feedback(bundle, draft, output, feedback_outbox)
    content_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    seen = load_seen(state_path) | set(source_by_id)
    write_json(state_path, {"ids": sorted(seen)})
    if result_path:
        write_json(result_path, {
            "status": "published",
            "article": str(output),
            "title": digest["title"],
            "source_count": len(selected),
            "candidate_count": len(source_by_id),
            "generated_by": GENERATOR,
            "model": MODEL,
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--handoff", type=Path, required=True)
    prepare.add_argument("--state", type=Path, default=Path("data/seen.json"))
    prepare.add_argument("--output", type=Path, default=Path(".daily-signal/candidates.json"))

    publish = subparsers.add_parser("publish")
    publish.add_argument("--bundle", type=Path, default=Path(".daily-signal/candidates.json"))
    publish.add_argument("--draft", type=Path, default=Path(".daily-signal/draft.json"))
    publish.add_argument("--content-dir", type=Path, default=Path("content/daily"))
    publish.add_argument("--state", type=Path, default=Path("data/seen.json"))
    publish.add_argument("--result", type=Path, default=Path(".daily-signal/publish-result.json"))
    publish.add_argument("--feedback-outbox", type=Path)

    args = parser.parse_args()
    if args.command == "prepare":
        bundle = prepare_bundle(
            args.handoff,
            args.state,
            args.output,
            expected_edition="digest",
        )
        print(args.output)
        return 0 if bundle["items"] else 3
    output = publish_draft(
        args.bundle,
        args.draft,
        args.content_dir,
        args.state,
        args.result,
        feedback_outbox=args.feedback_outbox,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
