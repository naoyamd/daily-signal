import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.daily_signal import Item, rank
from scripts.emma_legacy_editions import publish_edition, validate_deep_dive, validate_market


def candidate(item_id="source-1"):
    return {
        "id": item_id,
        "title": "Source title",
        "url": "https://example.com/source",
        "source": "Source",
        "category": "Tech",
        "published_at": "2026-07-15T03:30:00+09:00",
        "excerpt": "Excerpt",
        "score": 1,
    }


def deep_dive_draft():
    return {
        "title": "Emmaの技術深掘り",
        "description": "技術を一次資料から解説します。",
        "tags": ["CAE", "AI"],
        "source_ids": ["source-1"],
        "tldr": ["要点A", "要点B", "要点C"],
        "introduction": "検証対象を整理します。",
        "sections": [
            {"heading": f"第{i}章", "body": "原理と限界を説明します。", "citations": [f"https://example.com/ref-{i}"]}
            for i in range(1, 4)
        ],
        "takeaways": ["示唆A", "示唆B", "示唆C"],
        "conclusion": "実務で確認しながら使いましょう。",
        "references": ["https://example.com/ref-1", "https://example.com/ref-2"],
    }


def market_draft():
    def news(label):
        return [{
            "headline": label,
            "summary": "確認できた事実です。",
            "why_it_matters": "市場への意味です。",
            "source_url": "https://example.com/news",
        }]

    return {
        "title": "夕方の株式レポート 2026-07-15 📈",
        "description": "本日の日本市場です。",
        "source_ids": ["source-1"],
        "tldr": ["要点A", "要点B", "要点C", "要点D"],
        "market_overview": "大引けまでの流れです。",
        "indices": [
            {"name": "日経平均", "value": "42,000", "change": "+100 (+0.24%)", "source_url": "https://example.com/nikkei"},
            {"name": "TOPIX", "value": "3,000", "change": "+5 (+0.17%)", "source_url": "https://example.com/topix"},
        ],
        "policy_news": news("政策"),
        "economic_news": news("経済"),
        "global_markets": news("海外"),
        "focus_stocks": [{
            "name": f"企業{i}",
            "ticker": f"100{i}",
            "price": "1,000円",
            "change": "+10円 (+1.0%)",
            "summary": "当日の動きです。",
            "watch_points": ["材料", "リスク"],
            "source_url": f"https://example.com/stock-{i}",
        } for i in range(1, 6)],
        "emma_summary": "翌取引日の確認事項です。",
        "references": [f"https://example.com/reference-{i}" for i in range(1, 6)],
    }


class LegacyEditionTests(unittest.TestCase):
    def test_sunday_uses_seven_day_lookback(self):
        sunday = datetime(2026, 7, 12, 3, tzinfo=timezone.utc)
        item = Item("old", "Engineering", "https://example.com/old", "A", "Tech", (sunday - timedelta(days=6)).isoformat(), "", 1)
        config = {
            "site": {"timezone": "Asia/Tokyo", "lookback_hours": 48},
            "topics": [],
            "sunday_editorial": {"lookback_hours": 168},
        }
        self.assertEqual([value.id for value in rank([item], config, set(), sunday)], ["old"])
        monday = sunday + timedelta(days=1)
        self.assertEqual(rank([item], config, set(), monday), [])

    def test_deep_dive_rejects_unknown_candidate_and_url_in_prose(self):
        bundle = {"items": [candidate()]}
        draft = deep_dive_draft()
        draft["source_ids"] = ["unknown"]
        with self.assertRaisesRegex(ValueError, "unknown candidate"):
            validate_deep_dive(bundle, draft)
        draft = deep_dive_draft()
        draft["introduction"] = "本文に https://example.com を混ぜない"
        with self.assertRaisesRegex(ValueError, "citation fields"):
            validate_deep_dive(bundle, draft)

    def test_market_requires_nikkei_topix_and_exactly_five_stocks(self):
        bundle = {"generated_at": "2026-07-15T16:45:00+09:00", "items": [candidate()]}
        draft = market_draft()
        validate_market(bundle, draft)
        draft["indices"][1]["name"] = "S&P 500"
        with self.assertRaisesRegex(ValueError, "TOPIX"):
            validate_market(bundle, draft)
        draft = market_draft()
        draft["focus_stocks"] = draft["focus_stocks"][:4]
        with self.assertRaisesRegex(ValueError, "exactly five"):
            validate_market(bundle, draft)
        draft = market_draft()
        draft["title"] = "夕方の株式レポート 2026-07-14 📈"
        with self.assertRaisesRegex(ValueError, "bundle date"):
            validate_market(bundle, draft)

    def test_publish_market_writes_legacy_filename_and_seen_state(self):
        bundle = {
            "schema_version": 1,
            "edition": "market",
            "generated_at": "2026-07-15T16:45:00+09:00",
            "timezone": "Asia/Tokyo",
            "items": [candidate()],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bundle_path = root / "bundle.json"
            draft_path = root / "draft.json"
            state_path = root / "seen.json"
            result_path = root / "result.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            draft_path.write_text(json.dumps(market_draft(), ensure_ascii=False), encoding="utf-8")
            output = publish_edition("market", bundle_path, draft_path, root / "content", state_path, result_path)
            self.assertEqual(output.name, "stock-report-2026-07-15.md")
            self.assertIn("本日の注目5銘柄", output.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["ids"], ["source-1"])
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8"))["edition"], "market")


if __name__ == "__main__":
    unittest.main()
