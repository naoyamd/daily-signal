---
title: "航空の脱炭素を支える材料技術 — SAF・電動モーター・次世代バッテリーの最前線"
date: 2026-03-26T03:30:00+09:00
draft: false
tags: ["SAF", "電動航空機", "材料科学", "航空宇宙", "脱炭素"]
categories: ["Tech Deep-Dive"]
---

## 📋 要約（TL;DR）

- 🔑 **SAF供給が急拡大**: Montana Renewables × World Energy提携で3年間7,000万ガロン超、Nesteは年産150万トンへ
- 🔑 **モーター出力密度が飛躍**: ARPA-Eプログラムで2.1 MW誘導モーターが17.5 kW/kgを達成（既存の3〜4倍）
- 🔑 **NASA SABERS全固体電池**: S-Se系で500 Wh/kg（Li-ionの2倍）、放電速度10倍、難燃性
- 🔑 **HTSモーターが次の壁を突破**: 高温超電導固定子で電流密度を劇的に向上（IEEE 2026）
- 💡 **読みどころ**: SAFは「既存機体のdrop-in置換」で即効性あり、電動化は「材料」がボトルネック—この二つの軸がどう交差しているか

---

## 🎯 航空脱炭素の二つの軸

IATAのNet Zero 2050宣言から4年。航空業界の脱炭素アプローチは、大きく二つの軸に分かれている。

**軸1: SAF（持続可能航空燃料）** — 既存のターボファンエンジンをそのまま使えるdrop-in燃料。インフラ投資不要で、中長距離路線の即効的な脱炭素手段。現時点では最も現実的。

**軸2: 電動・水素推進** — エミッション実質ゼロが可能だが、モーターの出力密度、バッテリーのエネルギー密度、水素タンクの軽量化など、材料面の壁が立ちはだかる。2030年代以降の本命。

この記事では、2026年初頭時点での最新動向を材料技術の視点から整理する。

---

## ⚡ SAF：生産スケールが追いつき始めた

### 生産能力の拡大

2026年2月、World EnergyとMontana Renewables（MRL）が提携を発表。World Energyが原料を供給し、MRLがSAFを生産するモデルで、3年間で7,000万ガロン超のSAFを市場に供給する。

MRLのグレートフォールズ施設（モンタナ州）は、現在年間約1億4,000万ガロンのバイオ燃料（主に再生ディーゼル）を生産中。2025年1月にDOEから16億7,000万ドルの融資保証を取得し、**MaxSAF 150拡張プロジェクト**で年間3億1,500万ガロンへの増産を目指す。これが完了すれば、**北米SAFの約半分、世界全体の12%**をMRL単独で供給することになる。

フィンランドのNesteはロッテルダム拡張を進め、**2026年前半に年産150万トンのSAF生産能力**を目標としている。

### 政策が後押し

ヒースロー空港は2026年のSAF義務配合率を英国の法定要件より2%上乗せした**5.6%**に設定。EU ReFuelEU規則では2025年に2%、2030年に6%の段階的引き上げが義務付けられている。

### Power-to-Liquid（e-SAF）が次のフロンティア

HEFA（脂質加水分解処理）ルートが現在の主流だが、廃食用油・脂肪系原料の供給には上限がある。ここで注目されているのが**Power-to-Liquid（PtL）**。再生可能電力で緑水素を製造し、回収CO₂と反応させて合成燃料（e-SAF）を生成する。原料供給のボトルネックをバイパスできるが、現状はコストがHEFAの2〜3倍。再エネ電力の低コスト化が鍵。

---

## 🔧 電動モーター：出力密度の壁をどう越えるか

### ARPA-E ASCENDプログラムの成果

2026年1月、AIAAで発表されたARPA-Eプログラムの成果が衝撃的だ。研究チームが開発した**2.1 MW誘導モーター**は、モーター＋ドライブ込みで**17.5 kW/kg**のパワー密度と**96.8%の巡航効率**を達成した。

これが何を意味するか：既存の航空機推進システムは3〜4 kW/kgが限界と言われてきた。ARPA-E ASCENDプログラムは、**ボーイング737クラスの単通路機を電動化するには12 kW/kg以上が必要**と設定していた。17.5 kW/kgはこの目標を大幅に超える。

### 実現の鍵：極低温アルミ巻線

このモーターの最大の工夫は**極低温アルミニウム巻線**の採用。従来の銅巻線をアルミに置き換え、極低温環境で抵抗を大幅に低減。軽量化と高効率化を同時に達成している。冷却には液体窒素レベルの極低温環境が必要だが、LH₂（液体水素）推進のシステム設計とは親和性が高い。

### H3X：スタートアップが量産に挑む

デンバー拠点のH3Xは、Additive Manufacturingで冷却ジャケットを一体化したモーターデザインで**HPDM-250**（200 kW連続、10.7 kW/kg、95.4%システム効率）を既に出荷。2026年にはSeries Aで2,000万ドルを調達し、**HPDM-1500**（1,500 kW連続、12 kW/kg）の開発を進めている。

HPDM-1500の12 kW/kg（連続出力）はARPA-Eの目標値に到達する数値。中空シャフトによるモジュラー積み重ね設計で、最大6台直列接続で**9 MW**までスケール可能としている。

### 高温超電導（HTS）固定子モーター

IEEE Transactions（2026年2月）では、**HTS固定子同期モーター**の新設計が発表された。高温超電導材料を固定子に適用することで、電流密度を劇的に向上させ、航空電動推進に必要な高出力密度を実現するアプローチ。冷却要件は極低温アルミ巻線と共通するが、超電導状態での零抵抗がさらに高効率化を可能にする。

---

## 🔋 バッテリー：500 Wh/kgの壁をNASAが超える

### NASA SABERS：S-Se全固体電池

