#!/usr/bin/env python3
"""Publish the legacy Tech Deep-Dive and stock-market editions safely."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from scripts.daily_signal import Item, load_seen, yaml_string
from scripts.emma_pipeline import (
    GENERATOR,
    MODEL,
    prepare_bundle,
    validate_editorial_voice,
    write_json,
)


EDITIONS = ("deep-dive", "market")
DEEP_DIVE_TOPICS = (
    "材料科学・合金・積層造形",
    "航空宇宙・CAE・CFD・シミュレーション",
    "AI・機械学習・Neural Operator",
    "プログラミング言語・分散システム・ソフトウェア設計",
    "製造業・デジタルツイン・ジェネレーティブデザイン",
    "エネルギー・量子・新興科学技術",
    "過去1週間の重要技術を統合する週次Deep-Dive",
)


def _text(value: Any, field: str, *, one_line: bool = False, max_chars: int = 3000) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    value = value.strip()
    if one_line:
        value = re.sub(r"\s+", " ", value)
    if not value:
        raise ValueError(f"{field} must not be empty")
    if len(value) > max_chars:
        raise ValueError(f"{field} exceeds {max_chars} characters")
    return value


def _prose(value: Any, field: str, *, max_chars: int) -> str:
    value = _text(value, field, max_chars=max_chars)
    if re.search(r"https?://", value, flags=re.I):
        raise ValueError(f"{field} must keep URLs in citation fields")
    return value.replace("<", "&lt;").replace(">", "&gt;")


def _url(value: Any, field: str) -> str:
    value = _text(value, field, one_line=True, max_chars=1000)
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{field} must be an HTTPS URL")
    return value


def _text_list(
    value: Any,
    field: str,
    *,
    minimum: int,
    maximum: int,
    max_chars: int,
) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{field} must contain {minimum} to {maximum} values")
    return [_prose(item, f"{field}[{index}]", max_chars=max_chars) for index, item in enumerate(value)]


def _url_list(value: Any, field: str, *, minimum: int = 1, maximum: int = 20) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{field} must contain {minimum} to {maximum} URLs")
    urls = [_url(item, f"{field}[{index}]") for index, item in enumerate(value)]
    return list(dict.fromkeys(urls))


def _source_ids(bundle: dict[str, Any], value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("source_ids must contain at least one candidate ID")
    expected = {item["id"] for item in bundle.get("items", [])}
    result = [_text(item, "source_ids", one_line=True, max_chars=80) for item in value]
    if not expected or any(item not in expected for item in result):
        raise ValueError("source_ids contains an unknown candidate ID")
    return list(dict.fromkeys(result))


def prepare_edition(
    edition: str,
    config_path: Path,
    state_path: Path,
    output_path: Path,
    now: datetime | None = None,
) -> dict[str, Any]:
    if edition not in EDITIONS:
        raise ValueError(f"unsupported edition: {edition}")
    bundle = prepare_bundle(config_path, state_path, output_path, now=now)
    local_now = datetime.fromisoformat(bundle["generated_at"])
    bundle["edition"] = edition
    if edition == "deep-dive":
        bundle["editorial_note"] = (
            f"本日の優先テーマ: {DEEP_DIVE_TOPICS[local_now.weekday()]}。"
            "候補を起点に一次資料まで確認し、一つの論点を体系的に深掘りする。"
        )
    else:
        bundle["editorial_note"] = (
            "日本株の大引け後レポート。日経平均・TOPIX・為替、政治経済、海外市場、"
            "値動きに根拠のある注目5銘柄を扱う。数値には必ず確認URLを付ける。"
        )
    write_json(output_path, bundle)
    return bundle


def validate_deep_dive(bundle: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    source_ids = _source_ids(bundle, draft.get("source_ids"))
    tags = _text_list(draft.get("tags"), "tags", minimum=2, maximum=8, max_chars=40)
    tldr = _text_list(draft.get("tldr"), "tldr", minimum=3, maximum=6, max_chars=320)
    sections = draft.get("sections")
    if not isinstance(sections, list) or not 3 <= len(sections) <= 9:
        raise ValueError("sections must contain 3 to 9 sections")
    normalized_sections = []
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            raise ValueError(f"sections[{index}] must be an object")
        normalized_sections.append({
            "heading": _text(section.get("heading"), f"sections[{index}].heading", one_line=True, max_chars=120),
            "body": _prose(section.get("body"), f"sections[{index}].body", max_chars=3500),
            "citations": _url_list(
                section.get("citations"),
                f"sections[{index}].citations",
                minimum=1,
                maximum=5,
            ),
        })
    normalized = {
        "title": _text(draft.get("title"), "title", one_line=True, max_chars=160),
        "description": _text(draft.get("description"), "description", one_line=True, max_chars=280),
        "tags": tags,
        "source_ids": source_ids,
        "tldr": tldr,
        "introduction": _prose(draft.get("introduction"), "introduction", max_chars=1800),
        "sections": normalized_sections,
        "takeaways": _text_list(
            draft.get("takeaways"),
            "takeaways",
            minimum=3,
            maximum=7,
            max_chars=360,
        ),
        "conclusion": _prose(draft.get("conclusion"), "conclusion", max_chars=1600),
        "references": _url_list(draft.get("references"), "references", minimum=2, maximum=25),
    }
    validate_editorial_voice(normalized)
    return normalized


def _news_list(value: Any, field: str, *, minimum: int, maximum: int) -> list[dict[str, str]]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{field} must contain {minimum} to {maximum} entries")
    result = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{field}[{index}] must be an object")
        result.append({
            "headline": _text(item.get("headline"), f"{field}[{index}].headline", one_line=True, max_chars=140),
            "summary": _prose(item.get("summary"), f"{field}[{index}].summary", max_chars=1000),
            "why_it_matters": _prose(
                item.get("why_it_matters"),
                f"{field}[{index}].why_it_matters",
                max_chars=700,
            ),
            "source_url": _url(item.get("source_url"), f"{field}[{index}].source_url"),
        })
    return result


def validate_market(bundle: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    source_ids = _source_ids(bundle, draft.get("source_ids"))
    try:
        report_date = datetime.fromisoformat(bundle["generated_at"]).date().isoformat()
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("candidate bundle has an invalid generated_at") from exc
    title = _text(draft.get("title"), "title", one_line=True, max_chars=160)
    if title != f"夕方の株式レポート {report_date} 📈":
        raise ValueError("market title must match the candidate bundle date")
    indices = draft.get("indices")
    if not isinstance(indices, list) or not 2 <= len(indices) <= 8:
        raise ValueError("indices must contain 2 to 8 entries")
    normalized_indices = []
    for index, item in enumerate(indices):
        if not isinstance(item, dict):
            raise ValueError(f"indices[{index}] must be an object")
        normalized_indices.append({
            "name": _text(item.get("name"), f"indices[{index}].name", one_line=True, max_chars=80),
            "value": _text(item.get("value"), f"indices[{index}].value", one_line=True, max_chars=80),
            "change": _text(item.get("change"), f"indices[{index}].change", one_line=True, max_chars=80),
            "source_url": _url(item.get("source_url"), f"indices[{index}].source_url"),
        })
    index_names = {item["name"].casefold() for item in normalized_indices}
    if not any("日経" in name or "nikkei" in name for name in index_names):
        raise ValueError("indices must include Nikkei 225 / 日経平均")
    if not any("topix" in name for name in index_names):
        raise ValueError("indices must include TOPIX")

    focus_stocks = draft.get("focus_stocks")
    if not isinstance(focus_stocks, list) or len(focus_stocks) != 5:
        raise ValueError("focus_stocks must contain exactly five stocks")
    normalized_stocks = []
    for index, item in enumerate(focus_stocks):
        if not isinstance(item, dict):
            raise ValueError(f"focus_stocks[{index}] must be an object")
        normalized_stocks.append({
            "name": _text(item.get("name"), f"focus_stocks[{index}].name", one_line=True, max_chars=100),
            "ticker": _text(item.get("ticker"), f"focus_stocks[{index}].ticker", one_line=True, max_chars=30),
            "price": _text(item.get("price"), f"focus_stocks[{index}].price", one_line=True, max_chars=80),
            "change": _text(item.get("change"), f"focus_stocks[{index}].change", one_line=True, max_chars=80),
            "summary": _prose(item.get("summary"), f"focus_stocks[{index}].summary", max_chars=900),
            "watch_points": _text_list(
                item.get("watch_points"),
                f"focus_stocks[{index}].watch_points",
                minimum=2,
                maximum=5,
                max_chars=300,
            ),
            "source_url": _url(item.get("source_url"), f"focus_stocks[{index}].source_url"),
        })

    normalized = {
        "title": title,
        "description": _text(draft.get("description"), "description", one_line=True, max_chars=280),
        "source_ids": source_ids,
        "tldr": _text_list(draft.get("tldr"), "tldr", minimum=4, maximum=7, max_chars=300),
        "market_overview": _prose(draft.get("market_overview"), "market_overview", max_chars=1800),
        "indices": normalized_indices,
        "policy_news": _news_list(draft.get("policy_news"), "policy_news", minimum=1, maximum=4),
        "economic_news": _news_list(draft.get("economic_news"), "economic_news", minimum=1, maximum=5),
        "global_markets": _news_list(draft.get("global_markets"), "global_markets", minimum=1, maximum=4),
        "focus_stocks": normalized_stocks,
        "editorial_summary": _prose(
            draft.get("editorial_summary"),
            "editorial_summary",
            max_chars=1400,
        ),
        "references": _url_list(draft.get("references"), "references", minimum=5, maximum=30),
    }
    validate_editorial_voice(normalized)
    return normalized


def _front_matter(
    title: str,
    description: str,
    local_now: datetime,
    category: str,
    tags: list[str],
    source_count: int,
) -> list[str]:
    return [
        "---",
        f"title: {yaml_string(title)}",
        f"date: {local_now.isoformat()}",
        "draft: false",
        f"description: {yaml_string(description)}",
        f"categories: {json.dumps([category], ensure_ascii=False)}",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        f"generated_by: {yaml_string(GENERATOR)}",
        f"model: {yaml_string(MODEL)}",
        f"source_count: {source_count}",
        "generation_cost_usd: 0",
        "---",
        "",
    ]


def render_deep_dive(draft: dict[str, Any], local_now: datetime, source_count: int) -> str:
    lines = _front_matter(
        draft["title"],
        draft["description"],
        local_now,
        "Tech Deep-Dive",
        draft["tags"] + ["Tech Deep-Dive"],
        source_count,
    )
    lines.extend(["## 📋 要約（TL;DR）", ""])
    lines.extend([f"- {item}" for item in draft["tldr"]])
    lines.extend(["", draft["introduction"], ""])
    for section in draft["sections"]:
        lines.extend([f"## {section['heading']}", "", section["body"], "", "**参照:**", ""])
        lines.extend([f"- <{url}>" for url in section["citations"]])
        lines.append("")
    lines.extend(["## 🎯 実務への示唆", ""])
    lines.extend([f"- {item}" for item in draft["takeaways"]])
    lines.extend(["", "## 💭 まとめ", "", draft["conclusion"], "", "## 📚 参考リンク", ""])
    lines.extend([f"- <{url}>" for url in draft["references"]])
    lines.extend([
        "",
        "---",
        "",
        "> 本記事は公開情報をもとに編集されています。重要な判断には一次情報をご確認ください。",
        "",
    ])
    return "\n".join(lines)


def _render_news(lines: list[str], heading: str, items: list[dict[str, str]]) -> None:
    lines.extend([f"## {heading}", ""])
    for item in items:
        lines.extend([
            f"### {item['headline']}",
            "",
            item["summary"],
            "",
            f"**なぜ重要？** {item['why_it_matters']}",
            "",
            f"参考: <{item['source_url']}>",
            "",
        ])


def render_market(draft: dict[str, Any], local_now: datetime, source_count: int) -> str:
    lines = _front_matter(
        draft["title"],
        draft["description"],
        local_now,
        "株式レポート",
        ["株式", "日経平均", "投資"],
        source_count,
    )
    lines.extend(["## 📋 要約（TL;DR）", ""])
    lines.extend([f"- {item}" for item in draft["tldr"]])
    lines.extend(["", "## 📊 市場概況", "", draft["market_overview"], "", "### 主要指数", ""])
    lines.extend(["| 指数 | 終値・水準 | 前日比 |", "|:---|:---|:---|"])
    for item in draft["indices"]:
        lines.append(f"| [{item['name']}]({item['source_url']}) | {item['value']} | {item['change']} |")
    lines.append("")
    _render_news(lines, "🗳️ 政治・政策ニュース", draft["policy_news"])
    _render_news(lines, "📰 経済・社会ニュース", draft["economic_news"])
    _render_news(lines, "🌍 海外マーケット", draft["global_markets"])
    lines.extend(["## 🔥 本日の注目5銘柄", ""])
    for index, item in enumerate(draft["focus_stocks"], start=1):
        lines.extend([
            f"### {index}. {item['name']} ({item['ticker']})",
            "",
            f"> 株価: {item['price']} | 前日比: {item['change']}",
            "",
            item["summary"],
            "",
            "**注目ポイント:**",
            "",
        ])
        lines.extend([f"- {point}" for point in item["watch_points"]])
        lines.extend(["", f"参考: <{item['source_url']}>", ""])
    lines.extend(["## 💭 編集部のまとめ", "", draft["editorial_summary"], "", "## 📚 参考リンク", ""])
    lines.extend([f"- <{url}>" for url in draft["references"]])
    lines.extend([
        "",
        "---",
        "",
        "**免責**: この記事は情報提供目的です。投資判断は自己責任でお願いします。",
        "",
        "> 数値とニュースは執筆時点の公開情報です。取引前に取引所・証券会社等の最新情報をご確認ください。",
        "",
    ])
    return "\n".join(lines)


def publish_edition(
    edition: str,
    bundle_path: Path,
    draft_path: Path,
    content_dir: Path,
    state_path: Path,
    result_path: Path | None = None,
) -> Path:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    if bundle.get("edition") != edition:
        raise ValueError("candidate bundle edition mismatch")
    selected = [Item(**item) for item in bundle.get("items", [])]
    local_now = datetime.fromisoformat(bundle["generated_at"])
    if edition == "deep-dive":
        normalized = validate_deep_dive(bundle, draft)
        filename = f"{local_now:%Y-%m-%d}-tech-deep-dive.md"
        markdown = render_deep_dive(normalized, local_now, len(selected))
    elif edition == "market":
        normalized = validate_market(bundle, draft)
        filename = f"stock-report-{local_now:%Y-%m-%d}.md"
        markdown = render_market(normalized, local_now, len(selected))
    else:
        raise ValueError(f"unsupported edition: {edition}")

    output = content_dir / filename
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing article: {output}")
    content_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    seen = load_seen(state_path) | {item.id for item in selected}
    write_json(state_path, {"ids": sorted(seen)})
    if result_path:
        write_json(result_path, {
            "status": "published",
            "edition": edition,
            "article": str(output),
            "title": normalized["title"],
            "source_count": len(selected),
            "generated_by": GENERATOR,
            "model": MODEL,
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--edition", choices=EDITIONS, required=True)
    prepare.add_argument("--config", type=Path)
    prepare.add_argument("--state", type=Path)
    prepare.add_argument("--output", type=Path)

    publish = subparsers.add_parser("publish")
    publish.add_argument("--edition", choices=EDITIONS, required=True)
    publish.add_argument("--bundle", type=Path)
    publish.add_argument("--draft", type=Path)
    publish.add_argument("--content-dir", type=Path, default=Path("content/daily"))
    publish.add_argument("--state", type=Path)
    publish.add_argument("--result", type=Path)
    args = parser.parse_args()

    if args.command == "prepare":
        config_path = args.config or Path("config/market_sources.yaml" if args.edition == "market" else "config/sources.yaml")
        state_path = args.state or Path(f"data/seen-{args.edition}.json")
        output_path = args.output or Path(f".daily-signal/{args.edition}/candidates.json")
        bundle = prepare_edition(args.edition, config_path, state_path, output_path)
        print(output_path)
        return 0 if bundle["items"] else 3

    bundle_path = args.bundle or Path(f".daily-signal/{args.edition}/candidates.json")
    draft_path = args.draft or Path(f".daily-signal/{args.edition}/draft.json")
    state_path = args.state or Path(f"data/seen-{args.edition}.json")
    result_path = args.result or Path(f".daily-signal/{args.edition}/publish-result.json")
    output = publish_edition(
        args.edition,
        bundle_path,
        draft_path,
        args.content_dir,
        state_path,
        result_path,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
