#!/usr/bin/env python3
"""Prepare source candidates and publish an editorial Daily Signal brief."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from scripts.daily_signal import Item, collect, load_seen, rank, render_markdown


SCHEMA_VERSION = 1
MODEL = "openai/gpt-5.6-luna"
GENERATOR = "OpenClaw Editorial System"
IDENTITY_PATTERN = re.compile(r"Emma|エマ", re.IGNORECASE)
SELF_REFERENCE_PATTERN = re.compile(r"(?:私|わたし|筆者|執筆者)(?:は|が|の|として)")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_bundle(
    config_path: Path,
    state_path: Path,
    output_path: Path,
    now: datetime | None = None,
) -> dict[str, Any]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    now = now or datetime.now(timezone.utc)
    selected = rank(collect(config, now), config, load_seen(state_path), now)
    selected = selected[: int(config["site"].get("max_items", 8))]
    timezone_name = config.get("site", {}).get("timezone", "Asia/Tokyo")
    local_now = now.astimezone(ZoneInfo(timezone_name))
    editorial_note = ""
    if local_now.weekday() == 6:
        editorial_note = config.get("sunday_editorial", {}).get("prompt", "")
    bundle = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": local_now.isoformat(),
        "timezone": timezone_name,
        "editorial_note": editorial_note,
        "items": [asdict(item) for item in selected],
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


def validate_draft(bundle: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    if bundle.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported candidate bundle schema")
    source_items = bundle.get("items")
    draft_items = draft.get("items")
    if not isinstance(source_items, list) or not source_items:
        raise ValueError("candidate bundle has no items")
    if not isinstance(draft_items, list):
        raise ValueError("draft.items must be a list")
    expected_ids = [item["id"] for item in source_items]
    returned_ids = [item.get("id") for item in draft_items if isinstance(item, dict)]
    if returned_ids != expected_ids:
        raise ValueError("draft must preserve every candidate ID in the original order")

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
            "id": expected_ids[index],
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
        "cost_usd": 0,
    }
    validate_editorial_voice(normalized)
    return normalized


def publish_draft(
    bundle_path: Path,
    draft_path: Path,
    content_dir: Path,
    state_path: Path,
    result_path: Path | None = None,
) -> Path:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    digest = validate_draft(bundle, draft)
    selected = [Item(**item) for item in bundle["items"]]
    local_now = datetime.fromisoformat(bundle["generated_at"])
    if local_now.tzinfo is None:
        local_now = local_now.replace(tzinfo=ZoneInfo(bundle.get("timezone", "Asia/Tokyo")))
    output = content_dir / f"{local_now:%Y-%m-%d}-daily-signal.md"
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing article: {output}")
    markdown = render_markdown(digest, selected, local_now, MODEL, generator=GENERATOR)
    content_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    seen = load_seen(state_path) | {item.id for item in selected}
    write_json(state_path, {"ids": sorted(seen)})
    if result_path:
        write_json(result_path, {
            "status": "published",
            "article": str(output),
            "title": digest["title"],
            "source_count": len(selected),
            "generated_by": GENERATOR,
            "model": MODEL,
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--config", type=Path, default=Path("config/sources.yaml"))
    prepare.add_argument("--state", type=Path, default=Path("data/seen.json"))
    prepare.add_argument("--output", type=Path, default=Path(".daily-signal/candidates.json"))

    publish = subparsers.add_parser("publish")
    publish.add_argument("--bundle", type=Path, default=Path(".daily-signal/candidates.json"))
    publish.add_argument("--draft", type=Path, default=Path(".daily-signal/draft.json"))
    publish.add_argument("--content-dir", type=Path, default=Path("content/daily"))
    publish.add_argument("--state", type=Path, default=Path("data/seen.json"))
    publish.add_argument("--result", type=Path, default=Path(".daily-signal/publish-result.json"))

    args = parser.parse_args()
    if args.command == "prepare":
        bundle = prepare_bundle(args.config, args.state, args.output)
        print(args.output)
        return 0 if bundle["items"] else 3
    output = publish_draft(args.bundle, args.draft, args.content_dir, args.state, args.result)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
