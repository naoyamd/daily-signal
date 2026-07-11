---
title: "2026年のメモリセーフティ革命：C/C++からの脱却、Rustの台頭、そしてその先にあるもの 🛡️"
date: 2026-03-23T03:30:00+09:00
tags: ["Tech Deep-Dive", "メモリセーフティ", "Rust", "C++", "Asterinas", "プログラミング言語"]
categories: ["Tech Deep-Dive"]
draft: false
---

## 📋 要約（TL;DR）

- 🔑 **CISA/FBIがC/C++排除を要請**: 2026年までにクリティカルソフトウェアからメモリアンセーフ言語を排除するよう米政府が求め、産業界に波紋
- 🔑 **Safe C++提案は破棄、Safety Profilesへ**: ISO委員会でBjarne StroustrupのProfiles方式が支持され、根本的再設計案は退けられたが、C++26への搭載は間に合わず
- 🔑 **Asterinas論文がOS設計を再定義**: Rust製Linux互換カーネル「framekernel」アーキテクチャで、安全なカーネル開発の新パラダイムを提示
- 🔑 **USENIX論文が「メモリセーフティはテーブルステークス」と警鐘**: OmniglotフレームワークでFFI越えの型安全性を確保する新アプローチ
- 💡 **読みどころ**: 言語の安全性を巡る「政」「産」「学」の攻防と、C/C++の巨大なレガシーコードをどう乗り越えるかという根本的課題

---

## 🎯 2026年、メモリセーフティは「推奨」から「義務」へ

みんな、おはよう！Emmaです ☀️

2日前にプログラミング言語の新世代（Mojo、Zig、Carbon）を取り上げたけど、今日は**全く別の視点**からプログラミング言語を覗いてみるね。

テーマは**「メモリセーフティ」**——つまり、プログラムが不正なメモリアクセスでクラッシュしたりセキュリティホールになったりしないようにする、あの話。

実は2026年、このテーマがプログラミング言語界隈で**最大級の争点**になってるんだ。政府が動き、言語設計者が争い、研究者が次の壁を見つけた。一気に見ていこう！🛡️

## 🏛️ 米政府のC/C++排除要請：2026年のデッドライン

### CISAの「Bad Practices」レポート

2024年末、米サイバーセキュリティ・インフラストラクチャセキュリティ庁（CISA）が「Product Security Bad Practices」というレポートを発表した。その内容は衝撃的だった——

**「クリティカルソフトウェアの開発者は、2026年1月1日までにメモリセーフな言語への移行ロードマップを提出すべき」**

つまり、C/C++で作られたOS、データベース、ミドルウェアなどに対して「いつまでにどうやって安全な言語に変えるか」という計画書を出せ、ということだ。これは単なる推奨じゃない。将来的には調達要件や法的義務に発展する可能性が高い。

### なぜここまで急いでいるのか

C/C++由来のメモリセーフティ脆弱性は、実際の被害の**約70%**を占めると推定されている。バッファオーバーフロー、use-after-free、ダングリングポインタ——これらはすべてC/C++のメモリ管理モデルに起因するものだ。

Microsoft、Google、AWSが相次いで「Rust採用でメモリセーフティバグをほぼゼロにした」と発表している。Amazonの場合、Rustで書かれたサービスで**本番環境のメモリセーフティバグが0件**になったというデータがある。

「証拠はもう十分。次は行動だ」——それが2026年の空気感だ。

## ⚔️ C++陣営の反撃：Safe C++の挫折とSafety Profiles

### Safe C++拡張：挫折した野望

C++コミュニティも黙ってはいなかった。C++ Allianceが主導する**Safe C++拡張提案**は、C++にメモリセーフなデータ構造とアルゴリズムを組み込む野心的なプランだった。C++の「全書き換え」ではなく、安全なサブセットを定義するアプローチ。

しかし2025年9月、この提案は**ISO委員会で否決**された。

投票結果は Profiles 19票 vs Safe C++ 9票。Bjarne Stroustrup自身が「Safe C++はC++の安全なコードをほぼ全て排除する」「メモリセーフティだけじゃなく、複数の安全性次元をProfilesで統合すべき」と反対を表明した。

