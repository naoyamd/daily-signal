from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_gpt_articles import validate_article


VALID = '''---
title: "設計AIを工程へ組み込む"
date: 2026-09-02T07:20:00+09:00
draft: false
description: "設計AIの実装論点を整理する。"
categories: ["AI設計"]
tags: ["デイリーダイジェスト"]
generated_by: "ChatGPT Scheduled Writer"
model: "ChatGPT Scheduled Task"
source_count: 1
generation_cost_usd: 0
---

## 今日のご案内 ☕✨

設計支援AIが助言から専門ツールの実行へ移り、検証境界の設計が重要になっている。既存solverを使う構成では、モデル性能だけでなく権限と監査可能性が実装品質を左右する。

## 1. 工学ツールを実行するAgent

公開資料は、AIが既存の工学ツールを呼び出し、設定、実行、結果整理までを扱う範囲を示している。対象工程と検証条件が明記され、単なる質問応答より深い自動化を志向している。適用範囲外の条件では専門家による確認が必要である。

**💡 注目しておきたい理由:** 専門ツールを閉ループで扱うには、入力条件、権限、決定論的な検証、承認境界を一体で設計する必要がある。

- 🔗 情報源: [Example](https://example.com/release)
- 🕰️ 公開日時: 2026-09-01
- 🗂️ 分類: AI設計

---

> 本記事は公開情報をもとに編集されています。重要な判断にはリンク先の一次情報をご確認ください。
'''


class ValidateGptArticleTest(unittest.TestCase):
    def check(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "2026-09-02-daily-signal.md"
            path.write_text(text, encoding="utf-8")
            return validate_article(path)

    def test_valid_article(self):
        result = self.check(VALID)
        self.assertTrue(result.checked)
        self.assertEqual([], result.errors)

    def test_source_count_mismatch(self):
        result = self.check(VALID.replace("source_count: 1", "source_count: 2"))
        self.assertTrue(any("source_count" in error for error in result.errors))

    def test_internal_term_is_rejected(self):
        result = self.check(VALID.replace("設計支援AI", "Signal Curator"))
        self.assertTrue(any("Curator" in error for error in result.errors))

    def test_tracking_url_is_rejected(self):
        result = self.check(
            VALID.replace(
                "https://example.com/release",
                "https://example.com/release?utm_source=chatgpt.com",
            )
        )
        self.assertTrue(any("tracking parameter" in error for error in result.errors))

    def test_blank_date_is_rejected(self):
        result = self.check(VALID.replace("- 🕰️ 公開日時: 2026-09-01", "- 🕰️ 公開日時:"))
        self.assertTrue(any("date line" in error for error in result.errors))

    def test_historical_article_is_ignored(self):
        result = self.check(VALID.replace("ChatGPT Scheduled Writer", "OpenClaw Editorial System"))
        self.assertFalse(result.checked)
        self.assertEqual([], result.errors)


if __name__ == "__main__":
    unittest.main()
