---
title: Transolverとその派生技術 — TransformerはPDEをどう解くのか
date: 2026-05-14
draft: false
summary: 清華大の龍明盛ラボがICML 2024で発表したTransolverは、Neural Operatorの常識を変えた。Physics-Attentionによる「物理状態の学習」は何が凄いのか、Transolver++、Transolver-3、UniSolver、GeoTransolver、LinearNOといった派生技術を含めて体系的に解説する。
tags:
- Neural Operator
- Transformer
- PDE
- CFD
- Physics-Attention
- Transolver
categories:
- 科学・工学
aliases:
- /posts/2026-05-14-transolver-ecosystem/
---

## はじめに — PDEを「解く」ということ

偏微分方程式（PDE）は、流体力学、熱伝導、構造解析、電磁場など、工学のあらゆる場所に現れる。Navier-Stokes、Darcy、弾性方程式……名前を上げればきりがない。

従来、これらはFEM（有限要素法）やFDM（有限差分法）で離散化し、数値計算で解くのが当たり前だった。1回のシミュレーションに数時間〜数日かかるのも日常茶飯事。

**Neural Operator**は、この「入力→出力の写像」をニューラルネットで学習してしまおうというアプローチだ。学習済みモデルなら推論は秒単位。FNO（Fourier Neural Operator）を筆頭に様々な手法が提案されてきたが、**複雑な形状のメッシュ**に対応するのはずっと難題だった。

そこに登場したのが **Transolver** だ。

---

## Transolver — メッシュの裏にある「物理状態」を学ぶ

### 基本思想

論文: *Transolver: A Fast Transformer Solver for PDEs on General Geometries* (ICML 2024 Spotlight)
著者: Haixu Wu, Huakun Luo, Haowen Wang, Jianmin Wang, Mingsheng Long（清華大学）
コード: <https://github.com/thuml/Transolver>

Transolverの核心はシンプルだ:

> **メッシュの個々の点にattentionをかけるのではなく、その裏にある「物理状態（physical states）」を学んで、その状態間でattentionを計算する。**

従来のTransformerベースNeural Operator（OFormer、GNOTなど）は、メッシュの全点に対して直接attentionを適用していた。でも、自動車の周りの流れ場なら数万点のメッシュがある。二次の計算量は致命的だし、何より「点と点の関係」を見ているだけで「物理的な構造」を捉えられていない。

### Physics-Attentionの仕組み

Transolverが提案した **Physics-Attention** は以下の3ステップで動く:

1. **Slice（スライス化）**: メッシュ上の点を、学習可能な重みで柔軟にグルーピングする。似た物理状態の点が同じスライスに集まる
2. **Slice Attention**: 各スライスを物理を意識したトークン（physics-aware token）にエンコードし、トークン間でattentionを計算
3. **Deslice（逆スライス化）**: attentionの結果を元のメッシュ点にマッピングし直す

この設計の面白さは、**スライスの形状が固定されていない**こと。ViTのパッチのように正方形に切るのではなく、「この付近は衝撃波領域」「ここは後流領域」というふうに、物理的な意味に沿って自律的に分割される。

論文のFigure 1が秀逸で——Darcy流れなら流体-構造相互作用のパターン、翼の周りなら衝撃波と後流、自動車なら前後面と上下空間——というふうに、学習されたスライスが実際の物理状態を明確に反映しているのが可視化されている。

### 計算量の優位性

Physics-Attentionは線形計算量で動く。メッシュ点数をN、スライス数をSとすると、attentionの計算量はO(N×S)而非O(N²)。実用上はSを小さく抑えられるので、大きなメッシュでも高速に処理できる。

### ベンチマーク結果

6つの標準ベンチマークで一貫してSOTAを達成:

- **Darcy Flow**（多孔質媒体中の流れ）
- **Elasticity**（弾性変形、Plates/Plate-Mesh）
- **Navier-Stokes**（流体、NS-2d/NS-3d）

従来SOTA比で **22%の相対改善**。しかも自動車設計（ShapeNetCar）や翼設計（AirfRANS）のような大規模産業シミュレーションでも優位性を発揮。

---

## Transolver++ — 100万点メッシュへのスケールアップ

論文: *Transolver++: An Accurate Neural Solver for PDEs on Million-Scale Geometries* (2025)
コード: <https://github.com/thuml/Transolver_plus>

Transolverは素晴らしかったが、対象は数万点のメッシュまで。産業用途では100万点以上のメッシュが当たり前だ。

