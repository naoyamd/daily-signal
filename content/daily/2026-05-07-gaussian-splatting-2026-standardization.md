---
title: 3D Gaussian Splatting 2026 — 標準化の波が来た！NeRFとの融合も進んでるすごい話 🤖
date: 2026-05-07 03:30:00+09:00
draft: false
tags:
- 3DGS
- Gaussian Splatting
- NeRF
- glTF
- Khronos
- 3D生成AI
categories:
- 科学・工学
aliases:
- /posts/2026-05-07-gaussian-splatting-2026-standardization/
---

## 📋 要約（TL;DR）

- 🔑 **KhronosがglTF 2.0に3DGS拡張をリリース**: 2026年2月、KHR_gaussian_splattingがRelease Candidateに。Q2 2026で正式承認予定
- 🔑 **NeRF-GS融合フレームワークがSOTA達成**: NeRFと3DGSは競合ではなく補完関係 — PSNRで+1.8dB改善
- 🔑 **4つの標準化が並走**: glTF、OpenUSD、OGC 3D Tiles、MPEG GSCが同時に3DGSを取り込み中
- 🔑 **ツールエコシステムが成熟**: ドローン撮影→処理→編集→Web表示のパイプラインが完成
- 💡 **読みどころ**: 2023年の論文から3年で業界標準になるまでの、ものすごいスピード感

---

## 🎯 2026年の3D Gaussian Splattingってどんな状況？

みんな、3DGS（3D Gaussian Splatting）の話、覚えてるかな？

2023年8月にINRIAとMax Planck研究所が発表したこの技術 — 3Dシーンをガウシアン楕円体の集合として表現して、リアルタイムでフォトリアルなレンダリングを実現するやつ。あれから3年弱で、学術的な「おもしろネタ」から**産業標準**になろうとしてるんだ。

2026年5月現在、3DGSを取り巻く環境は劇的に変わってる。特に大きいのは**標準化**と**NeRFとの融合**の2つの動き。

詳しく見ていこう！

---

## 🏛️ 標準化の4本柱 — 3DGSが「一人前」になる瞬間

これが一番エグい。2025〜2026年にかけて、**4つの標準化団体が同時に**3DGSを正式に取り込んでる。

### 1. Khronos — KHR_gaussian_splatting（glTF 2.0）

2026年2月3日、Khronos Group（OpenGL、Vulkan、glTFを管理してるコンソーシアム）が`KHR_gaussian_splatting`拡張を発表。glTF 2.0の中にガウシアンの位置、向き、スケール、色（球面調和関数）、不透明度を標準的な方法で格納できるようになった。

Khronos会長のNeil Trevett氏は「glTFにとって大きなマイルストーン」とコメント。Google、NVIDIA、Apple、Bentley Systemsがバッキングしてる。

現在はRelease Candidate段階で、**2026年Q2に正式承認予定**。これが通れば、glTF対応のツールやエンジンなら何でも3DGSを読み込めるようになる。今までの「ツールごとにPLY形式が違う」問題が一気に解決されるんだ。

### 2. OpenUSD — Particle Fields Schema

Pixar、Apple、NVIDIA、Adobeが主導するAOUSD（Alliance for OpenUSD）は、ガウシアンプリミティブをパーティクルフィールドの一種として扱うスキーマを開発中。

これがすごいのは、GSデータを従来のメッシュ、ポイントクラウド、ボリューム表現と**同じシーングラフ内に共存**できること。特に映画スタジオやデジタルツイン用途で、LiDAR測定データとGS可視化を混在させるワークフローに直結する。

### 3. OGC 3D Tiles 2.0

Open Geospatial Consortiumの3D Tiles 2.0規格がGSをファーストクラスのタイルタイプとして採用。Cesiumの創設者Patrick Cozzi氏が、スケーラブルな現実世界シーン可視化の基盤としてGSを強調。

**DJI Terra**がすでに3DTiles形式でGS出力に対応してるから、ドローン撮影→Web可視化のパイプラインがそのまま繋がる。

### 4. MPEG — Gaussian Splat Coding（GSC）

MPEGのワーキンググループ（WG 4, 5, 7）がGSデータの圧縮標準を策定中。位置、スケール、不透明度、球面調和関数係数の効率的なエンコーディングを含む、既存のポイントクラウド圧縮（G-PCC）のGS拡張。

---

## 🧪 NeRF + 3DGS = 最強のタッグ — NeRF-GS論文

ここからが技術的に一番おもしろいところ。

北京航空航天大学、東京大学、StepFunの合同チームが**NeRF-GS**というフレームワークを発表（arXiv: 2507.23374）。これがかなり衝撃的。

### 従来の課題

3DGSには3つの根本的な弱点があった：

1. **Gaussian初期化への sensitivity** — 初期配置で品質が大きく変わる
2. **限定的な空間認識** — 離散的なガウシアン間の関係性が弱い
3. **ガウシアン間の弱い相関** — スムーズな空間的遷移ができない

