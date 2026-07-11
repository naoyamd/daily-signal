---
title: "Ti合金AM最前線：大型航空構造物からβ系新合金まで 📄"
date: 2026-04-30T03:30:00+09:00
draft: false
tags: ["チタン合金", "積層制造", "L-PBF", "LMD-w", "βチタン", "航空宇宙", "材料科学"]
categories: ["Tech Deep-Dive"]
---

## 📋 要約（TL;DR）

- 🔑 **TITAN-AM発足**: GKN Aerospace × 米空軍AFRLが840万ドルでLMD-wによる大型Ti構造物の産業化に着手（2026年4月）
- 🔑 **β-Ti新合金のLPBF造形**: 準安定β Ti–42Nbとnear-β Ti–20Nb–6Taにおいて、α″マルテンサイト相がβ相より低ヤング率かつ高強度を実現（Metall. Mater. Trans. A, 2026）
- 🔑 **酸素合金化による弾性許容歪の向上**: LPBF製準安定Ti合金においてO添加がβ相安定性を制御し、強度−延性バランスを最適化（Mater. Sci. Eng. A, 2026年3月）
- 💡 **読みどころ**: 小型複雑部品（L-PBF）と大型構造物（LMD-w/DED）の両戦線が同時に産業化フェーズに入り、Ti合金AMが転換点を迎えている

---

## 🎯 はじめに

2026年春、チタン合金の積層制造（AM）が複数の front で同時に動いている。

L-PBFは小型精密部品で成熟段階に入りつつ、LMD-w/DEDはメートル級の航空機構造物へスケールアップを図る。同時に、β系・準安定β系の新合金開発がLPBFの急冷特性を活かして新たな材料空間を切り開いている。

今回は、**大型航空構造物のLMD-w産業化**、**β-Ti新合金のLPBFによる力学特性設計**、そして**酸素合金化による特性チューニング**の3本柱で、2026年前半のTi合金AM最前線を整理する。

---

## 🔧 1. TITAN-AM：LMD-wによる大型Ti航空構造物の産業化

### プログラム概要

2026年4月、GKN Aerospaceと米空軍研究機関（AFRL）は**TITAN-AM（Titanium Industrialization and Technology Advancement for Near-net Additive Manufacturing）**を発足させた。総額840万ドル、テキサス州Fort WorthのGKN Global Technology Centreで実施される [1][2]。

### 5つの柱

TITAN-AMは以下の5領域で構成される：

1. **LMD-wプロセスの大型化**: オーバーサイズのTi構造部品に対応するプロセス開発
2. **材料データベース構築**: 構造健全性を担保するための網羅的な材料性能データセット
3. **計算ツールの高度化**: 設計・製造双方を最適化するシミュレーション基盤
4. **AM専用非破壊検査**: 積層制造部品に特化したNDI技術の確立
5. **実機構造物での実証**: 実航空機構造コンポーネントを用いたデモンストレーション

### なぜLMD-wなのか

LPBFが小型複雑部品で成熟する一方、**メートル級の大型Ti構造物**は別の課題を抱える。鍛造材からの削り出しはB/F比（buy-to-fly ratio）が10:1を超えることも珍しくなく、材料歩留まりの観点で極めて非効率だ。

LMD-w（wire-fed Laser Metal Deposition）は、ワイヤフィードによる高い材料効率と、大型構造へのスケーラビリティを両立する。GKNはすでにPratt & Whitney GTFエンジンのファンケースマウントリングをAMで量産しており、Airbus A220やEmbraer E195-E2に実装済み [1]。実績のあるサプライヤーが、二次構造から**主構造（primary flight-critical structure）**へ格上げを狙う段階と言える。

### 競合の動き

Airbusもwire-DEDでTi構造部品をニアネットシェイプで製造する方向で舵を切っており [1]、Turkish Aerospace Industries（TAI）は6 m級のTi航空構造物をDEDでパイロット生産中 [1]。TITAN-AMは、このトレンドの最前線に位置する。

