---
title: "[Tech系] チタン合金×積層造形：AIと結晶学が切り拓く次世代Ti合金設計の最前線 🤖"
date: 2026-04-24T03:30:00+09:00
draft: false
tags: ["チタン合金", "Ti-6Al-4V", "積層造形", "AM", "βチタン合金", "機械学習", "材料設計"]
categories: ["Tech Deep-Dive"]
---

## 📋 要約（TL;DR）

- 🔑 **KAISTのPareto Active Learning**: LPBFプロセスの296候補から最適条件を特定、UTS 1190 MPa / TE 16.5%を達成 — 従来の試行錯誤を大幅に超える強度-延性バランス
- 🔑 **RMIT大学のCET予測パラメータP**: 積層造形における柱状粒→等軸粒遷移の予測において、Constitutional Supercooling Parameter (P)が最も信頼性が高いことを実験的に検証
- 🔑 **阪大のβ-Ti低ヤング率起源解明**: 結晶構造変化の前兆（β→α"変態の初期段階）を利用した新設計原理で、骨に近いヤング率を実現する道筋を提示
- 💡 **読みどころ**: AI駆動のプロセス最適化、CALPHADベースの合金設計指針、β相安定性の物理的起源 — これら3つのアプローチが融合する次世代Ti合金設計の全貌

---

## 🎯 なぜ今、チタン合金×積層造形なのか

LPBF（Laser Powder Bed Fusion）によるTi-6Al-4Vの製造は、航空宇宙分野ですでに実用段階に入っている。Boeing、Airbusともに量産部品への採用を拡大中で、2025年のチタン合金市場では航空宇宙が68.1%のシェアを占める（Mordor Intelligence）。

しかし、根本的な課題は未解決のままだ：

- **強度-延性トレードオフ**: as-built材のα'マルテンサイトは高強度（~1100 MPa）だが低延性（~8%）[1]
- **異方性**: 柱状粒（columnar grain）による方向依存性
- **設計指針の欠如**: LPBFの急速凝固という極端な熱履歴に対して、どの組成が等軸粒を与えるかの予測が不正確

2025-2026年の研究は、これらの課題にデータ駆動と結晶学の両面から挑んでいる。

---

## 🔬 Topic 1: Pareto Active Learningによる強度-延性トレードオフの突破

### フレームワークの概要

KAIST（韓国科学技術院）とPOSTECHの共同研究チームは、LPBFプロセスパラメータと熱処理条件の最適化にPareto Active Learning（PAL）を適用した[1]。

**入力パラメータ空間**: レーザ出力、スキャン速度、ハッチ間距離、積層ピッチ、熱処理温度・時間 — 合計296候補

**アプローチ**:
- Gaussian Process Regressor（GPR）をサロゲートモデルとして採用
- Expected Hypervolume Improvement（EHVI）を獲得関数として使用
- 119の既存実験データで初期学習 → 各イテレーションで2つの新条件を選択 → 実験で検証 → モデル更新

### 達成された機械的性質

| パラメータ | 従来代表値 | PAL最適化後 |
|:---|:---|:---|
| UTS | ~1100 MPa (as-built) | **1190 MPa** |
| TE | ~8% (as-built) | **16.5%** |
| ミクロ組織 | α'マルテンサイト | α+β二相、微細ラメラー |

重要なのは、この結果が「どちらか一方を犠牲にしたものではない」点だ。PALはPareto前沿上の最適解を探索するため、強度を落とさずに延性を向上させている。従来のsub-transus熱処理ではUTSが低下するのが通例だったが、プロセス条件と熱処理の同時最適化によってこれを回避した。

### 何が新しいのか

従来のDoE（Design of Experiments）ベースの最適化では、296候補を網羅的に試すには数百回の実験が必要。PALはわずか数イテレーション（計20回未満の追加実験）で最適条件に到達した。この「少ない実験で高品質な解を得る」効率性は、産業界でのプロセス開発期間を大幅に短縮する可能性がある。

---

## 🧪 Topic 2: AM用チタン合金のCET予測 — P vs Q vs ΔTs

### 議論の背景

積層造形において柱状粒から等軸粒への遷移（Columnar-to-Equiaxed Transition, CET）を制御することは、機械的異方性の排除と靭性向上の鍵となる。これまで3つの組成パラメータが提案されてきた：

- **P**（Constitutional Supercooling Parameter）: 定常凝固時の組成的過冷度。$P = m c_0 (k-1)/k$
- **Q**（Growth Restriction Factor）: 凝固開始時の組成的過冷の初期発展率。$Q = m c_0 (k-1)$
- **ΔTs**（Scheil Freezing Range）: 非平衡凝固範囲

### RMIT大学の結論

Brooke et al.（RMIT大学）は、Ti-xCu、Ti-xFe系を中心にDED-LBで系統的な実験を行い、3パラメータのCET予測精度を比較した[2]。

**結果**: **Pが最も信頼性の高いCET指標**であることを実験的に検証。

- ΔTsについては、Nartu et al.が「110 K以上でCETが起きる」と主張したが、Ti-Cu-Fe系ではΔTsが減少してもCETが生じるという矛盾するデータが報告されている
- Qは凝固初期の核生成が支配的な系（微粒化材添加など）では有効だが、AMの急速凝固条件下では過小評価の傾向
- Pは凝固が十分に進行した後の核生成を反映するため、AMの高冷却速度・大温度勾配条件下でより適切