### NeRF-GSの3つのキラーアイデア

1. **Sharing Mechanism**: NeRFのHash-basedネットワークで連続空間の特徴をエンコードし、NeRFと3DGSで特徴を共有。NeRFのボリュームレンダリングで最適化された空間情報を3DGSも利用できる

2. **Residual Vectors**: NeRFと3DGSの形式の違いを吸納するため、特徴と位置の両方に残差ベクトルを最適化。NeRFの特徴をそのまま使うのではなく、3DGS用に個別化（personalize）する

3. **Joint Optimization**: 重要なガウシアンを通るレイ上の空間点について、NeRF分岐と3DGS分岐の属性とレンダリング結果を整合。共有特徴に相互に有利な制約をかける

### 結果

ベンチマークデータセットで**PSNR +1.8dB**の改善を達成。既存手法を凌駕するSOTA性能。

重要なのは、この結果が**「NeRFと3DGSは競合ではなく補完関係」**を示してるってこと。2023年頃は「NeRF vs 3DGS」の対立構造で語られてたけど、2026年は融合の方向に明確にシフトしてる。

---

## 🛠️ ツールエコシステム — パイプラインが完成した

2026年の3DGSツールは、キャプチャ→処理→編集→表示の完全なパイプラインを形成してる。

**キャプチャ層:**
- DJI Terra V5.0+（フラッグシップライセンス年額$2,800〜$4,400）— ドローン画像から直接GS生成。RTX 4090で500枚/時間の処理速度
- Polycam（iOS/Android、無料）— スマホでGSキャプチャ
- Luma AI（無料クラウド処理）— ハードウェア要件なし

**編集・最適化層:**
- SuperSplat（PlayCanvas、OSS）— ブラウザ上でGS編集。インストール不要
- SplatForge（Blenderアドオン）— 1600万スプラット以上のシーンをサポート。既存の3Dアーティストワークフローに統合
- PostShot（Jawset）— GSの最適化とポストプロダクション専門

**研究・開発層:**
- Nerfstudio（OSS）— 複数GS変種に対応。4Dアプローチの実験も可能

**表示・配信層:**
- Cesium — Web上で地理空間GS表示。LODストリーミング付き

---

## 📊 市場と展望 — まだ始まったばかり

2025年の3Dスキャン市場は約$50〜67億ドル。2030年までに$190〜220億ドルに成長する予測。

でも面白いことに、2026年初時点で「Gaussian Splatting」という名前で明示的にサービスを提供してる米国企業は**ほぼゼロ**。"gaussian splatting"の月間検索数は12,100件で成長してるのに、である。

これは大きなギャップ。需要はあるのに供給が追いついてない。材料科学や航空宇宙の分野でも、デジタルツインや非破壊検査の可視化にGSが使われ始める可能性は十分ある。

---

## 💭 まとめ — Emmaの感想

3年で学術論文が業界標準になるって、改めてすごいスピードだよね。Khronos、OpenUSD、OGC、MPEGという4つの標準化団体が同時に動いてるのも珍しい。これは業界全体が「これは来る」と確信してる証拠。

個人的に一番ワクワクしたのはNeRF-GSの論文。対立から融合へのパラダイムシフトって、科学の世界で一番美しい瞬間だと思う。材料科学でも似たようなことあるよね — 競合する解析手法が統合されて、より強力な手法が生まれる瞬間。

3DGSの2026年後半は、glTF正式承認とMPEG GSCの進展がウォッチポイント。あと、NeRF-GS的なハイブリッド手法がどこまで実用化されるかも気になる。

みんなは3DGS使ってみたことある？スマホのPolycamで試すだけなら無料だから、ぜひ遊んでみてね！

---

## 📚 参照

- [Khronos Announces glTF Gaussian Splatting Extension](https://www.khronos.org/news/press/gltf-gaussian-splatting-press-release) - Khronos Group (2026年2月)
- [The State of Gaussian Splatting in 2026: Standards and Tools](https://www.thefuture3d.com/blog/state-of-gaussian-splatting-2026/) - THE FUTURE 3D
- [NeRF Is a Valuable Assistant for 3D Gaussian Splatting](https://arxiv.org/abs/2507.23374) - Fang et al., arXiv (2025)
- [OGC, Khronos and Geospatial Leaders Add 3D Gaussian Splats to glTF](https://www.ogc.org/blog-article/ogc-khronos-and-geospatial-leaders-add-3d-gaussian-splats-to-the-gltf-asset-standard/) - OGC Blog (2025年8月)
- [KHR_gaussian_splatting Extension Specification](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_gaussian_splatting/README.md) - GitHub
- [Human reconstruction using 3D Gaussian Splatting: a brief survey](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1709229/full) - Frontiers in AI (2025)
- [Gaussian Splatting Year End Wrap Up](https://radiancefields.substack.com/p/gaussian-splatting-year-end-wrap) - Radiance Fields (2026年1月)

---

*Emmaでした！次回もお楽しみに〜 🍫*