Transolver++は以下の工夫でこの壁を突破した:

- **極度に最適化された並列化フレームワーク**: 複数GPUでの線形スケールが可能
- **局所適応メカニズム**: 大規模メッシュから物理状態を効率的に抽出
- **単一GPUで100万点の入力を初めて処理**: GPUを増やせばさらにスケール

結果として、標準ベンチマークで13%の改善、100倍大規模な産業シミュレーション（自動車・3D航空機）で20%以上の性能向上を達成。

---

## Transolver-3 — 1.6億セルへの挑戦

論文: *Scaling Up Transformer Solvers to Industrial-Scale Geometries* (2026.02)

2026年2月に発表された最新版。**1.6億セル（160M cells）** のメッシュを処理できるようになった。

鍵となる技術:

- **Faster Slice & Deslice**: 行列積の結合則を利用した高速化
- **Geometry Slice Tiling**: 物理状態の計算を分割して処理
- **Amortized Training**: 元の高解像度メッシュのランダムな部分集合で学習
- **Physical State Caching**: 推論時のキャッシュ技術

DrivAerML（自動車空力ベンチマーク）のフルサイズでSOTAを達成。航空機・自動車設計タスクで実用レベルに到達している。

---

## UniSolver — 万能PDEソルバーへの道

論文: *UniSolver: PDE-Conditional Transformers Are Universal PDE Solvers* (ICML 2025)
コード: <https://github.com/thuml/Unisolver>

これも同じ清華大龍ラボからの成果。

Transolverが「特定のPDEを解く」のに対し、UniSolverは**「様々なPDEを汎用的に解く」**ことを目指す。PDEの方程式記号、境界条件、初期条件などの「PDE構成要素」を条件付けとしてTransformerに入力し、異なる方程式系でも一つのモデルで対応する。

アプローチ:

- PDEの数学的構造に基づき、完全なPDE構成要素セットを定義
- domain-wise（領域全体に適用）と point-wise（個別の点に適用）の条件を柔軟に埋め込み
- データ駆動と物理知識の両方を活用

3つの大規模ベンチマークで一貫してSOTA。一つのモデルでDarcy、Navier-Stokes、弾性などをカバーできる可能性を示した。

---

## GeoTransolver — 幾何学情報を物理状態に統合する

論文: *GeoTransolver: Learning Physics on Irregular Domains Using Multi-scale Geometry Aware Physics Attention Transformer* (2025.12)

NVIDIA PhysicsNeMoフレームワーク上で実装・公開されている派生。

標準のTransolverに **GALE（Geometry-Aware Learning Engine）** を組み合わせ、マルチスケールのball queryで計算された幾何学・境界条件コンテキストを、各ブロックの物理状態空間に投影する。

特徴:

- ドメイン構造と運転条件を潜在空間にアンカー
- DrivAerML、Luminary SHIFT-SUV/Wingで評価
- Drag/LiftのR²スコアとフィールド変数の相対L1誤差で既存手法を凌駕
- 幾何学・条件変化に対するロバスト性が高い

NVIDIA PhysicsNeMo公式サンプルとして Transolver for Darcy Flow が組み込まれており、GeoTransolverはその実用的拡張版と言える。

---

## LinearNO — 「Transolverは実はLinear Attentionだった」

論文: *Transolver Is a Linear Transformer: Revisiting Physics-Attention Through the Lens of Linear Attention* (2025.11)

これは外部からの興味深い分析論文。

**主張**: TransolverのPhysics-Attentionは、実は線形注意の特殊ケースとして定式化できる。しかも、スライス間のattention（slice attention）は必ずしも性能に寄与しておらず、**スライス化と逆スライス化の操作そのもの**が有効性の主因である可能性がある。

この洞察に基づいて提案された **LinearNO（Linear Attention Neural Operator）** は:

- Physics-Attentionを正準線形注意（canonical linear attention）に再設計
- パラメータ数を平均40%削減
- 計算コストを36.2%削減
- 6つの標準PDEベンチマークでSOTAを達成
- AirfRANSやShapeNetCarの産業レベルデータセットでも優秀

「もっとシンプルで速くて精度もいい」という結果は、Transolverの設計意図を裏から照らす面白い研究だ。

---

## 応用: 衝突動力学への適用

論文: *Automotive Crash Dynamics Modeling Accelerated with Machine Learning* (2025.10)

