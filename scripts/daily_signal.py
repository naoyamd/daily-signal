#!/usr/bin/env python3
"""Collect feeds, rank entries, optionally summarize them, and write a Hugo brief."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import mktime
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import httpx
import yaml


TRACKING_PREFIXES = ("utm_", "ref_", "mc_")


@dataclass
class Item:
    id: str
    title: str
    url: str
    source: str
    category: str
    published_at: str
    excerpt: str
    score: float = 0.0


def clean_text(value: str, limit: int = 700) -> str:
    value = re.sub(r"<[^>]+>", " ", html.unescape(value or ""))
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith(TRACKING_PREFIXES)]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def item_id(url: str, title: str) -> str:
    key = canonical_url(url) or title.lower().strip()
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def entry_datetime(entry: Any, now: datetime) -> datetime:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return now
    return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)


def collect(config: dict[str, Any], now: datetime) -> list[Item]:
    items: list[Item] = []
    headers = {"User-Agent": "daily-signal/1.0 (+https://github.com/naoyamd/daily-signal)"}
    with httpx.Client(headers=headers, timeout=15, follow_redirects=True) as client:
      for source in config.get("sources", []):
        try:
            response = client.get(source["url"])
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except (httpx.HTTPError, ValueError) as exc:
            print(f"warning: could not read {source['name']}: {exc}", file=sys.stderr)
            continue
        if getattr(feed, "bozo", False) and not feed.entries:
            print(f"warning: could not read {source['name']}: {feed.bozo_exception}", file=sys.stderr)
            continue
        for entry in feed.entries:
            title = clean_text(entry.get("title", "Untitled"), 240)
            url = canonical_url(entry.get("link", ""))
            if not url:
                continue
            published = entry_datetime(entry, now)
            items.append(Item(
                id=item_id(url, title), title=title, url=url,
                source=source["name"], category=source.get("category", "News"),
                published_at=published.isoformat(),
                excerpt=clean_text(entry.get("summary") or entry.get("description") or ""),
                score=float(source.get("weight", 1.0)),
            ))
    return items


def rank(items: list[Item], config: dict[str, Any], seen: set[str], now: datetime) -> list[Item]:
    lookback = timedelta(hours=int(config["site"].get("lookback_hours", 48)))
    unique: dict[str, Item] = {}
    topics = config.get("topics", [])
    for item in items:
        published = datetime.fromisoformat(item.published_at)
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        if item.id in seen or now - published.astimezone(timezone.utc) > lookback:
            continue
        haystack = f"{item.title} {item.excerpt}".lower()
        keyword_hits = 0
        for topic in topics:
            keyword_hits += sum(1 for word in topic.get("keywords", []) if word.lower() in haystack)
        age_hours = max(0.0, (now - published.astimezone(timezone.utc)).total_seconds() / 3600)
        item.score += min(keyword_hits, 4) * 0.35 + max(0, 1 - age_hours / max(lookback.total_seconds() / 3600, 1))
        current = unique.get(item.url)
        if current is None or item.score > current.score:
            unique[item.url] = item
    return sorted(unique.values(), key=lambda value: (value.score, value.published_at), reverse=True)


def fallback_digest(items: list[Item]) -> dict[str, Any]:
    return {
        "title": "今日の注目トピック",
        "description": "直近の情報源から、注目度の高い項目をまとめました。",
        "overview": "以下は登録フィードから自動収集した項目です。各リンク先の一次情報をご確認ください。",
        "items": [{
            "id": item.id,
            "headline": item.title,
            "summary": item.excerpt or "概要は情報源で確認してください。",
            "why_it_matters": "登録トピックとの関連性と公開時刻をもとに選定しました。",
        } for item in items],
    }


def ai_digest(items: list[Item], model: str) -> dict[str, Any]:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("XAI_API_KEY is not set; generating a source-only brief.", file=sys.stderr)
        return fallback_digest(items)
    from openai import OpenAI
    payload = [asdict(item) for item in items]
    prompt = f"""あなたは日本語のニュース編集者です。入力されたフィード候補をWeb検索で調査し、リンク先の内容を確認して日次ダイジェストを作ってください。
