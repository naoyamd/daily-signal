import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.daily_signal import Item, canonical_url, item_id, rank, render_markdown


class DailySignalTests(unittest.TestCase):
    def test_canonical_url_removes_tracking(self):
        self.assertEqual(canonical_url("HTTPS://Example.com/a/?utm_source=x&keep=1#top"), "https://example.com/a?keep=1")

    def test_rank_deduplicates_and_filters_seen(self):
        now = datetime.now(timezone.utc)
        config = {"site": {"lookback_hours": 48}, "topics": [{"keywords": ["AI"]}]}
        first = Item(item_id("https://a.test/1", "AI news"), "AI news", "https://a.test/1", "A", "Tech", now.isoformat(), "", 1)
        duplicate = Item(first.id, first.title, first.url, "B", "Tech", now.isoformat(), "", 2)
        old = Item("old", "old", "https://a.test/old", "A", "Tech", (now - timedelta(days=3)).isoformat(), "", 5)
        result = rank([first, duplicate, old], config, set(), now)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source, "B")
        self.assertEqual(rank([first], config, {first.id}, now), [])

    def test_sunday_editorial_boosts_design_over_chinese_model_detail(self):
        now = datetime(2026, 7, 12, 3, tzinfo=timezone.utc)  # Sunday in Japan
        config = {
            "site": {"lookback_hours": 48, "timezone": "Asia/Tokyo"},
            "topics": [],
            "sunday_editorial": {
                "priority_keywords": ["design", "aerospace"],
                "deprioritize_keywords": ["Qwen"],
                "priority_boost": 0.65,
                "deprioritize_penalty": 0.45,
            },
        }
        design = Item("design", "AI design for aerospace", "https://a.test/design", "A", "Tech", now.isoformat(), "", 1)
        model = Item("model", "Qwen minor benchmark update", "https://a.test/model", "A", "Tech", now.isoformat(), "", 2)
        result = rank([model, design], config, set(), now)
        self.assertEqual(result[0].id, "design")

    def test_render_contains_source(self):
        now = datetime.now(timezone.utc)
        item = Item("1", "Title", "https://example.com", "Source", "Science", now.isoformat(), "Excerpt")
        digest = {"title": "Brief", "description": "Desc", "overview": "Overview", "cost_usd": 0.01, "items": [{"id": "1", "headline": "見出し", "summary": "要約", "why_it_matters": "理由", "citations": ["https://example.org/check"]}]}
        output = render_markdown(digest, [item], now, "test-model")
        self.assertIn("https://example.com", output)
        self.assertIn("https://example.org/check", output)
        self.assertIn("source_count: 1", output)
        self.assertIn("generation_cost_usd: 0.01", output)


if __name__ == "__main__":
    unittest.main()