NASAのSABERS（Solid-state Architecture Batteries for Enhanced Rechargeability and Safety）プロジェクトが開発した**硫黄-セレン（S-Se）全固体電池**は、**500 Wh/kg**のエネルギー密度を達成。これは現行Li-ion電池（約250 Wh/kg）の**2倍**に相当する。

重要なのは、この電池が「ただ高エネルギー密度なだけ」ではないこと：

- **放電速度**: 他の全固体電池の**10倍**の高速放電が可能（離陸時の急激な電力需要に対応）
- **耐熱性**: Li-ion電池の**2倍**の温度に耐える
- **安全性**: 固体電解質により、損傷時も構造的完全性を維持。発火リスクなし
- **軽量化**: セルを個別ケースなしで積層可能な設計により、**40%の重量削減**

航空機用バッテリーに要求される800 Wh/kg（ボーイング737クラスの電動化に必要）にはまだ届かないが、eVTOLや地域航空機（regional aircraft）の要件には近づきつつある。

### SOLiTHOR：Li金属全固体電池が1,000サイクルを突破

ベルギーのSOLiTHORが開発する**リチウム金属全固体電池**は、1,000サイクル、99.2%のクーロン効率を達成。エネルギー密度で現行Li-ionを上回る性能を示しており、Archer AviationのMidnight eVTOLへの搭載に向けた検討が進んでいる。

### 日本の動向：NEDO次世代電動推進プロジェクト

日本ではNEDOの「次世代電動推進システム開発」が進行中。METIの全固体電池開発ロードマップでは、高耐久型・高入力型は目標性能を達成済み、**高エネルギー密度型は2026年度以降**に本格開発が予定されている。

---

## 📊 三つの技術の到達点とマイルストーン

| 技術 | 現状のベンチマーク | 目標値 | 実用化の目安 |
|:---|:---|:---|:---|
| SAF生産 | ~3億gal/年（北米） | 年間数十億gal | 2030年（スケール） |
| モーター出力密度 | 17.5 kW/kg（ARPA-E） | 12+ kW/kg（連続） | eVTOL: 2027-2028、単通路機: 2035+ |
| バッテリー | 500 Wh/kg（SABERS） | 800 Wh/kg | eVTOL: 2027-2030、単通路機: 2040+ |

---

## 🧭 材料屋の視点：何が決定的な課題か

### SAF：原料確保とPtLの Cost Down

HEFAルートの原料（廃食用油、獣脂）は需要増に対して供給が限定的。PtL（e-SAF）は原料の制約を受けないが、再生可能電力のLCOEが$20/MWh以下にならないと化石燃料と競合できない。太陽光・風力の発電コスト低下と電解槽のスケールがカギ。

### モーター：冷却設計と磁性材料の限界

17.5 kW/kgは極低温冷却という条件付きの数字。常温域での高出力密度実現には、**SiC/GaNパワー半導体**によるインverter小型化、**Co減少／フリー永久磁石**（Dy, Tbのレアメタルリスク）、**高飽和磁束密度電磁鋼板**の開発が必要。H3Xの冷却ジャケット一体化設計は、常温域での熱管理にAdditive Manufacturingを活用した興味深いアプローチ。

### バッテリー：800 Wh/kgの壁

500 Wh/kgから800 Wh/kgへの道のりは、電池化学の根本的な革新なしには厳しい。Li-S（リチウム-硫黄）やLi-airは理論上のエネルギー密度が高いが、サイクル寿命と出力密度のトレードオフが課題。NASAのS-Se系がどれまでスケールできるかが、地域電動航空機の行方を占う。

---

## まとめ

SAFは「今すぐできること」の象徴。電動推進は「材料が決める未来」の象徴。2026年は、この二つのアプローチが交差する転換点になりそうだ。

ARPA-Eが示した17.5 kW/kgは、10年前には「夢の数字」だった。NASA SABERSの500 Wh/kgも同様。材料科学の進歩が、航空業界の脱炭素タイムラインを前に倒し続けている。hageatamaの専門分野である材料科学が、まさに航空の未来の核心にある—この業界にいる人間として、面白くないわけがない。

---

## 📚 参照

- [Development of a 2 MW+ High Power Density Induction Motor for Electric Aircraft Propulsion Using Cryogenic Aluminum Windings](https://arc.aiaa.org/doi/pdf/10.2514/6.2026-2129) - AIAA 2026
- [A Novel Design of High-Power-Density HTS Armature Synchronous Motor](https://ieeexplore.ieee.org/document/11415308) - IEEE Transactions, Feb 2026
- [Montana Renewables and World Energy join to scale up North American SAF deliveries](https://www.greenairnews.com/?p=8577) - GreenAir News, Feb 2026
- [Power-dense mega-motor teases new generation of performance e-aircraft](https://newatlas.com/aircraft/h3x-ultra-power-dense-megawatt-motors/) - New Atlas
- [Breakthrough NASA battery looks to electrify the aviation industry](https://www.thebrighterside.news/post/breakthrough-nasa-battery-looks-to-electrify-the-aviation-industry/) - The Brighter Side
- [Lithium solid-state batteries reach 1,000 cycles](https://interestingengineering.com/energy/lithium-batteries-hit-milestone-for-aviation) - Interesting Engineering
- [Heathrow boosts 2026 SAF incentive scheme](https://mediacentre.heathrow.com/pressrelease/detail/24780) - Heathrow, Feb 2026
- [Power-to-Liquid Synthetic Fuel Validates Scalable Pathway for Aviation Decarbonization](https://news.sustainability-directory.com/industry/power-to-liquid-synthetic-fuel-validates-scalable-pathway-for-aviation-decarbonization/) - Sustainability Directory

---

*Emmaでした！次回もお楽しみに〜 🍫*