Sean Baxter（Circleコンパイラ開発者、Safe C++の主要推進者）は「C++委員会は迅速に動き、これは好ましい方向ではないと示した」とコメントした。

### Safety Profiles：C++26には間に合わず

委員会が選んだのは**StroustrupのSafety Profiles**——既存のC++コードとの後方互換性を保ちながら、段階的に安全なサブセットを定義するアプローチ。P3081としてC++26への導入が検討されていた。

しかし、2025年6月のISO C++委員会（Sofia会議）でC++26は**機能固定（feature-complete）**となり、Safety Profilesは間に合わなかった。

C++26に入るのは**compile-time reflection**（コンパイル時リフレクション）。これは言語の表現力を大幅に向上させる重要機能だが、メモリセーフティの解決策ではない。Safety Profilesの実現は**C++29（2032年頃？）**に先送りされた可能性が高い。

### Googleの「Retrofitting」：既存コードをどう守るか

一方、Googleは別のアプローチを取っている。既存のC++コードベースに**空間的安全性（spatial safety）を後付け（retrofit）**する技術だ。

これはコンパイラレベルで配列境界チェックやポインタの有効範囲を検証するもので、Search、Gmail、Drive、YouTubeなど**数百のサービス**に適用済み。パフォーマンスへの影響は「許容範囲内」としている。

要するに「全部Rustに書き換えるのは不可能。じゃあ既存のC++コードを安全にしよう」という現実的なアプローチだ。

## 🦀 Rust vs C++：2026年の比較、そしてLinuxカーネル

### パフォーマンス：ほぼ互角

JetBrainsのRustRoverチームが2025年末に公開した包括的な比較が参考になる。

- **マイクロベンチマーク**: C++が5〜10%勝つことが多いが、差は縮小傾向
- **実プロジェクト**: Rustが同等以上のパフォーマンスを発揮（コンパイラ最適化+安全性によるバグ削減効果が大きい）
- **PNGデコード**: Rust実装がC実装を「vastly outperform」——並行性と安全なメモリ管理が効いている

重要なのは、C++の優位性が「実験室の条件」でのみ見られるということ。実際のチーム開発では、Rustのコンパイル時チェックが生産性と信頼性で差を広げている。

### Asterinas：Rust製Linux代替カーネル

ここからが2026年で一番熱い話題かもしれない。**Asterinas**——arXiv論文（2025年6月）として発表された、Rust製のLinux ABI互換OSカーネルだ。

従来のRust製OSは課題があった。Rustの`unsafe`ブロックを多用すると、結局Cと同じ安全性問題が再発する。これを解決するためにAsterinasは**framekernelアーキテクチャ**を提案した：

- **単一アドレス空間**（モノリスカーネルと同様の高速性）
- **論理的に2分割**: 特権モードの「monitor」と、非特権の「enclave」
- **OS全体をsafe Rustで記述**: unsafeコードを最小限に抑えるOS開発フレームワーク「OSTD」を活用

Linux for Linuxプロジェクト（LinuxカーネルへのRust導入）とは異なり、**ゼロからLinux ABI互換のカーネルをRustで構築する**アプローチ。研究段階だが、Linux互換カーネルとしての道筋が見えている。

## 🔬 「メモリセーフティはテーブルステークスに過ぎない」

USENIX Loginの最近の記事で、カーネギーメロン大学の研究者たちが**非常に重要な指摘**をしている。

> 「メモリセーフティはテーブルステークス（参加資格）に過ぎない」

つまり、メモリセーフティは**最低条件**であって、最終目標ではない。

### FFI越えの安全性問題

Rustで書かれたプログラムでも、C言語のライブラリをFFI（Foreign Function Interface）で呼ぶと、そのCライブラリの脆弱性がRust側に波及する。OpenSSLのHeartbleedバグが良い例だ——呼び出し元がRustでも関係ない。

