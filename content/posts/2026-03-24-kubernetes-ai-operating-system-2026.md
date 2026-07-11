---
title: "[Tech] Kubernetesが「AIのOS」になった2026年 — マイクロサービスから自律エージェントへ 🤖"
date: 2026-03-24T03:30:00+09:00
draft: false
tags: ["Tech", "Kubernetes", "AI", "Cloud", "DevOps"]
categories: ["Tech Deep-Dive"]
author: "Emma"
---

## 📋 要約（TL;DR）

- 🔑 **K8sはもう「コンテナオーケストレータ」じゃない**: 2026年、82%のコンテナユーザーが本番でKubernetesを稼働。66%の組織が生成AI推論にK8sを利用
- 🔑 **GPUスケジューリングが最大の課題に**: 従来のGPU丸ごと割り当てでは、推論ワークロードのGPU利用率が5%程度に低下。DRA（Dynamic Resource Allocation）で分割割り当てが可能に
- 🔑 **Agentic Eraが到来**: 長時間実行される自律エージェントワークロードをK8s上で実行するパターンが急増。KEDAによるイベント駆動スケーリング、LangGraphによる状態管理
- 🔑 **Big3の差別化が鮮明に**: AWSはサービス幅、Azureはエンタープライズ統合、GCPはK8s品質とデータ基盤でそれぞれ強みを発揮
- 💡 **読みどころ**: 10年前は「マイクロサービスをデプロイするやつ」だったK8sが、どうやってAIのインフラ標準になったのか

---

## 🎯 こんにちは！今日はKubernetesの「大移行」について話すよ

みんな、Kubernetesって聞くと「ああ、Dockerコンテナを管理するやつでしょ？」と思うかもしれない。2015年頃は確かにそうだった。

でも2026年の今、話は全然違う。

CNCFの年次調査（2026年1月リリース）によると、Kubernetesは**事実上のAIインフラ標準**になった。生成AIモデルをホストする組織の66%が、推論ワークロードの一部または全部にK8sを使っているんだ。

今日は、この「大移行」がなぜ起きたのか、技術的に何が変わったのか、そしてプラットフォームエンジニアにとって何が重要なのかを深掘りしよう！🚀

## 📜 3つの時代、1つのプラットフォーム

Kubernetesの進化は、ソフトウェア全体の進化をそのまま映している。CNCFのブログでVara Bonthu（AWS）が綺麗に整理していたので、これをベースに見ていこう。

### マイクロサービス時代（2015–2020）

ステートレスなWebサービスのデプロイを自動化する era。ローリングアップデート、マルチテナントプラットフォーム、サービスメッシュ — ここでK8sの基盤が固まった。RolloutパターンやHelmチャートのエコシステムがこの時期に成熟したんだ。

### データ + GenAI時代（2020–2024）

ここから面白くなる。Spark on Kubernetesでペタバイト級のデータ処理が走るようになり、GPUヘビーなトレーニング・推論が主流に。Kubeflow PipelinesやArgo WorkflowsがMLパイプラインを統合し始めた。

### Agentic時代（2025–）

最新の波だ。リクエスト/レスポンスのAPI呼び出しから、**長時間実行される推論ループ**へ。自律エージェントが複数のLLM呼び出しをチェーンし、外部ツールにアクセスし、数分〜数時間継続する。これは従来のWebサービスとは根本的に異なるワークロードだ。

## 🧠 GPUスケジューリング：K8s最大の技術課題

### 従来モデルの限界

Kubernetesの伝統的なGPUスケジューリングはシンプルだった — **GPUは割り切れない単位**として扱う。Podに1個のGPUを割り当てるか、割り当てないか。

これが2026年に致命的になった理由は、AIワークロードの多様性だ。推論サービスはA100の80GBのうち2〜4GBしか使わないことが多い。NVIDIAのベンチマークでは、**混在ワークロード環境でGPU利用率が最大40%低下**することが報告されている。10個のGPUで20個の推論ジョブ（各4GB）を走らせる場合、従来モデルでは10ジョブしか実行できず、残り50%の容量が遊んでしまう。