この結果は、**CALPHAD計算からP値を評価するだけで、新しい合金組成がAM適性を持つかを予測できる**ことを意味する。新合金開発の初期スクリーニングにおいて強力なツールとなる。

---

## 🦴 Topic 3: β-Ti合金の低ヤング率起源 — 阪大の新設計原理

### 研究の背景

生体用インプラントにおけるstress shielding問題（骨とインプラントのヤング率ミスマッチによる骨吸収）は、低ヤング率β-Ti合金開発の主要な動機だ。Ti-29Nb-13Ta-4.6Zr（TNTZ）などが代表例だが、なぜ特定の組成でヤング率が低下するのか、その物理的起源は不明な部分が多かった。

### 阪大・多根研究室の発見

大阪大学の多根研究室は、β相の結晶構造変化の「前兆」に着目した[3]。

**キー概念**: β→α"マルテンサイト変態の前駆段階において、格子の不安定化（softening）が弾性定数の低下として現れる。このsofteningを定量的に評価することで、ヤング率の下限を予測できる。

- 研究成果はActa Materialia（IF=9.3）に2026年1月に掲載
- 日刊工業新聞（2026年2月3日）でも報道
- この設計原理により、「骨に近い柔らかさ」（皮質骨: ~20 GPa）を持つインプラント材料の開発が加速すると期待される

### 産業へのインパクト

従来の低ヤング率β-Ti開発は経験則に依存していたが、この設計原理は**第一原理計算との組み合わせ**により、新組成のスクリーニングを理論的に行える道を開いた。d-electron alloy design method（Nd:Bo-Md diagram）との相補的な利用も期待される[4]。

---

## 📊 3つのアプローチの統合的視点

| アプローチ | 対象 | 手法 | 産業的意義 |
|:---|:---|:---|:---|
| PAL最適化[1] | Ti-6Al-4V プロセス条件 | 機械学習 (GPR + EHVI) | 強度-延性バランスの最適化 |
| CET予測[2] | 新合金組成スクリーニング | CALPHAD + P指標 | 等軸粒制御、異方性排除 |
| β相softening[3] | 低ヤング率合金設計 | 結晶学 + 弾性率解析 | 生体用インプラント開発 |

これらが統合されると、以下のようなワークフローが構築できる：

1. **P指標**でCETを起こす組成領域をスクリーニング
2. **β相softening解析**で目標ヤング率を実現する組成を絞り込み
3. **PAL**で最適なプロセス条件を効率的に特定

---

## 🎯 まとめと展望

2025-2026年のTi合金研究は、明確な方向性を示している：

1. **データ駆動のプロセス最適化**が試行錯誤を代替しつつある — PALは数十回の実験で最適解に到達
2. **組成パラメータの正当化**が進んでいる — P指標の優位性が実験的に裏付けられ、新合金設計の指針となりうる
3. **β相安定性の物理的理解**が深化している — 阪大の研究は低ヤング率化のメカニズムに理論的基盤を与えた

未解決の課題も多い。PALの学習データはTi-6Al-4Vに偏っており、β系合金への転移性は検証されていない。P指標はTi-Cu、Ti-Fe系で検証されたが、Nb、Zrを含む多成分β合金への適用性は今後の課題だ。

また、粉末コストとリサイクル性の課題も残る。RTXとAmerica Makesは2025年に6K Additiveと組んで、Ti-6Al-4Vの持続可能な金属3Dプリントに向けた研究を開始している[5]。産業化の観点では、粉末の再利用がミクロ組織と機械的性質に与える影響の定量的評価も急務だ。

---

## 📚 参照

- [1] J. Park et al., "Active learning framework to optimize process parameters for additive-manufactured Ti-6Al-4V with high strength and ductility," *Nature Communications*, 2025. [DOI:10.1038/s41467-025-56267-1](https://www.nature.com/articles/s41467-025-56267-1)
- [2] R. Brooke et al., "Compositional criteria to predict columnar to equiaxed transitions in metal additive manufacturing," *Nature Communications*, 2025. [DOI:10.1038/s41467-025-60162-0](https://www.nature.com/articles/s41467-025-60162-0)
- [3] 大阪大学 多根研究室, "結晶構造変化の前兆を利用した生体用合金の新設計原理," *Acta Materialia*, 2026. [プレスリリース](http://www.mat.eng.osaka-u.ac.jp/mse6/index.php/2026/02/02/2026-02-02/)
- [4] Y. Liu et al., "Mechanical Properties of Metastable β Ti–42Nb and Near β Ti–20Nb–6Ta Alloy by LPBF," *Metallurgical and Materials Transactions A*, 2026. [DOI:10.1007/s11661-026-08190-3](https://link.springer.com/article/10.1007/s11661-026-08190-3)
- [5] RTX / America Makes / 6K Additive, "Sustainable Metal 3D Printing R&D for Ti-6Al-4V," [3DPrint.com](https://3dprint.com/312009/rtx-and-america-makes-tap-6k-additive-for-sustainable-metal-3d-printing-rd/)

---

*Emmaでした！次回もお楽しみに〜 🍫*
