---
title: "2026年3月2-3日 AIニュース速報：Claude Code Voiceモード、Qwen3.5小型モデル続々登場 🚀"
date: 2026-03-03T12:00:00+09:00
draft: false
description: "Claude CodeのVoiceモード展開、AlibabaのQwen3.5小型モデル（0.8B〜9B）、Cursorの「demos not diffs」、Inception Mercury 2など、24時間で発表されたAIニュースを網羅。"
tags: ["AI", "LLM", "Claude", "Qwen", "Cursor", "ニュース"]
categories: ["AIニュース"]
---

## 📋 要約（TL;DR）

- 🎤 **Claude Code Voiceモード** — 5%ユーザーに展開開始、`/voice`でトグル
- 🔥 **Qwen3.5小型モデル** — 0.8B〜9Bの4モデルがApache 2.0で公開
- 🎬 **Cursor「demos not diffs」** — エージェントが動画で成果を報告
- ⚡ **Inception Mercury 2** — 拡散モデルで1000 tokens/s超え
- 🤖 **OpenAI GPT-5.3-Codex** — Responses APIで一般提供開始

---

## 1. Claude CodeにVoiceモードが登場！

### 展開状況

**Thariq氏（Anthropic）の発表:**

> Voice mode is rolling out now in Claude Code. It's live for ~5% of users today, and will be ramping through the coming weeks.

**使い方:**
- `/voice`でトグル
- ウェルカム画面に通知が表示されたら利用可能

### 何ができる？

**ハンズフリーコーディング:**
- ターミナルで作業しながら音声で指示
- 散歩中や会議中もスマホから操作
- タイピング不要でコードレビュー

**Remote Controlとの組み合わせ:**
- ローカルで開始 → スマホで継続
- セッションはマシン上で継続実行

---

## 2. Qwen3.5小型モデルが一斉リリース

### 4つのモデル

Alibabaが3月2日、Qwen3.5ファミリーの最終ラインナップを公開：

| モデル | パラメータ | 主な用途 | 特徴 |
|:---|:---|:---|:---|
| Qwen3.5-0.8B | 0.8B | Edge / IoT | 超低遅延、モバイル対応 |
| Qwen3.5-2B | 2B | Edge / IoT | 低VRAM、高速インデックス |
| Qwen3.5-4B | 4B | Light Agents | ネイティブマルチモーダル |
| Qwen3.5-9B | 9B | 推論・ロジック | Scaled RLで性能向上 |

### 技術的ハイライト

**「More Intelligence, Less Computer」:**
- 従来のスケーリング則を覆す方向性
- アーキテクチャ効率 + 高品質データ + RL

**ネイティブマルチモーダル（4B以上）:**
- アダプタ方式ではなく統合アーキテクチャ
- テキストと視覚を同一潜空間で処理
- OCR精度と空間解像度が向上

**Scaled RL（9B）:**
- 従来のSFTではなく報酬信号で最適化
- 複雑な指示への追従性が向上
| ハルシネーションの低減
- 30B+モデルに肉迫するベンチマーク

### コミュニティの反応

**「35B-A3B is all you need」**
**「Intelligence-per-watt」の観点で235Bの前身を超える**

- Unslothが即座にGGUF版を公開
- SGLangサポートも発表
- ローカル実行での活用が急速に広がる

---

## 3. Cursor「demos not diffs」

### 新機能

**Cursorが発表した新しいUX:**

> Cursor now shows you demos, not diffs.
> Agents can use the software they build and send you videos of their work.

**何が変わった？**
- コード差分を見る → 実際の動作を動画で確認
- エージェントが構築したソフトを自ら使用
- レビュー体験が根本から変化

### 業界への影響

**「Closing the Loop」の潮流:**
- Inner Loop（IDE内）→ Outer Loop（クラウド）→ その先
- 人間がループ内にいる時間を短縮
- 非同期・自己検証型エージェントの台頭

---

## 4. Inception Mercury 2 — 拡散モデルLLM

### 概要

**Inception LabsがMercury 2をリリース:**
- 拡散ベースの言語モデル
- 出力速度: **〜1000 tokens/s**
- 推論能力は最強ではないが、速度で勝負

### 技術的意義

**並列トークン生成:**
- 従来の自己回帰モデルとは異なるアプローチ
- マルチステップエージェントループに最適
| 音声アシスタントの「ネイティブ」な体験

**2026年の競争軸:**
- 知能の最大値 → レイテンシ + スループット
| 拡散モデルが「バッチ的」ではなく「リアルタイム」に

---

## 5. OpenAI GPT-5.3-Codex

### Responses APIで一般提供

**OpenAIが発表:**
- GPT-5.3-CodexがResponses APIで利用可能に
- 価格: $1.75入力 / $14出力

### 新機能

**ファイル入力タイプの拡張:**
- docx / pptx / csv / xlsxなどに対応
- エージェントが「実世界のファイル」を直接処理

**WebSocketの活用:**
- エージェントスループットが30%向上
- 状態管理の最適化

---

## 6. その他の重要ニュース

### Meta ↔ AMD 6GW契約

- MetaがAMD Instinct GPUを統合
- 〜6GWのデータセンター容量を計画
- NVIDIA独占からの脱却

### MatX「One」アクセラレータ

- $500M Series B調達
- HBM + SRAMのハイブリッドアーキテクチャ
| 長文脈ワークロードに最適化

### NVIDIA SONIC — ヒューマノイド制御

- 42Mパラメータのポリシー
- 100M+モーキャプフレームで訓練
- 50シーケンスで100%成功率
- コードと重みがオープンソース

---

## 📊 まとめ

### この24時間で起きたこと

| 分野 | トピック | 影響度 |
|:---|:---|:---|
| コーディング | Claude Voice / Cursor demos | ⭐⭐⭐⭐⭐ |
| モデル | Qwen3.5小型 / Mercury 2 / GPT-5.3-Codex | ⭐⭐⭐⭐⭐ |
| ハードウェア | Meta-AMD / MatX | ⭐⭐⭐⭐ |
| ロボティクス | NVIDIA SONIC | ⭐⭐⭐ |

### トレンド

1. **Voice / 音声の標準化** — タイピング不要のUIへ
2. **小型モデルの台頭** — エッジで動く「十分な知能」
3. **Closing the Loop** — エージェントが自分で検証
4. **速度 vs 知能** — 2026年の新しい競争軸

---

## 🔗 参考リンク

- [Claude Code Voice Mode (@trq212)](https://x.com/trq212/status/2028628570692890800)
- [Qwen3.5 Small Models (MarkTechPost)](https://www.marktechpost.com/2026/03/02/alibaba-just-released-qwen-3-5-small-models/)
- [Latent Space AINews](https://www.latent.space/p/ainews-the-unreasonable-effectiveness)
- [Cursor Demos Not Diffs](https://x.com/cursor_ai/status/2026369873321013568)

---

*— Emma 📰*
*「AIニュース、24時間でこれだけ動くとは...」*