NVIDIA PhysicsNeMoフレームワーク上で、Transolverを自動車の衝突シミュレーションに適用した研究。

- **データセット**: BIW（Body-in-White）衝突データ、LS-DYNAによる150回のFE解析
- **対象**: 200以上のコンポーネントを持つ車両構造体の変形予測
- **モデル**: MeshGraphNetとTransolverを比較
- **結果**: 完全なFE精度にはまだ届かないが、桁違いの計算コスト削減を実現
- **意義**: クラッシュシミュレーションへのML適用の実現可能性を実証

航空宇宙材料開発に携わる人間としては、衝撃波伝播や塑性変形のサロゲートモデルとしての可能性が気になるところだ。

---

## Transolverエコシステム全体像

| 名前 | 年 | 役割 | スケール |
|:---|:---|:---|:---|
| **Transolver** | 2024 | 基礎モデル。Physics-Attentionの提案 | 数万点 |
| **Transolver++** | 2025 | 並列化・大規模化。単GPU100万点対応 | 100万点 |
| **Transolver-3** | 2026 | 産業スケール対応。幾何学スライスタイリング | 1.6億セル |
| **UniSolver** | 2025 | 汎用PDEソルバー。PDE条件付け | 複数方程式系 |
| **GeoTransolver** | 2025 | 幾何学情報統合。PhysicsNeMo実装 | 産業レベル |
| **LinearNO** | 2025 | Physics-Attentionの線形注意再解釈 | 汎用（軽量化）|

---

## なぜTransolverが大事なのか

### 1. 「点」から「状態」へのパラダイムシフト

従来のNeural Operatorは「メッシュ点」を直接扱っていた。Transolverは「物理状態」を学ぶ。この違いは大きい。メッシュの形状に依存しないから、異なる形状のドメインにも汎化できる。

### 2. 産業への即時適用可能性

自動車設計、航空機設計、そして衝突シミュレーション。NVIDIA PhysicsNeMoへの統合は、実用性の強力な証明だ。数日かかっていたCFD解析を秒単位に短縮できる世界が近づいている。

### 3. スケーラビリティの系統的進化

Transolver → ++ → -3 の進化は、学術的なproof-of-conceptから産業規模への系統的なスケールアップを示している。1.6億セルを処理できるということは、実製品の設計サイクルに直接組み込めるレベルだ。

### 4. 理論と実践の対話

LinearNOによる「Transolverは実はLinear Attentionだ」という分析は、経験的に上手くいっている手法の真の有効要因を特定する好例だ。研究コミュニティが成熟している証拠でもある。

---

## 材料科学・航空宇宙エンジニアへの示唆

Ti合金のミクロ組織シミュレーション、Ni基超合金のクリープ解析、CFDによる伝熱解析……これらはすべてPDEの世界だ。Transolver系列の技術が実用レベルに達しつつある今、以下のような応用が現実味を帯びてくる:

- **合金設計の高速スクリーニング**: 相場法（phase-field）のサロゲートモデル
- **タービンブレード冷却設計**: 複雑形状の伝熱CFDを秒単位で評価
- **積層造造形の熱歪み予測**: 非定常熱伝導のリアルタイム推論
- **衝撃・クラッシュ解析**: 自動車だけでなく航空機構造にも

---

## まとめ

Transolverは「TransformerでPDEを解く」というアイデアを、**物理状態を学ぶ**という一つの洞察で根本的に変えた。そこから派生したエコシステムは、学術ベンチマークから産業規模の1.6億セルまで、系統的にスケールアップしている。

材料科学、流体力学、構造解析——PDEに携わるエンジニアにとって、この系列の動向は **今こそ注目すべき** だと思う。

---

### 参考リンク

- Transolver論文: <https://arxiv.org/abs/2402.02366>
- Transolver++論文: <https://arxiv.org/abs/2502.02414>
- Transolver-3論文: <https://arxiv.org/abs/2602.04940>
- UniSolver論文: <https://arxiv.org/abs/2405.17527>
- GeoTransolver論文: <https://arxiv.org/abs/2512.20399>
- LinearNO論文: <https://arxiv.org/abs/2511.06294>
- 衝突動力学応用: <https://arxiv.org/abs/2510.15201>
- GitHub: <https://github.com/thuml/Transolver>
- Neural Solver Library: <https://github.com/thuml/Neural-Solver-Library>
- NVIDIA PhysicsNeMo: <https://github.com/NVIDIA/physicsnemo>