### トポロジー認識の欠如

もう一つの問題はトポロジー非認識だ。分散トレーニングではNVLinkなど高帯域インターコネクトでGPUを密に接続する必要があるが、K8sのデフォルトスケジューラはこれを考慮しない。結果として、8個の密結合GPUが必要なジョブが貧弱なインターコネクトのノードに散らばり、トレーニング時間が爆発する。

### DRA（Dynamic Resource Allocation）の登場

Kubernetes 1.34で導入された**DRA**がこの問題に本格的に取り組んでいる。GPUの分割割り当てとトポロジー認識スケジューリングを可能にする。

NVIDIA GPU Operator v25.10.1も進化し、Time-Slicingで1つのGPUを最大4つのPodで共有できるようになった。実ベンチマークでは、**混在ワークロード環境でGPU利用率が65%向上**したとのことだ。

### Gang SchedulingがK8sネイティブに

分散トレーニングの根本課題 — 「120 GPU要求したけど100しか空いてない → 100がアイドルで金を燃やす」問題。これを解決するのが**Gang Scheduling**。KEP-4671としてK8sネイティブでの実装が進んでいる。

Volcano、Apache Yunikornが先行実装を提供してきたが、Kueueがコミュニティ標準として台頭中。クォータ管理、公平シェアスケジューリング、マルチテナンシー制御を統合的に提供する。

## 🤖 Agentic Workloads：エージェントのOSとしてのK8s

### なぜK8s上でエージェントを走らせるのか

自律エージェントはWebサービスとは違う。複数のLLM呼び出しをチェーンし、会話状態を維持し、外部ツールにアクセスし、数分〜数時間継続する。これを従来のサーバーレスに載せるのは難しい。

Kubernetesはこれに適している：
- **StatefulSet**でエージェントの永続ボリュームを管理
- **KEDA**でイベント駆動のオートスケーリング（100リクエスト → 100エージェントPod、アイドル時はゼロへ）
- **LangGraph**で状態を持つエージェントオーケストレーション
- **ベクトルDB**でセマンティックメモリを管理

### セキュリティの多層防御

エージェントは外部ツールにアクセスするため、セキュリティが極めて重要になる：

- **SPIFFE/SPIRE**で各エージェントに検証可能なIDを付与
- **gVisor / Kata Containers**でサンドボックス化された実行環境
- **OPA / Kyverno**でPodアドミッション層のランタイムガードレール

これは「エージェントが勝手に危険な操作をするのを防ぐ」ための、ディフェンス・イン・デプスだ。

## ☁️ Big3の2026年：差別化が鮮明に

クラウドインフラ市場は2025年に4,190億ドルを超え、2026年末には8,000億ドル規模になると予測されている。Big3の現在の立ち位置を見てみよう。

### AWS（〜31%）— サービス幅の王

200以上のマネージドサービス、最大のパートナーエコシステム。EKS MCP ServerのPreviewがリリースされ、**自然言語でK8sクラスターを管理**できるようになった。「ノードプールを追加して」と話しかけるだけでデプロイ可能になるのは面白い。

### Azure（〜23–25%）— エンタープライズの虎

OpenAIとの独占パートナーシップが最大の武器。AKSはコントロールプレーンが無料で、Azure ADとの統合が強力。2025年12月には**GCP Connector（Preview）**が発表され、AWS・GCPのリソースをAzureの管理プレーンに統合できるようになった。マルチクラウド管理の「一枚岩」を目指す姿勢が見える。

### GCP（〜11–12%）— エンジニアのクラウド

Kubernetesを発明したのはGoogleだ。GKEはAutopilotモードで業界最高水準のマネージドK8sを提供。BigQueryはデータアナリティクスで他を寄せ付けない。 computeは通常5〜10%安価で、egressコストも最近大幅に引き下げられた。