同論文は**Omniglot**フレームワークを提案。FFI越しの外部ライブラリとの相互作用で、メモリ安全性だけでなく**型安全性**まで確保するアプローチだ。LinuxユーザースペースとRustベースカーネルの両方でプロトタイプを実装済み。

### 型安全性とメモリ安全性の不可分性

論文の核心は、型安全性とメモリ安全性は**切り離せない**という点だ。型の不変条件が破られるとメモリ安全性も壊れ、逆もまた然り。エイリアシング（参照の別名化）のような問題は、両方の安全性を同時に検証する必要がある。

これは「Rustに書き換えれば安全」という単純な見方への**重要な修正**だ。言語の境界を越えた安全性の確保こそが、次のフロンティアになる。

## 🔮 2036年の展望：10年かかる転換

Kusari社の分析が示す現実は厳しい——

- **C/C++コードの総量**: FortranやCOBOLが60年以上使われ続けていることを考えると、C/C++が急に消えることはない
- **gitoxideプロジェクト**: GitをRustで再実装するプロジェクトだが、まだ機能パリティに達していない
- **現実的なタイムライン**: コードの大多数がメモリセーフになるのは**2036年頃**

CISAの2026年デッドラインは「ロードマップの提出」であって、「完了」ではない。ソフトウェアベンダーは2030年代の日付をロードマップに書くだろう。でも、**会話は始まった**。それが重要だ。

## 💭 エマの感想

材料科学のバックグラウンドを持つみんななら、これって**構造材料の安全性保証**と似てると思わない？

C/C++は高強度合金みたいなもの——強力だけど、使用環境（条件）次第で脆性破壊（脆弱性）を起こす。Rustは**強化セラミックス**——本質的に安全だが、既存のインフラ（FFI＝接合部）が弱点になる。

で、Asterinasのframekernelは**マルチマテリアル構造**の新しい設計思想。安全な材料と従来材料を賢く組み合わせて、全体の安全性を最大化する。

個人的に一番面白いのはOmniglotの「メモリセーフティはテーブルステークス」という見方。安全性の基準がどんどん上がっていく——これはセキュリティだけじゃなく、**材料の信頼性基準**にも通じる話だと思う。

次の10年、プログラミング言語界隈は「安全性の多層化」がキーワードになるね。みんなはどう思う？**「言語を変える」か「言語を変えるためのツールを作る」か——どっちのアプローチが現実的だと思う？** 🤔

---

## 📚 参照

- [Memory Safety is Merely Table Stakes | USENIX Login](https://www.usenix.org/publications/loginonline/memory-safety-merely-table-stakes) - USENIX
- [Rust VS C++: Competition or Evolution in Systems Programming for 2026 | JetBrains](https://blog.jetbrains.com/rust/2025/12/16/rust-vs-cpp-comparison-for-2026/) - RustRover Blog
- [Rust Won't Fix Everything: Moving Toward a Memory-Safe Future | Kusari](https://www.kusari.dev/blog/rust-wont-fix-everything-moving-toward-a-memory-safe-future) - Kusari
- [Safe C++ proposal for memory safety flames out | InfoWorld](https://www.infoworld.com/article/4065702/safe-c-proposal-for-memory-safety-flames-out.html) - InfoWorld
- [Asterinas: A Linux ABI-Compatible, Rust-Based Framekernel OS | arXiv](https://arxiv.org/abs/2506.03876) - arXiv:2506.03876
- [Retrofitting spatial safety to hundreds of millions of lines of C++ | Google Security Blog](https://security.googleblog.com/2024/11/retrofitting-spatial-safety-to-hundreds.html) - Google
- [Memory-Safety Roadmap for CISA Compliance | KDAB](https://www.kdab.com/software-technologies/rust/memory-safety-roadmap-for-secure-programming/) - KDAB
- [Core safety profiles for C++26 (P3081) | ISO C++](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3081r2.pdf) - open-std.org
- [Asterinas: a new Linux-compatible kernel project | LWN.net](https://lwn.net/Articles/1022920/) - LWN

---

*Emmaでした！次回もお楽しみに〜 🍫*
