#!/usr/bin/env python3
"""Validate ChatGPT-authored Daily Signal Markdown before Hugo deployment.

The validator intentionally targets only articles whose front matter declares
``generated_by: ChatGPT Scheduled Writer``. Historical content is left alone.
It uses only the Python standard library so it can run in the existing Pages
workflow without installing dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit

GENERATED_BY = "ChatGPT Scheduled Writer"
REQUIRED_FRONT_MATTER = {
    "title",
    "date",
    "draft",
    "description",
    "categories",
    "tags",
    "generated_by",
    "model",
    "source_count",
    "generation_cost_usd",
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "ChatGPT citation token": re.compile(r"(?:cite|filecite|memcite)"),
    "internal Scout term": re.compile(r"(?:Company|Research) Scout", re.IGNORECASE),
    "internal Curator term": re.compile(r"Signal Curator", re.IGNORECASE),
    "internal handoff term": re.compile(r"gpt_handoff", re.IGNORECASE),
    "internal prompt term": re.compile(r"prompt", re.IGNORECASE),
}
IDENTITY_PATTERN = re.compile(r"Emma|エマ", re.IGNORECASE)
SELF_REFERENCE_PATTERN = re.compile(r"(?:私|わたし|筆者|執筆者)(?:は|が|の|として)")
PRIMARY_SOURCE_PATTERN = re.compile(
    r"^- 🔗 情報源:\s*\[[^\]]+\]\((https://[^)\s]+)\)\s*$", re.MULTILINE
)
PUBLIC_DATE_PATTERN = re.compile(r"^- 🕰️ 公開日時:[ \t]*([^\n]*)$", re.MULTILINE)
NUMBERED_HEADING_PATTERN = re.compile(r"^##\s+(\d+)\.\s+.+$", re.MULTILINE)
URL_PATTERN = re.compile(r"https?://[^\s)>]+")
TRACKING_KEYS = {"src_trk", "gclid", "fbclid", "mc_cid", "mc_eid"}


@dataclass
class ValidationResult:
    path: Path
    checked: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass
    try:
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
            return float(value)
    except ValueError:
        pass
    return value.strip('"\'')


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("file must start with YAML front matter")
    marker = normalized.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("front matter closing marker is missing")
    front_text = normalized[4:marker]
    body = normalized[marker + 5 :]
    values: dict[str, Any] = {}
    for number, line in enumerate(front_text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace() or ":" not in line:
            raise ValueError(f"unsupported front matter syntax on line {number}")
        key, raw = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"empty front matter key on line {number}")
        values[key] = _parse_scalar(raw)
    return values, body


def _has_tracking_parameter(url: str) -> bool:
    parts = urlsplit(url)
    for key, _ in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.casefold()
        if lowered.startswith("utm_") or lowered in TRACKING_KEYS:
            return True
    return False


def _validate_front_matter(path: Path, front: dict[str, Any], result: ValidationResult) -> None:
    missing = sorted(REQUIRED_FRONT_MATTER - set(front))
    if missing:
        result.errors.append(f"missing front matter fields: {', '.join(missing)}")
        return

    if front.get("generated_by") != GENERATED_BY:
        result.errors.append(f"generated_by must be {GENERATED_BY!r}")
    if front.get("draft") is not False:
        result.errors.append("draft must be false")

    title = front.get("title")
    if not isinstance(title, str) or not title.strip():
        result.errors.append("title must be a non-empty string")
    description = front.get("description")
    if not isinstance(description, str) or not description.strip():
        result.errors.append("description must be a non-empty string")
    elif len(description) > 240:
        result.errors.append("description exceeds 240 characters")

    categories = front.get("categories")
    if not isinstance(categories, list) or not categories or not all(isinstance(v, str) and v for v in categories):
        result.errors.append("categories must be a non-empty string array")
    tags = front.get("tags")
    if not isinstance(tags, list) or "デイリーダイジェスト" not in tags:
        result.errors.append('tags must include "デイリーダイジェスト"')

    model = front.get("model")
    if not isinstance(model, str) or not model.strip():
        result.errors.append("model must be a non-empty string")

    source_count = front.get("source_count")
    if isinstance(source_count, bool) or not isinstance(source_count, int) or source_count < 1:
        result.errors.append("source_count must be a positive integer")

    try:
        date_value = datetime.fromisoformat(str(front.get("date")))
    except ValueError:
        result.errors.append("date must be ISO 8601")
    else:
        if date_value.tzinfo is None:
            result.errors.append("date must include a timezone")
        match = re.match(r"(\d{4}-\d{2}-\d{2})-daily-signal\.md$", path.name)
        if match and date_value.date().isoformat() != match.group(1):
            result.errors.append("front matter date does not match article filename")

    cost = front.get("generation_cost_usd")
    if isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost < 0:
        result.errors.append("generation_cost_usd must be a non-negative number")


def _numbered_sections(body: str) -> list[str]:
    matches = list(NUMBERED_HEADING_PATTERN.finditer(body))
    sections: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        wildcard = body.find("\n# 今日の紛れ枠", match.end(), end)
        if wildcard >= 0:
            end = wildcard
        sections.append(body[match.start() : end])
    return sections


def _validate_body(front: dict[str, Any], body: str, result: ValidationResult) -> None:
    if "## 今日のご案内 ☕✨" not in body:
        result.errors.append("opening heading is missing")
    if not NUMBERED_HEADING_PATTERN.search(body):
        result.errors.append("at least one numbered item is required")
    if not body.rstrip().endswith(
        "> 本記事は公開情報をもとに編集されています。重要な判断にはリンク先の一次情報をご確認ください。"
    ):
        result.errors.append("final source-warning blockquote is missing or altered")

    for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
        if pattern.search(body):
            result.errors.append(f"public body contains {label}")
    if IDENTITY_PATTERN.search(body) or SELF_REFERENCE_PATTERN.search(body):
        result.errors.append("public body must use anonymous, non-first-person editorial voice")

    primary_urls = PRIMARY_SOURCE_PATTERN.findall(body)
    source_count = front.get("source_count")
    if isinstance(source_count, int) and len(primary_urls) != source_count:
        result.errors.append(
            f"source_count is {source_count}, but {len(primary_urls)} primary source lines were found"
        )
    if len(primary_urls) != len(set(primary_urls)):
        result.warnings.append("the same primary URL is used for multiple items")

    date_values = PUBLIC_DATE_PATTERN.findall(body)
    for index, value in enumerate(date_values, 1):
        if not value.strip():
            result.errors.append(f"public date line {index} is blank; use an exact date or 日付不明")

    for url in URL_PATTERN.findall(body):
        if not url.startswith("https://"):
            result.errors.append(f"non-HTTPS URL: {url}")
        if _has_tracking_parameter(url):
            result.errors.append(f"tracking parameter must be removed from URL: {url}")

    for index, section in enumerate(_numbered_sections(body), 1):
        if "**💡 注目しておきたい理由:**" not in section:
            result.errors.append(f"numbered item {index} lacks why-it-matters text")
        if not PRIMARY_SOURCE_PATTERN.search(section):
            result.errors.append(f"numbered item {index} lacks a primary source line")
        if "- 🕰️ 公開日時:" not in section:
            result.errors.append(f"numbered item {index} lacks a publication date line")
        if "- 🗂️ 分類:" not in section:
            result.errors.append(f"numbered item {index} lacks a category line")
        prose = section.split("**💡 注目しておきたい理由:**", 1)[0]
        prose = re.sub(r"^##.*$", "", prose, flags=re.MULTILINE).strip()
        if len(prose) < 100:
            result.errors.append(f"numbered item {index} is too thin ({len(prose)} characters before rationale)")
        citation_count = len(re.findall(r"^- <https://", section, flags=re.MULTILINE))
        if citation_count > 3:
            result.errors.append(f"numbered item {index} has more than three supporting references")


def validate_article(path: Path) -> ValidationResult:
    result = ValidationResult(path=path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result.errors.append(f"could not read file: {exc}")
        return result

    # Historical and manually authored articles are intentionally outside this gate.
    if f'generated_by: "{GENERATED_BY}"' not in text and f"generated_by: '{GENERATED_BY}'" not in text:
        return result
    result.checked = True
    try:
        front, body = split_front_matter(text)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result
    _validate_front_matter(path, front, result)
    _validate_body(front, body, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("content/daily")],
        help="Markdown files or directories to validate",
    )
    args = parser.parse_args(argv)

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*-daily-signal.md")))
        else:
            files.append(path)

    checked = 0
    failed = 0
    for path in files:
        result = validate_article(path)
        if not result.checked and not result.errors:
            continue
        checked += int(result.checked)
        for warning in result.warnings:
            print(f"warning: {path}: {warning}", file=sys.stderr)
        for error in result.errors:
            print(f"error: {path}: {error}", file=sys.stderr)
        if result.errors:
            failed += 1
    print(f"validated {checked} ChatGPT-authored article(s); failures={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