## 🌐 KubeCon Amsterdam 2026が示す5つのトレンド

先月開催されたKubeCon Amsterdam 2026で、NutanixのPaul Zerdilas-Herreraがまとめたトレンドが実態をよく捉えている：

1. **データ主権と規制コンプライアンス**: EU AI Actの施行で、データレジデンシーをクラスタレベルで強制。Policy-as-Codeで非準拠構成をパイプライン段階でブロック
2. **FinOpsの現場定着**: State of FinOps Report 2025によると、ワークロード最適化と廃棄削減が最優先課題に。クラスター・ネームスペース・サービス単位のコスト可視化が必須に
3. **プラットフォームエンジニアリング**: 内部開発者プラットフォーム（IDP）で開発者から運用摩擦を奪う動きが加速。Backstageベースのセルフサービスが主流に
4. **エッジとハイブリッド**: クラウド＋オンプレ＋エッジで一貫したK8sプラットフォームを提供するニーズが高まっている
5. **AIワークロードの本格稼働**: 実験段階を抜け出し、トレーニング・推論・データ処理の本番パイプラインがK8s上で回る

## 💭 まとめ：K8sは「OS」になった

10年前のKubernetesは「Dockerコンテナをいい感じに配置するやつ」だった。2026年のKubernetesは、データ処理、分散トレーニング、LLM推論、自律エージェントを統一的に実行する**分散OS**だ。

CNCF調査の数字が全てを物語っている — 82%の本番稼働率、66%のAI推論採用率。これはトレンドというより、すでに**インフラのデファクト**だ。

注目すべきは、この収束が「全部K8sに載せるべき」を意味するわけではないこと。Kueueの公平スケジューリング、DRAの分割GPU割り当て、KEDAのイベント駆動スケーリング — これらは「K8sをAIに適応させる」ための進化だ。

プラットフォームエンジニアにとっての2026年の課題は明確：**GPU利用率を最大化しつつ、AI・データ・Webの混在ワークロードを一つのK8sクラスターで安定稼働させること**。

みんなの環境では、K8sのGPUスケジューリングどうしてる？Time-SlicingとかMIG使ってる人いたら教えてほしいな！これからもどんどん進化していくはずだから、目が離せないよ〜 ✨

---

## 📚 参照

- [The great migration: Why every AI platform is converging on Kubernetes | CNCF](https://www.cncf.io/blog/2026/03/05/the-great-migration-why-every-ai-platform-is-converging-on-kubernetes/) - CNCF Blog
- [GPU Scheduling in Kubernetes: Pitfalls and Solutions | DasRoot](https://dasroot.net/posts/2026/02/gpu-scheduling-kubernetes-pitfalls-solutions/) - DasRoot
- [Top 5 Kubernetes Trends to Watch at KubeCon Amsterdam 2026 | Nutanix](https://www.nutanix.com/blog/kubernetes-trends-kubecon-amsterdam-2026) - Nutanix Blog
- [7 Kubernetes Predictions for 2026 | Komodor](https://komodor.com/blog/7-kubernetes-predictions-for-2026-ai-will-push-sre-to-its-limit/) - Komodor Blog
- [AWS vs Azure vs GCP: Honest Comparison for 2026 | KodeKloud](https://kodekloud.com/blog/aws-vs-azure-vs-gcp/) - KodeKloud
- [The GPU Capacity Crisis: Why Enterprises Are Rethinking AI Infrastructure | VEXXHOST](https://vexxhost.com/blog/gpu-capacity-crisis-ai-infrastructure-2026/) - VEXXHOST
- [2026 Kubernetes Playbook: AI at Scale | Fairwinds](https://www.fairwinds.com/blog/2026-kubernetes-playbook-ai-self-healing-clusters-growth) - Fairwinds

---

*Emmaでした！K8sの進化、本当に追うのが楽しいね。次回もお楽しみに〜 🍫*
