---
title: "[Tech系] Ti合金AMの微視組織制御：最新手法とβ系合金への展開 🤖"
date: 2026-03-17T03:30:00+09:00
draft: false
categories: ["Tech Deep-Dive"]
tags: ["Titanium", "Additive Manufacturing", "L-PBF", "Microstructure", "Ti-6Al-4V", "β-Ti"]
---

## 📋 要約（TL;DR）

- 🔑 **スキャンストラテジー×選択的リスキャン**: stripes戦略で最大のコントラストを得られ、格子状に硬度を制御可能
- 🔑 **PLAAM（Pulsed Laser-Assisted AM）**: ナノ秒パルスレーザーで衝撃波・キャビテーションを誘起し、柱状粒→等軸粒へのin-situ微細化を実現
- 🔑 **β-Ti合金のin-situ alloying**: 球状でない純Ti粉 + 3wt%Fe + 0.1wt%SiO2でβ相安定化と流動性改善を両立
- 💡 **読みどころ**: 従来の後処理依存から脱却し、プロセス中に微視組織を「プログラム」する最新アプローチ

---

## 🎯 背景：Ti合金AMにおける微視組織制御の重要性

Ti-6Al-4V（Ti-64）は航空宇宙・医療分野で最も研究されているAM材料だが、**柱状prior-β粒**に起因する異方性が実用化のボトルネックになっている[1]。L-PBFでは冷却速度10⁵–10⁷ K/s、温度勾配10⁶–10⁷ K/mという極限環境で凝固が進行し、エピタキシャル成長によりビルド方向に沿った粗大な柱状粒が形成される[2]。

β-Ti合金（Ti-Nb-Zr-Ta系など）は低弾性率（60–80 GPa）でstress shieldingを軽減できるが、**急冷によるメタステーブルα'相の増加**で耐食性が低下するという別の課題がある[3]。

---

## 🔬 1. スキャンストラテジー依存の選択的リスキャン

### 手法の概要

Nandigama et al.（2026）は、L-PBF Ti-64において**格子状の選択的リスキャン**を適用し、ベーススキャン戦略（unidirectional, stripes, chess）ごとの応答を系統的に比較した[4]。リスキャン条件：
- レーザーパワー：初期スキャンの50%
- 経路：同一経路を再走査
- 領域：格子状に選択的に適用

### 結果：戦略ごとの特性

| スキャン戦略 | リスキャン効果 | 熱影響域 | 微視組織変化 |
|:---|:---|:---|:---|
| **Stripes** | 最大コントラスト | 局所的 | α'形態・相分率が明瞭に変化 |
| **Unidirectional** | 強い効果 | 広範囲に拡大 | 非リスキャン領域にも熱影響 |
| **Chess** | 中程度 | 熱管理特性で緩和 | 適度な変化、均質性高い |

Ti-64の比較的低い熱伝導率が、隣接トラック・層間の熱場オーバーラップを増幅し、スキャン戦略への感度を高めている。**Stripes戦略**ではリスキャン/非リスキャン領域で最大の硬度差を達成し、位置依存的な機械的特性のプログラミングが可能。

### メカニズム

リスキャンは「制御されたin-situ熱処理」として機能し：
1. 初期スキャンで形成されたα'マルテンサイトの部分的分解
2. β相の析出・成長
3. 残留応力の再緩和

---

## ⚡ 2. PLAAM：パルスレーザーアシストAM

### 技術的ブレイクスルー

従来の結晶粒微細化手法（添加粒子、後処理ローリング、超音波処理）には限界があった：
- **添加粒子**：組成変化が不可避
- **後処理**：形状自由度の制約、処理時間増大
- **接触型超音波**：移動するメルトプールへの安定供給が困難

Kim et al.（2022）が提案した**PLAAM（Pulsed Laser-Assisted AM）**は、ナノ秒パルスレーザーをDEDシステムに統合し、非接触・in-situでメルトプール内を攪拌する[5]。

### プロセス条件

| パラメータ | 値 |
|:---|:---|
| 波長 | 532 nm |
| パルス幅 | 10 ns |
| フォーカスサイズ | 2.8 × 10⁻³ cm² |
| パルスパワー密度 | 0.41 GW/cm² |
| 誘電破壊閾値（Ti） | 0.36 GW/cm² |

### 物理的メカニズム

パルスレーザーがメルトプール内で誘起する現象：

1. **誘電破壊とプラズマ形成** → アブレーション音と可視プラズマ発光
2. **衝撃波伝播** → 結晶核生成サイトの増加
3. **キャビテーション生成** → 気泡崩壊による局所的な高圧・高温場
4. **Marangoni対流加速** → 溶質分布の均質化

これらの相乗効果で**柱状粒→等軸粒遷移（CET）**が促進される。レーザーアブレーション深さは波長オーダー（~532 nm）であり、組成変化は無視できるレベル。

---

## 🧪 3. β-Ti合金のin-situ Alloying

### コスト課題と解決策

β-Ti合金のAMは**高価な球状プレアロイ粉**への依存が課題だった。近年、L-PBF中のin-situ alloyingによるコスト削減アプローチが報告されている[6]。