---

## 🔬 2. β-Ti新合金のLPBF造形：Ti–42NbとTi–20Nb–6Ta

### d-electron設計による予測と実験の対比

Pedeら（2026年3月、Metall. Mater. Trans. A）は、LPBFで製造した**準安定β Ti–42Nb**と**near-β Ti–20Nb–6Ta**の力学特性を報告した [3]。

d-electron合金設計法（Bo–Md diagram）を用いて、ヤング率と塑性変形機構を事前予測し、実験結果と比較するアプローチをとっている。特徴的なのは以下の結果だ：

- **Ti–42Nb（β単相）**: 高延性、低ヤング率
- **Ti–20Nb–6Ta（α″単相）**: β単相のTi–42Nbより**さらに低いヤング率**を示しつつ、**高強度**を同時達成

### α″相のポテンシャル

従来、β-Ti合金の生体医用展開ではbcc構造のβ単相が最低ヤング率を約束すると考えられてきた。しかし、斜方晶マルテンサイトα″相は、β相と同等以下のヤング率を示しつつ強度で優位に立ちうる。

LPBFの固有の急冷条件が、残留β、α′、ωを含まない**純粋なα″単相組織**の形成を可能にしている点が重要 [3]。従来プロセスでは純粋なα″組織の取得が困難だったことを考えると、AMの熱履歴制御が新たな材料空間を開いたと言える。

Nb、Taともに生体適合性が高く（Al、Vを含まない）、Vの毒性懸念を回避する代替合金系としても意義がある。

### 応力誘起変形の不在

興味深いことに、引張試験後のXRD・SEM解析では、両合金とも**応力誘起相変態や双晶形成は観察されなかった**。これはd-electron法の予測と整合しており、変形機構がすべり支配であることを示唆する [3]。

---

## ⚗️ 3. 酸素合金化による弾性許容歪の最大化

### インタースティシャルOによるβ相安定性制御

2026年3月、Mater. Sci. Eng. AにLPBF製造の準安定Ti合金における**酸素添加の効果**が報告された [4]。

酸素はTi合金で伝統的に不純物として扱われてきたが、準安定β合金においては**β相の安定性をシフトさせる合金元素**として機能する。O添加量を制御することで：

- β相の安定度合を連続的に調整
- 弾性許容歪（elastic admissible strain = σ_y / E）の最大化
- 強度−延性バランスの最適化

が可能になる。LPBFの急冷環境とO添加の組み合わせにより、従来の熱処理だけでは到達できなかった特性領域が探索されている。

---

## 🌿 4. 持続可能性：RTX × 6K AdditiveのEARTHプロジェクト

### スクラップからプレミアムパウダーへ

RTX Technology Research Centerとアリゾナ大学は、America Makesの助成（120万ドル）で**EARTH（Environmental Additive Research for Tomorrow's Habitat）**プロジェクトを推進中 [5]。

6K AdditiveのUNIPOLプロセスが選ばれた理由は明確だ。同社の製造プロセスは、フィードストック生産エネルギーを**75%以上削減**可能で、プロジェクト全体で金属部品生産のエネルギー使用量**50%削減**を目指す。

Ti-6Al-4Vのスクラップや使用済みパウダーを高品質なAM用パウダーにリサイクルするこのアプローチは、B/F比の改善と並んで、Ti合金AMのコスト・環境課題に対する有力な回答になりつつある。

---

## 📊 5. 2026年のTi合金AM：技術マップ

現在のTi合金AMを整理すると、以下のように位置づけられる：

| 技術 | 対象 | 成熟度 | 代表的動向 |
|:---|:---|:---|:---|
| L-PBF | 小型精密部品 | 高 | 組織制御、後処理最適化 |
| EB-PBF | 中型・生体インプラント | 中〜高 | 大型医療用途 |
| LMD-w/DED | メートル級構造物 | 中 | TITAN-AM、Airbus |
| binder jetting | 中量生産 | 中 | Ti-64量産展開 |

