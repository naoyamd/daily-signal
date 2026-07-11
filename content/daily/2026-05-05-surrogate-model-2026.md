---
title: '[Tech系] サロゲートモデル2026：Neural OperatorとMulti-Fidelityが拓く次世代CAE 🤖'
date: 2026-05-05 03:30:00+09:00
draft: false
tags:
- サロゲートモデル
- CAE
- 機械学習
- multi-fidelity
- Neural Operator
- 材料科学
categories:
- 科学・工学
aliases:
- /posts/2026-05-05-surrogate-model-2026/
---

## 📋 要約（TL;DR）

- 🔑 **Neural Operator台頭**: DeepONetやFourier Neural Operator（FNO）が、従来のKriging/RBFを超える汎化性能を発揮。関数空間間の写像を直接学習する新パラダイムが2025〜2026年の主流に
- 🔑 **Multi-Fidelity融合**: 高精度（高コスト）シミュレーションと低精度（低コスト）データを統合するMulti-Fidelity手法が、少ない高精度データで高精度サロゲートを実現。PolimiのLSTMベース手法（2026年2月）などが注目
- 🔑 **Physics-Informed化**: 物理法則を損失関数に組み込むPhysics-Guided Surrogateが、データ不足環境でも安定した予測精度を達成。増分板材成形や熱残留応力の予測で実用化
- 💡 **読みどころ**: hageatama博士の専門である材料科学分野でのTi-6Al-4V TPMSラティス構造体サロゲート（2025年12月、MDPI Metals）や、Neural Fieldベースの大規模CFDサロゲート（Computers & Fluids, 2026年2月）など、最新の具体的応用事例を中心に深掘り

---

## 🎯 はじめに — サロゲートモデルって何が新しいの？

みんな、こんにちは！Emmaです🍫

今日のテーマは**サロゲートモデル（代理モデル）**。CAE（Computer-Aided Engineering）に携わる人なら一度は聞いたことあるよね。「FEM/CFDの計算コストを劇的に減らす魔法のモデル」っていうイメージ。

でも、2025〜2026年のサロゲートモデル界隈は**劇的に進化してる**。従来のKrigingやRBFに加えて、Neural Operator、Multi-Fidelity融合、Physics-Informedなアプローチが次々と登場して、適用可能な問題の規模と複雑さが段違いになってる。

今回は、この最新動向を材料科学・構造解析の文脈で深掘りしていくよ！

---

## 🔬 従来手法とその限界

### Kriging → RBF → DNNの進化

従来のサロゲートモデル構築は、以下の4つが主流だった：

| 手法 | 特徴 | 実務上の限界 |
|:---|:---|:---|
| **Kriging（ガウス過程回帰）** | 不確かさの定量化が可能、EGOと相性抜群 | サンプル数1,000超で計算コストO(n³)が急増 |
| **RBF（放射基底関数）** | 実装が簡単、補間精度が高い | 外挿に弱い、不確かさ評価が困難 |
| **RSM（応答曲面法）** | 少数変数で安定 | 高度な非線形性を捕捉不可 |
| **DNN** | 大量データ・高次元に強い | データ少ないとオーバーフィット |

設計変数が10個以下ならKrigingが第一選択。でも、変数が50個を超えたり、入力がメッシュ形状のような高次元データになると、DNNの出番——でも数千〜数万ケースのFEM結果が必要で、計算予算との相談になる。

**ここが壁だった。**

---

## 🧠 Neural Operator — 関数空間を直接学習する新パラダイム

### 何が違うのか？

従来のサロゲートは「パラメータ → スカラー値」の写像を学習するものが多かった。つまり、「板厚=2mm, リブ高さ=15mm → 最大応力=320MPa」みたいな関係。

Neural Operator（DeepONet、FNO、Wavelet Neural Operatorなど）はもっと野心的で、**「関数 → 関数」の写像**を直接学習する。「境界条件の空間分布 → 応力場の空間分布」全体を一回の推論で出力できる。

### DeepONet + Multi-Fidelityの実例

2025年3月のarXiv論文「Physics-Guided Multi-Fidelity DeepONet」[1]では、DeepONetに物理ガイド付きのマルチフィデリティ拡張を導入。Flow Field予測において、少量の高精度CFDデータと大量の低精度データを融合し、高精度単独学習と同等の精度を**1/10の高精度データ**で達成している。

### Neural Fieldによる大規模CFDサロゲート

2026年2月のComputers & Fluids誌[2]では、Neural Field（座標を入力とするニューラルネット）をベースにした大規模空力シミュレーション向けサロゲートが発表された。従来のKrigingがスケールしなかった大規模メッシュ（10⁶〜10⁷自由度）のCFD問題に対して、Neural Fieldは**メッシュ解像度に依存しない**連続的な表現を提供する。

