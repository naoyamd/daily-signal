"""Pure publishing models and Markdown rendering for the Daily Signal blog.

Collection, web research, learning, and the Obsidian pool intentionally live in
the separate ``daily-signal-collector`` repository.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


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
    source_kind: str = "feed"
    doi: str = ""
    authors: list[str] = field(default_factory=list)
    query: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    matched_keywords: list[str] = field(default_factory=list)
    candidate_signals: dict[str, Any] = field(default_factory=dict)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_seen(path: Path) -> set[str]:
    if not path.exists():
        return set()
    value = json.loads(path.read_text(encoding="utf-8"))
    ids = value.get("ids", []) if isinstance(value, dict) else []
    return {str(item) for item in ids}


def render_markdown(
    digest: dict[str, Any],
    selected: list[Item],
    local_now: datetime,
    model: str,
    generator: str = "daily-signal",
) -> str:
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
        f"generated_by: {yaml_string(generator)}",
        f"model: {yaml_string(model)}",
        f"source_count: {len(selected)}",
        f"generation_cost_usd: {digest.get('cost_usd', 0)}",
        "---",
        "",
        "## 今日のご案内 ☕✨",
        "",
        digest["overview"],
        "",
    ]
    for index, summary in enumerate(digest["items"], 1):
        source = by_id[summary["id"]]
        lines.extend([
            f"## {index}. {summary['headline']}",
            "",
            summary["summary"],
            "",
            f"**💡 注目しておきたい理由:** {summary['why_it_matters']}",
            "",
            f"- 🔗 情報源: [{source.source}]({source.url})",
            f"- 🕰️ 公開日時: {source.published_at}",
            f"- 🗂️ 分類: {source.category}",
            "",
        ])
        citations = [url for url in summary.get("citations", []) if str(url).startswith("https://")]
        if citations:
            lines.extend(["**📚 追加で確認した資料:**", ""])
            lines.extend(f"- <{url}>" for url in citations[:3])
            lines.append("")
    lines.extend([
        "---",
        "",
        "> 本記事は登録フィードと公開情報をもとに編集されています。"
        "重要な判断にはリンク先の一次情報をご確認ください。",
        "",
    ])
    return "\n".join(lines)
