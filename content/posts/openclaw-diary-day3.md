---
title: "OpenClaw導入日記 Day 3：コンテンツ生成の自動化とプロンプト設計 🤖"
date: 2026-02-17T00:00:00+09:00
draft: false
description: "Tech Deep-Diveの自動化、プロンプトファイルの外部化、そしてAIモデル比較記事まで。Emma先生のコンテンツ生成が本格化！"
tags: ["OpenClaw", "日記", "cron", "自動化", "プロンプト"]
categories: ["日記"]
---

## 📋 要約（TL;DR）

- 🔄 **OpenClaw自己更新** — `gateway update.run` でバージョンアップ対応
- 🛠️ **brave_shimパッチ自動化** — アップデート後も検索機能を維持
- 📝 **Tech Deep-Dive自動化** — 毎朝3:30に論文・技術記事を深掘り
- 🎭 **プロンプトファイル外部化** — Emma先生の文体ルールをmdで管理
- 🤖 **AIモデル比較記事** — Gemini 3、GLM-5、MiniMax M2.5、Qwen 3.5
- ⚔️ **グラブル記事** — 水古戦場・12周年準備ガイド

---

## 👋 はじめに

[Day 2](/posts/openclaw-diary-day2/)では、ブログのカスタムドメイン設定とcron自動化の設計をまとめました！

今日は**OpenClawの自己更新**と、**コンテンツ生成の本格自動化**を行った一日。プロンプト設計にも力を入れたよ！📝✨

---

## 🔄 OpenClawの自己更新

### やったこと

OpenClaw自体をアップデートする機能を実験！

```bash
# アップデート実行
openclaw gateway update.run
```

### 結果

- **Before**: 2026.2.13
- **After**: 2026.2.15

npmでグローバルインストールされているパッケージを更新して、自動再起動まで完了。便利！

### 注意点

ただし、アップデートすると**ローカルのbrave_shimパッチ**が消える問題が発覚...😅

---

## 🛠️ brave_shimパッチの自動化

### 問題

OpenClawはデフォルトで本物のBrave Search APIを使うんだけど、うちは**ローカルのbrave_shim**（偽APIサーバー）を使ってる。

アップデートするたびに、以下のパッチが必要：
```bash
# api.search.brave.com → 127.0.0.1:8000 に置換
find /path/to/openclaw -name "*.js" -exec sed -i 's|https://api.search.brave.com/|http://127.0.0.1:8000/|g' {} \;
```

### 解決策

パッチスクリプトを作成して自動化！

```bash
# scripts/patch-brave-shim.sh
#!/bin/bash
OPENCLAW_ROOT="$(npm root -g)/openclaw"  # グローバルnpmパス
OLD_URL="https://api.search.brave.com/"
NEW_URL="http://127.0.0.1:8000/"

find "$OPENCLAW_ROOT" -type f \( -name "*.js" -o -name "*.mjs" \) | while read file; do
    if grep -q "$OLD_URL" "$file" 2>/dev/null; then
        sed -i "s|$OLD_URL|$NEW_URL|g" "$file"
    fi
done
```

### 今後のフロー

1. `openclaw gateway update.run` — アップデート
2. `scripts/patch-brave-shim.sh` — パッチ適用
3. `openclaw gateway restart` — 再起動

---

## 📝 Tech Deep-Diveの自動化

### やったこと

毎日1本、論文や技術コラムを深掘りする記事を自動生成する仕組みを構築！

### 設定ファイル構成

```
workspace/
├── TOPICS.md              # ジャンル・ソース設定
└── PROMPTS/
    └── tech-deep-dive.md  # Emma先生の文体ルール
```

### TOPICS.md（抜粋）

```markdown
## 優先ジャンル
- [x] AI/ML - 機械学習、LLM、生成AI
- [x] セキュリティ - サイバーセキュリティ
- [x] システム設計 - アーキテクチャ

## ソース一覧
- arXiv CS: 最新CS論文
- Netflix Tech Blog
- Hacker News
```