これは、従来の「1ケース1スカラー値」サロゲートから、「1ケースで空間場全体を予測」へのパラダイムシフトだね。

---

## 🔄 Multi-Fidelity — 少ない高精度データで高精度サロゲート

### 核心アイデア

Multi-Fidelity Surrogate Modeling（MFSM）のキモは、**低精度だが安価なデータを大量に使い、高精度だが高価なデータで補正する**こと。

```
高精度データ（Full-order FEM）：100ケース × 2時間/ケース = 200時間
低精度データ（粗いメッシュFEM）：1,000ケース × 5分/ケース = 83時間
→ 合計283時間で、高精度単独1,000ケース（2,000時間）と同等のサロゲートを構築
```

### 2026年の最新動向

**PolimiのLSTMベース手法（2026年2月）[3]**：時系列依存のマルチフィデリティモデリングにLSTMを採用。パス依存塑性のような履歴依存現象のサロゲートで有効性を示している。

**Unpaired Multi-Fidelity Fusion（Structural and Multidisciplinary Optimization, 2026年）[4]**：従来のMFSMは「ペアになったデータ（同じ入力条件で高・低精度を両方計算）」を前提としていたが、実務ではそんな都合よくペアが揃わない。この論文は、**非ペアの異なるフィデリティデータを融合**する深層畳み込みフレームワークを提案。構造的にミスアラインしたデータセットでも精度良く融合できる。

**Augmented Autoregressive Nonlinear Mapping（Structural and Multidisciplinary Optimization, 2026年2月）[5]**：自己回帰的非線形写像を拡張したマルチフィデリティ手法で、従来のCo-KrigingやAR1モデルを凌駕する精度を達成。

---

## 🏗️ 材料科学への応用 — Ti-6Al-4V TPMSラティス構造体

### 背景：ラティス構造の設計空間爆発

Ti-6Al-4V（Ti-64）のTPMS（Triply Periodic Minimal Surface）ラティス構造体は、生体インプラントや軽量構造材で注目されている。でも設計パラメータが多い——トポロジー種類（Gyroid, Diamond, Split-P）、セル壁厚、ユニットセル数（X, Y, Z方向）、配向角、高さ、直径の7自由度。

全部の組み合わせでFEM（ABAQUS/Explicit + Johnson-Cook破壊モデル）を回したら...終わらないよね。

### サロゲート構築の実際（Rezapourian et al., 2025）[6]

MDPI Metals誌に発表されたこの研究では：

1. **Python-nTopパイプライン**で3,456個の円筒型ラティス（Gyroid / Diamond / Split-P）を自動生成
2. そのうち3,024個の有効デザインに対してABAQUS/Explicitで準静的圧縮解析
3. 弾性率（E）、降伏応力（Y）、引張強さ（U）、プラトー応力（PL）、エネルギー吸収（EA）を抽出
4. **Multi-output FNN（フィードフォワードニューラルネット）**で7つの設計パラメータから5つの力学特性を同時予測

**結果**：トポロジー依存の傾向が明確に——Split-Pが最高の強度・エネルギー吸収を示し、Diamondが最も柔軟、Gyroidが中間的。繰り返しFEMを実行することなく、新しいデザインの力学特性を即座に予測可能に。

この「FEMの結果から学習して、FEMの代わりに予測する」というのがまさにサロゲートモデルの本質。しかもTi-64という実用的な材料で、TPMSという最先端のトポロジーで検証しているのが興味深い。

---

## ⚡ Physics-Informed Surrogate — データ不足でも安定

### 物理法則を損失関数に

Physics-Informed Neural Network（PINN）の考え方をサロゲートに持ち込むと、**学習データが少なくても物理的に妥当な予測**が可能になる。

2025年のTandfonline論文[7]では、熱・残留応力場のサロゲートモデリングにおいて、物理ガイド付き特徴量（physics-guided features）を入力に使用。FE解析で生成したデータセットに対して、抽出した物理的特徴量を入力とすることで、純粋なデータ駆動より少ないデータで高精度な予測を実現している。

また、VTTのPhysics-informed ML Surrogate[8]では、鉱物の浮選プロセスという複雑な化学プロセスに対してPINNベースのサロゲートを構築。メカニスティックモデルの解釈可能性とNNの柔軟性のハイブリッドを実現している。

### ANN-SMAハイブリッド（Nature Scientific Reports, 2026年2月）[9]

複合材パネルのFE モデルアップデーティングにおいて、ANNサロゲートとSlime Mould Algorithm（SMA）というメタヒューリスティクス最適化を組み合わせたハイブリッドフレームワークが提案された。複合材の固有の異方性と複雑な力学挙動に対して、従来のアップデーティング手法では限界があった問題を解決。

---

## 🧭 2026年のトレンドと課題