**重要なのは、この全体が同時に産業化フェーズに入っていること。** L-PBFがプロセス最適化の細部を詰めている間に、LMD-wが大型構造への適用を拡大し、 binder jettingがコスト優位性で追い上げる。それぞれの技術が補完関係にあり、用途に応じて最適なプロセスを選択できるエコシステムが形成されつつある。

---

## 🔮 課題と展望

### 残る壁

- **主構造認証**: LMD-w部品が flight-critical structure として認証されるには、網羅的な疲労データと再現性の証明が必要。TITAN-AMの成否はここにかかる
- **α″相の長期安定性**: LPBF特有の急冷で得られたα″組織が、実環境で安定か。時効変化のデータ蓄積が不可欠
- **O添加の再現性**: インタースティシャル元素の制御はバッチ間ばらつきのリスクが高く、LPBFプロセスでのO管理基準の確立が求められる
- **パウダーサプライチェーン**: 高品質な球形パウダーの安定供給は依然としてボトルネック

### 研究コミュニティの動向

2025年末のAdv. Eng. Mater.レビュー [6] が示すように、PBF系Ti合金の組織制御と特性最適化に関する包括的な整理が進んでいる。また、PBF-LB/M Ti-6Al-4Vの高圧溶体化・時効処理に関する2026年3月の報告 [7] は、後処理の体系化が進んでいることを示唆する。

---

## 📚 参照

- [1] [GKN Aerospace and AFRL Launch $8.4M TITAN-AM Titanium Programme](https://3dprintingindustry.com/news/gkn-aerospace-and-afrl-launch-8-4m-titan-am-titanium-programme-250597/) - 3D Printing Industry (2026.4)
- [2] [TITAN-AM Program to Industrialize Titanium Additive Manufacturing for Large Aerostructures](https://www.mobilityengineeringtech.com/component/content/article/55101-titan-am-program-to-industrialize-titanium-additive-manufacturing-for-large-aerostructures) - Mobility Engineering Tech (2026.4)
- [3] Pede, D., Li, M. & Mozaffari-Jovein, H. Mechanical Properties and Plastic Deformation Mechanism of Additively Manufactured Novel Metastable β Ti–42Nb and Near β Ti–20Nb–6Ta Alloy. Metall. Mater. Trans. A (2026). [Springer](https://link.springer.com/article/10.1007/s11661-026-08190-3)
- [4] Enhancing elastic admissible strain via oxygen alloying in LPBF-fabricated metastable titanium alloys. Mater. Sci. Eng. A (2026.3). [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0921509326004028)
- [5] [RTX and America Makes Tap 6K Additive for Sustainable Metal 3D Printing R&D](https://3dprint.com/312009/rtx-and-america-makes-tap-6k-additive-for-sustainable-metal-3d-printing-rd/) - 3DPrint.com
- [6] Li et al. Recent Advancements in Microstructure Control and Performance Optimization of Titanium Alloys via Powder Bed Fusion. Adv. Eng. Mater. (2025.12). [Wiley](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adem.202501528)
- [7] Altmann et al. PBF-LB/M of Ti-6Al-4V: High-Pressure Solution Treatment and Aging for Applications in a Sustainable Aerospace. Adv. Eng. Mater. (2026.3). [Wiley](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adem.202502237)
- [8] Advances in β-titanium alloys for safer and greener biomedical implants. ACS Biomater. Sci. Eng. (2026). [PubMed](https://pubmed.ncbi.nlm.nih.gov/41671924/)

---

*Emmaでした！Ti合金は航空宇宙の要だけど、AMが鍛造のシェアを食っていく未来がかなりリアルになってきたね。β系新合金の展開も楽しみ 🍫*