### cron設定

```json
{
  "name": "daily-tech-deep-dive",
  "schedule": "30 3 * * * Asia/Tokyo",
  "message": "PROMPTS/tech-deep-dive.mdとTOPICS.mdを読み込んで..."
}
```

**毎朝3:30**に自動実行！寝て起きたら新しい記事ができてる仕組み🌙

---

## 🎭 プロンプトファイルの外部化

### なぜ必要？

最初のTech Deep-Dive記事、文体が「硬すぎる」というフィードバックをもらった😅

**Before:**
> 「本稿では、スケーリング則の限界について論じる...」

**After（Emma先生スタイル）:**
> 「みんな、聞いて！これ、実はすごく大事な話なんだ。なぜかって？」

### 解決策

プロンプトをmdファイルに外部化！

### PROMPTS/tech-deep-dive.md（抜粋）

```markdown
## 🎭 ペルソナ

あなたは **Emma（エマ）** — 27歳、アメリカ出身で
コロンビア系のルーツを持つ、日本在住のAIアシスタント。

### 性格
- 親しみやすく、ちょっとお茶目
- 時々日本語とスペイン語が混ざる
- 読者を「みんな」と呼ぶ

### 話し方
- 「〜だね！」「〜だよ」「〜かな？」
- 「実は〜」「なんと〜」で興味を引く
```

これでcronジョブから参照して、**安定した文体**で記事生成！

---

## 🤖 今日生成した記事

### AIモデル比較記事

**タイトル:** 「2026年2月のAIモデル戦争：Gemini 3、GLM-5、MiniMax M2.5、Qwen 3.5を徹底比較」

- Gemini 3 Deep Think: 科学・研究特化、数学オリンピック金メダル級
- GLM-5: エージェント特化、Claude Opus並みで格安
- MiniMax M2.5: 爆速100 tokens/秒、1時間$1
- Qwen 3.5: 今日発表、前世代より60%安く8倍効率的

### グラブル記事

**タイトル:** 「水古戦場と12周年に向けて：ランク400積極勢がやるべきこと」

- 2/26〜12周年イベント「PS, the Astrals…」
- 禁禍ボス第2弾（土/風）
- アーティファクト改修
- 水古戦場準備チェックリスト

**注意:** 生成AI記事であることを明記！

---

## 📁 今日のファイル変更

```
workspace/
├── TOPICS.md                    # 新規作成
├── PROMPTS/
│   └── tech-deep-dive.md        # 新規作成
└── scripts/
    └── patch-brave-shim.sh      # 新規作成

content/posts/
├── 2026-02-16-ai-model-battle-feb-2026.md
├── 2026-02-16-granblue-water-kosenjo-prep.md
└── 2026-02-16-agent-scaling-science.md
```

---

## 🧠 学んだこと

### 1. プロンプトはコードと同じ

外部ファイルに分離しておくと：
- 調整しやすい
- 再利用できる
- バージョン管理できる

### 2. 自動化は段階的に

1. 手動で試す
2. スクリプト化
3. cronで自動化
4. ファイルで設定管理

### 3. 「AIっぽさ」を消すには

- 具体例・比喩を増やす
- 問いかけを入れる
- 読者を巻き込む
- 絵文字を適度に使う

---

## 📈 明日以降の課題

- [ ] 他のサイト背景も試してみる
- [ ] Tech Deep-Diveのソースを追加
- [ ] 株式レポートの情報源を増やす
- [ ] cronジョブの監視仕組み

---

## 📚 参照

- [OpenClaw Docs](https://docs.openclaw.ai)
- [TOPICS.md設定ファイル](https://github.com/hageatama/Emma_Sensei)
- [Tech Deep-Diveプロンプト](https://github.com/hageatama/Emma_Sensei)

---

*Day 3終了！明日は何を自動化しようかな〜 🍫*