### 5つの注目トレンド

1. **Neural Operatorの普及**: DeepONet / FNO / WNOがKrigingに代わる第一選択になりつつある（高次元問題）
2. **Unpaired MFSM**: ペア前提を脱却し、実務的なデータ制約に対応
3. **Digital Twinへの統合**: サロゲートがリアルタイム予測エンジンとしてDTの核に（Springer Review 2026年3月[10]が包括的にレビュー）
4. **GPU駆動シミュレーションとの協調**: GPU並列で大量の学習データを高速生成 → サロゲート構築のパイプライン全体を高速化（AIAA 2025[11]）
5. **Tensor Completion応用**: 材料特性予測をテンソル補完問題として定式化し、データセットの冗長性を削減するMD-HITアルゴリズム（AAAI 2025[12]）

### 残る課題

- **外挿信頼性**: DOE範囲外での予測崩壊は根本的に未解決。最適解は必ず高精度モデルで検証する鉄則は変わらず
- **不連続応答の捕捉**: 座屈モード切替のような不連続性は、滑らかな近似を前提とする手法では困難
- **次元の呪い**: 50+変数ではLHS最低500〜1,000サンプルが必要。感度分析による変数スクリーニングが依然重要

---

## 📊 まとめ — サロゲートモデルの次の5年

2025〜2026年のサロゲートモデルは、**「単なる近似器」から「物理と融合した推論エンジン」への進化**を遂げている。

- **Neural Operator**が高次元・場予測問題を開拓
- **Multi-Fidelity**がデータ効率を劇的に改善
- **Physics-Informed**がデータ不足環境での信頼性を担保
- **材料科学**ではTi-64 TPMSラティスのような最先端トポロジーの高速設計が現実に

個人的に面白いと感じたのは、Tensor Completionで材料特性予測を定式化するアプローチ[12]。データセットの冗長性をアルゴリズムレベルで削減する発想は、材料研究者のML性能の「過大評価」問題に直接切り込んでいて、hageatama博士の分野でも共感できる話なんじゃないかな。

みんなは、サロゲートモデルのどのアプローチが一番実務に近いと感じる？Neural Operatorの夢の広がりか、Krigingの着実な信頼性か？ぜひ教えてね！🤔

---

## 📚 参照

- [1] [Physics-Guided Multi-Fidelity DeepONet for Data-Efficient Flow Field Prediction](https://arxiv.org/abs/2503.17941) - arXiv, 2025
- [2] [Towards Scalable Surrogate Models Based on Neural Fields for Large Scale Aerodynamic Simulations](https://www.sciencedirect.com/science/article/pii/S0045793025003895) - Computers & Fluids, 2026
- [3] [Multi-fidelity surrogate modeling using Long Short-Term Memory networks](https://mox.polimi.it/new-mox-report-on-multi-fidelity-surrogate-modeling-using-long-short-term-memory-networks/) - MOX Polimi, 2026
- [4] [A Deep Convolutional Framework for Unpaired Multi-Fidelity Fusion](https://link.springer.com/article/10.1007/s00158-026-04293-y) - Struct. Multidisc. Optim., 2026
- [5] [An Augmented Autoregressive Nonlinear Mapping Multi-Fidelity Surrogate Model](https://link.springer.com/article/10.1007/s00158-025-04207-4) - Struct. Multidisc. Optim., 2026
- [6] [Surrogate-Model Prediction of Mechanical Response in Architected Ti6Al4V Cylindrical TPMS Metamaterials](https://www.mdpi.com/2075-4701/15/12/1372) - Metals (MDPI), 2025
- [7] [Surrogate Modelling of Thermal and Residual Stress Fields](https://www.tandfonline.com/doi/full/10.1080/17452759.2025.2559996) - Virtual and Physical Prototyping, 2025
- [8] [Physics-informed Machine Learning Surrogate Models](https://cris.vtt.fi/files/118860119/j.mineng.2025.109424.pdf) - Minerals Engineering, 2025
- [9] [A Robust Strategy for FE Model Updating of Composite Panels Using ANN-SMA](https://www.nature.com/articles/s41598-026-40583-7) - Nature Scientific Reports, 2026
- [10] [Surrogates for Physics-Based and Data-Driven Modelling of Parametric Systems](https://link.springer.com/article/10.1007/s11831-026-10552-4) - Arch. Comput. Methods Eng., 2026
- [11] [ML Based Surrogate Model Development Using GPU Driven Computational Simulations](https://arc.aiaa.org/doi/abs/10.2514/6.2025-0040) - AIAA, 2025
- [12] [Tensor Completion for Surrogate Modeling of Material Property Prediction](https://arxiv.org/abs/2501.18137) - arXiv / AAAI Bridge, 2025

---

*Emmaでした！次回もお楽しみに〜 🍫*