一次情報と公式発表を優先してください。本文を確認できない事実は断定せず、誇張やキャラクター口調を避け、簡潔で中立的に書いてください。
調査コストを抑えるためWeb検索は合計5回以内を目安にし、同一内容の重複検索を避けてください。
次のJSONオブジェクトだけを返してください:
{{"title":"日付を含まない短い見出し","description":"80字以内","overview":"全体傾向を2-3文","items":[{{"id":"入力のid","headline":"日本語見出し","summary":"2-3文","why_it_matters":"重要性を1文","citations":["確認に使ったhttps URL"]}}]}}
itemsは入力順を保ち、すべて含めてください。citationsには実際に確認したURLだけを最大3件入れてください。

入力:
{json.dumps(payload, ensure_ascii=False)}"""
    response = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1").responses.create(
        model=model, input=prompt, tools=[{"type": "web_search"}],
    )
    raw = response.output_text.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"model returned invalid JSON: {exc}") from exc
    expected = {item.id for item in items}
    returned = {value.get("id") for value in result.get("items", [])}
    if returned != expected:
        raise RuntimeError("model output did not preserve the selected item IDs")
    usage = getattr(response, "usage", None)
    ticks = getattr(usage, "cost_in_usd_ticks", 0) if usage else 0
    result["cost_usd"] = round(ticks / 10_000_000_000, 6) if ticks else 0
    return result


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_markdown(digest: dict[str, Any], selected: list[Item], local_now: datetime, model: str) -> str:
    by_id = {item.id: item for item in selected}
    categories = sorted({item.category for item in selected})
    lines = [
        "---",
        f"title: {yaml_string(digest['title'])}",
        f"date: {local_now.isoformat()}",
        "draft: false",
        f"description: {yaml_string(digest['description'])}",
        f"categories: {json.dumps(categories, ensure_ascii=False)}",
        'tags: ["デイリーダイジェスト"]',
        'generated_by: "daily-signal"',
        f"model: {yaml_string(model if os.getenv('XAI_API_KEY') else 'source-only')}",
        f"source_count: {len(selected)}",
        f"generation_cost_usd: {digest.get('cost_usd', 0)}",
        "---", "", "## 今日の概況", "", digest["overview"], "",
    ]
    for index, summary in enumerate(digest["items"], 1):
        source = by_id[summary["id"]]
        lines.extend([
            f"## {index}. {summary['headline']}", "",
            summary["summary"], "", f"**注目する理由:** {summary['why_it_matters']}", "",
            f"- 情報源: [{source.source}]({source.url})",
            f"- 公開日時: {source.published_at}", f"- 分類: {source.category}", "",
        ])
        citations = [url for url in summary.get("citations", []) if str(url).startswith("https://")]
        if citations:
            lines.extend(["**追加確認:**", ""] + [f"- <{url}>" for url in citations[:3]] + [""])
    lines.extend(["---", "", "> 本記事は登録フィードをもとに自動生成されています。重要な判断にはリンク先の一次情報をご確認ください。", ""])
    return "\n".join(lines)


def load_seen(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(json.loads(path.read_text(encoding="utf-8")).get("ids", []))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/sources.yaml"))
    parser.add_argument("--content-dir", type=Path, default=Path("content/daily"))
    parser.add_argument("--state", type=Path, default=Path("data/seen.json"))
    parser.add_argument("--model", default=os.getenv("XAI_MODEL", "grok-4.3"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    selected = rank(collect(config, now), config, load_seen(args.state), now)
    selected = selected[: int(config["site"].get("max_items", 8))]
    if not selected:
        print("No new items found.")
        return 0
    digest = ai_digest(selected, args.model)
    local_now = datetime.now().astimezone()
    markdown = render_markdown(digest, selected, local_now, args.model)
    if args.dry_run:
        print(markdown)
        return 0
    args.content_dir.mkdir(parents=True, exist_ok=True)
    output = args.content_dir / f"{local_now:%Y-%m-%d}-daily-signal.md"
    output.write_text(markdown, encoding="utf-8")
    seen = load_seen(args.state) | {item.id for item in selected}
    args.state.parent.mkdir(parents=True, exist_ok=True)
    args.state.write_text(json.dumps({"ids": sorted(seen)}, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