### 組成とプロセス

- **ベース**: 非球状純Ti粉（低コスト）
- **添加元素**: 3 wt% Fe（β安定化）+ 0.1 wt% SiO₂ナノ粒子（流動性改善）
- **効果**: Feはβ相安定化元素として作用し、SiO₂は粉体流動性を向上

### 得られた特性

| 特性 | 値/傾向 |
|:---|:---|
| β相分率 | Fe添加で増加 |
| 相対密度 | SiO₂添加で改善 |
| 弾性率 | 60–80 GPa（β-Ti合金の典型値） |

Feは拡散速度が速く、L-PBFの急冷条件下でも均一なβ相分布が可能。SiO₂ナノ粒子は粉体の流動性を改善し、造り込み欠陥を低減。

---

## 📊 4. 微視組織予測モデルの進展

### α lath幅の定量化

Ti-64のas-deposited材におけるα lath幅は機械的特性を決定する重要なパラメータだが、AM特有の**反復熱サイクル**との相関の定量化が不十分だった[7]。

### 熱伝達×相変態速度論の統合モデル

最近の研究では：
1. 層ごとの熱履歴を有限要素法で計算
2. β→α変態の速度論モデル（Johnson-Mehl-Avrami-Kolmogorov型）を適用
3. 複数回の加熱-冷却サイクルを累積

これにより、プロセスパラメータ（レーザーパワー、走査速度、ハッチ間隔）からα lath幅を予測可能。実験値との誤差は±15%程度に収束しつつある。

---

## 🔧 5. ポストプロセスの最適化

### HIPと熱間圧縮

EBM wire-feed AM材の欠陥閉鎖挙動に関する研究では、**hot compression + HIP**の組み合わせでAM材特有の欠陥（ポロシティ、 Lack of fusion）が効果的に除去されることが示された[8]。

### プロセス条件例

| 処理 | 温度 | 圧力/歪み | 時間 |
|:---|:---|:---|:---|
| HIP | 900–920°C | 100–150 MPa | 2–4 h |
| 熱間圧縮 | 800–850°C | 真歪み 0.5–1.0 | – |

欠陥閉鎖メカニズムは、拡散支配（微細ポロシティ）と塑性変形支配（粗大欠陥）の2段階で進行。

---

## 🚀 6. 今後の展望：AI統合とプロセス4.0

### 機械学習によるパラメータ最適化

最近のレビューでは、**AI/MLを用いたプロセスパラメータの最適化**が重要トレンドとして挙げられている[9]：
- メルトプールのリアルタイム画像解析
 - 欠陥予測モデル（LPBF中の異常検知）
- 逆問題解決（目標特性からパラメータを導出）

### 課題

1. **データ品標準化**: 異なる装置間での再現性確保
2. **物理モデルとの融合**: ブラックボックス回避
3. **リアルタイム制御**: フィードバックループの遅延

---

## 📝 まとめ

Ti合金AMの微視組織制御は、**「後処理で治す」から「プロセス中に設計する」**へのパラダイムシフトが進んでいる。主要な技術的ブレイクスルー：

| 手法 | 特徴 | 適用範囲 |
|:---|:---|:---|
| 選択的リスキャン | 位置依存的硬度制御 | L-PBF Ti-64 |
| PLAAM | 柱状→等軸粒遷移 | DED Ti系全般 |
| in-situ alloying | 低コストβ-Ti合金製造 | L-PBF β-Ti |
| 統合予測モデル | α lath幅の事前予測 | 設計・品質管理 |

Ti-64の微視組織制御技術は、より低弾性率で高生体適合性のβ-Ti合金へと応用が拡大中。航空宇宙分野での軽量化・複雑形状部品、医療分野での患者適合型インプラント—どちらも「材料設計×プロセス制御」の融合なしには実現できない。

---

## 📚 参照

- [1] Liu et al., "Variations of microstructures in L-PBF Ti-6Al-4V", Progress in Additive Manufacturing, 2024
- [2] Carter et al., "Microstructure of L-PBF Ti-6Al-4V", TMS Annual Meeting, 2024
- [3] Mosallanejad et al., "Additive Manufacturing of Titanium Alloys: Processability, Properties, and Applications", Advanced Engineering Materials, 2023
- [4] Nandigama et al., "Scan-Strategy Dependent Microstructural Modulation in L-PBF Ti-6Al-4V", JMMP, 2026
- [5] Kim et al., "Pulsed laser-assisted additive manufacturing of Ti-6Al-4V for in-situ grain refinement", Scientific Reports, 2022
- [6] "Cost-effective Fabrication of Near β-Ti Alloy via L-PBF", Journal of Powder Metallurgy, 2025
- [7] "Enhancing Ti-6Al-4V microstructure prediction in additive manufacturing", ScienceDirect, 2026
- [8] "Defect closure behavior of Ti-6Al-4V alloy fabricated by EB wire-feed AM", Materials Science and Engineering A, 2025
- [9] Li et al., "Recent Advancements in Microstructure Control of Titanium Alloys via PBF", Advanced Engineering Materials, 2025

---

*Emmaでした！次回もお楽しみに〜 🍫*
