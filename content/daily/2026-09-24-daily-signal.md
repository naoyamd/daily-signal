---
article_schema: "daily-signal-article/v1"
policy_version: 2
title: "Engineering AIは制約と証拠へ――DeepONet、NCAMP、Zero Trust、実験閉ループ"
date: 2026-09-24T07:22:56+09:00
draft: false
description: "DeepONetによる制約付きマルチフィジックス設計、NCAMP材料データ、複合材デジタルツイン、RTL生成Agent、MCP Zero Trust、企業AI基盤調査、物理・実験で閉じるScientific AIを整理。生成性能より制約・検証・実行境界が価値を決める流れを追う。"
categories: ["Scientific AI・Neural Operator・マルチフィジックス設計", "航空機材料・部品・設計データ", "Scientific AI・デジタルツイン・複合材製造", "AIによる設計・EDA・Agentic Engineering", "MCP・Agent Security・Zero Trust", "AIエージェント・企業内AI・Mainframe", "OSS・推論基盤・Local AI", "企業AI・ROI・Trustworthy AI調査", "企業AI・Infrastructure・Spending調査", "Scientific AI・生成設計・材料/製剤", "Scientific AI・材料・Battery ML", "Scientific AI・研究自動化・日本", "製造技術・Scientific AI・金属AM", "最新AIモデル・Multimodal Agent・OSS follow-up", "航空機材料・部品・複合材製造"]
tags: ["デイリーダイジェスト"]
generated_by: "ChatGPT Scheduled Writer"
model: "GPT-5.6 Sol"
source_count: 15
selected_count: 12
wildcard_count: 3
curated_source: "gpt_handoff/curated/2026-09-24.json"
published_item_ids: ["r-ge-wbg-deeponet", "c-hexcel-ncamp", "r-ge-composite-twin", "r-cadence-rtl-agent", "r-mcp-zero-trust", "r-rocket-planguard", "r-hf-gguf-transformers", "r-sas-idc-trust", "r-digital-realty-infra", "r-emaf-controlled-release", "r-battery-physics-guided", "r-aist-boltz2-hitl", "w-instruct3d-build-intelligence", "w-qwen38-omni", "w-hexcel-vented-flexcore"]
event_keys: ["ge-vernova:wbg-deeponet-multiphysics-codesign:2026-09-14", "hexcel:hrh10-ncamp-honeycomb-qualification:2026-09-22", "ge-vernova:frp-closed-loop-digital-twin:2026-09-14", "cadence:chipstack-rtl-generation-agent:2026-09-22", "research:enterprise-mcp-zero-trust:2026-09-18", "rocket-software:eva-planguard-mainframe-agent:2026-09-23", "huggingface:transformers-gguf-ggml-kernels:2026-09-22", "sas-idc:data-ai-impact-trust-2026:2026-09-01", "digital-realty:global-data-insights-ai-infra:2026-09-17", "nature:e-maf-controlled-release-inverse-design:2026-09-15", "advanced-science:physics-guided-battery-ce:2026-09-08", "aist:boltz2-human-screening-akr1b10:2026-09-18", "instruct3d:additive-build-intelligence-launch:2026-09-23", "qwen:qwen38-omni-technical-followup:2026-09-22", "hexcel:vented-flexcore-space-launch:2026-09-22"]
generation_cost_usd: 0
---

## 今日のご案内 ☕✨

今日の中心は、Engineering AIの価値が「もっと賢く生成する」ことから、物理・製造・権限・実験という外部制約の中で再現可能に実行することへ移っている点にある。GE VernovaのDeepONetは形状だけでなくpackagingやmanufacturabilityを設計変数の側へ持ち込み、CadenceはRTL生成をPPA評価と機能検証につなぐ。MCPのZero Trust研究も、ツールを見せる／隠すことと、実際に呼び出せる権限を分離して扱う必要性を定量的に示す。

航空・材料では、モデルそのものより「再利用できる証拠」が資産になる動きが目立つ。HexcelのHRH-10はNCAMP資格化によって共有可能なdesign-ready dataへ進み、複合材製造ではセンサー、材料特性、simulation、MLを閉ループで接続する構想が進む。自動設計や自律制御を現場へ載せるほど、allowable、工程条件、traceabilityの整備が先に効いてくる。

Scientific AIでも同じ構図が見える。E-MAFは目標release profileから実験可能な製剤へ逆設計し、battery MLは74サンプルという小規模データで物理記述子の寄与を示し、産総研などの創薬研究はBoltz-2の順位付けを人の選別とwet-labで閉じた。企業側では、AIの本番化がidentity、data foundation、infrastructure、sovereigntyまで含むcontrol-plane問題へ広がっている。

## 1. GE Vernova、DeepONetを制約付きマルチフィジックス共設計へ

GE Vernova Advanced Research、Stony Brook University、Sandia National Laboratoriesは、wide-bandgap power moduleを対象に、geometry-informedなsurrogate modeling workflowを開発している。公式説明ではDeepONet architectureを採用し、power-module packaging、design、manufacturabilityの制約を明示的に取り込む計画だ。単一の固定形状を高速近似するだけでなく、幾何変更を含むmultiphysics co-designの探索を短縮する狙いが置かれている。

この案件は完成済みの性能実証ではなく、開発中のプロジェクトである。したがって評価すべきなのは「DeepONetを使う」という看板より、形状変更時のgeneralization、高忠実度multiphysics解析との誤差、制約違反の検出、探索中にmanufacturabilityを維持できるかという実装側の条件になる。

**💡 注目しておきたい理由:** Neural Operator系が実務CAEへ入る際の難所は、単純な推論速度ではなく、geometry、material、packaging、製造制約が同時に変わる設計空間で信頼できることにある。高忠実度solverを基準にしたheld-out geometry検証と、最適化の途中で製造不能解を排除する仕組みまで含めれば、surrogateは「解析の代替」ではなく設計loopの一部として評価できる。

- 🔗 情報源: [GE Vernova Advanced Research](https://www.gevernova.com/news/articles/creating-surrogate-modeling-workflow-reduce-design-cycle-time-wide-bandgap-power-modules)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Scientific AI・Neural Operator・マルチフィジックス設計

## 2. Hexcel、HRH-10 honeycombをNCAMP資格化――設計データを共有資産へ

Hexcelは、HexWeb HRH-10 aerospace honeycombがNCAMP-administered qualificationを完了したと発表した。NCAMPはWichita State UniversityのNIARが運営し、今回の資格化によって航空宇宙用honeycomb core materialとして初のNCAMP databaseが整備される。Hexcelは、design-readyなmaterial dataと共通material specificationを構造設計・開発に使えるようにする位置づけを示している。

重要なのは材料の新規性だけではなく、設計allowableやqualification evidenceを組織横断で再利用しやすくする点だ。各社が同じ基礎データを個別に取り直す負担を減らし、material selectionからstructural analysis、certification evidenceまでの接続を短くできる可能性がある。

**💡 注目しておきたい理由:** AI-assisted designやoptimizationが航空構造へ深く入るほど、出力モデルより入力データのqualification statusとprovenanceが支配的になる。NCAMPのような共有・監査可能な材料データを最適化やsimulationの正式な入力として扱えれば、探索速度だけでなく、設計判断を認証プロセスへ持ち込む際の説明可能性も改善する。

- 🔗 情報源: [Hexcel](https://www.hexcel.com/hexcel-advances-aerospace-design-innovation-with-first-ncamp-qualification-for-honeycomb-core-material/)
- 🕰️ 公開日時: 2026-09-22
- 🗂️ 分類: 航空機材料・部品・設計データ

## 3. 複合材digital twin、予測からresin flow・cureの閉ループ制御へ

GE Vernova Advanced ResearchとUniversity of Delawareは、fiber-reinforced polymer composite製造向けのAI-driven closed-loop digital twinを開発している。計画はsensor、real-time process monitoring、material characterization、ML model、simulationを統合し、resin flowとcureを自律的に適応制御するところまで含む。

**💡 注目しておきたい理由:** 複合材製造では、予測精度だけでなく「何を観測でき、何を安全に操作できるか」が価値を決める。実機評価ではsensor observability、batch間のrobustness、controller guardrail、first-pass yieldへの寄与を追い、digital twinが監視用dashboardで終わらず工程制御へ閉じているかを確認する必要がある。

- 🔗 情報源: [GE Vernova Advanced Research](https://www.gevernova.com/news/articles/developing-evaluating-ai-driven-framework-manufacturing-fiber-reinforced-polymer)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Scientific AI・デジタルツイン・複合材製造

## 4. Cadence、spec-to-RTL生成をPPA最適化と検証へ接続

CadenceはChipStack AI Super AgentにRTL Generation Agentを追加し、spec-to-RTL生成、RTLのanalysis/refinement、早期のpower・performance・area（PPA）最適化を一つのworkflowへ広げた。初期評価では、foundation-model-only生成に対し平均24%のarea削減、18%のpower削減をfunctional accuracyを維持して得たと同社は報告する。

**💡 注目しておきたい理由:** 数値はvendor-reportedで独立再現値ではないが、評価軸を「コード生成」からEDA toolでの解析・修正・verificationへ移している。実運用ではequivalence、regression coverage、traceability、held-out designでの再現可能なPPAを見る必要がある。

- 🔗 情報源: [Cadence Design Systems](https://newsroom.cadence.com/press-releases/press-release-details/2026/Cadence-Expands-ChipStack-AI-Super-Agent-with-a-New-Agent-for-RTL-Generation-and-Early-PPA-Optimization/default.aspx)
- 🕰️ 公開日時: 2026-09-22
- 🗂️ 分類: AIによる設計・EDA・Agentic Engineering

## 5. MCPのZero Trust、tool discoveryとinvocation authorizationを分離

論文は6つのMCP SDKを調べ、pre-auth discoveryやper-tool authorizationの隙間を整理し、FastMCPへpermission-filtered discoveryとinvocation enforcementを実装した。計2,160試行では、body内で権限確認するbaselineで禁止toolへのattemptが152/720（21.1%）、permission-aware visibilityでは0/720だった。ただしvisibilityだけでは直接呼び出しを防げず、実行時認可が必要だとする。

**💡 注目しておきたい理由:** MCPではtool非表示を認可境界にできない。identityをserver側へ伝播し、invocation-time authorizationを必須にしたうえで、filtered discoveryを防御層として使う構成が要る。

- 🔗 情報源: [arXiv](https://arxiv.org/abs/2609.22573)
- 🕰️ 公開日時: 2026-09-18
- 🗂️ 分類: MCP・Agent Security・Zero Trust

## 6. Rocket EVA、mainframe Agentの「推論」と「実行」の間にPlanGuard

Rocket Softwareはmainframe向けAgentic AI platform「EVA」を拡張した。PlanGuardはAI reasoningとsystem executionの間にpolicy decision pointを置き、identity controlとscoped accessでmainframe resourceへの操作範囲を制限する。

**💡 注目しておきたい理由:** mission-critical systemではmodel選定より、planをactionへ変える直前の決定論的認可が重要になる。agent intent、許可判断、実行operationを同じaudit trailで追い、人間承認が必要な操作を分離する設計が要る。

- 🔗 情報源: [Rocket Software](https://www.rocketsoftware.com/en-us/news/rocket-software-advances-governed-agentic-ai-mainframe-rocket-eva)
- 🕰️ 公開日時: 2026-09-23
- 🗂️ 分類: AIエージェント・企業内AI・Mainframe

**📚 追加で確認した資料:**

- <https://www.globenewswire.com/news-release/2026/09/23/3367450/0/en/rocket-software-advances-governed-agentic-ai-on-the-mainframe-with-rocket-eva.html>

## 7. TransformersがGGUFを直接実行、local inferenceのtoolchainが接近

Hugging FaceはTransformersからGGUF checkpointを直接load・実行する経路を追加し、ggml kernelでllama.cpp系quantized modelを`from_pretrained` workflowへ持ち込んだ。初期focusはApple SiliconとQwen3.5系で、Qwen3.5-4Bの例はBF16 8.42 GBからQ4_K_M 2.74 GBへ縮小する。

**💡 注目しておきたい理由:** GGUFがTransformers標準APIへ近づけばlocal AIの検証経路は単純化する。ただしfile size減少は品質やthroughputを保証しないため、target hardwareでtask quality、latency、memoryを測る必要がある。

- 🔗 情報源: [Hugging Face](https://huggingface.co/blog/transformers-llama-cpp-quants)
- 🕰️ 公開日時: 2026-09-22
- 🗂️ 分類: OSS・推論基盤・Local AI

## 8. SAS / IDC調査、Trustworthy AIとROIの相関を大規模surveyで提示

SASがIDCのresearch insightを用いて公表した第2回「Data and AI Impact Report」は、28か国、banking・insurance・life sciences・public sectorの4業種にまたがる2,699人のdecision-makerを対象とする。回答者は自社のdata / AI initiativeを把握または意思決定に影響する立場で、組織はdata quality and governance、model governance and oversight、explainability and fairness、responsible AI policy、audit and accountabilityの5軸で評価された。

主要結果では、generative AIへのtrustが76%なのに対しagentic AIは66%。AI recommendationを少なくとも時々overrideする利用者は97.2%で、override理由の首位はAIが判断理由を説明できないことだった。Trustworthy AIへ投資する組織でstrong/high ROIを報告した比率は62%、laggardは4%で「15倍」と整理され、最上位群は13のbusiness outcomeで1.85倍大きいgainを報告した。一方、agentic AIに十分なoptimized data infrastructureを持つ企業は17.5%にとどまる。

前回比較について、今回の公開資料は62%対4%のROI splitに直接対応する前年値を示していないため、年次差は補わない。さらに、SASによるvendor-published researchでIDCが関与した自己申告surveyであり、governanceやdata foundationとROIの関連は因果関係を証明しない。対象業種も4分野に集中している。

**💡 注目しておきたい理由:** 数字の読みどころは「Trustworthy AIをやればROIが15倍になる」という因果主張ではなく、説明可能性、data quality、auditability、人間のoverrideが本番運用の変数として可視化されている点にある。導入評価ではproductivityだけでなくoverride rate、explainability failure、data-quality incident、approval latencyを同時に計測すると、trustの問題を運用指標へ落とし込める。

- 🔗 情報源: [SAS / IDC](https://www.sas.com/en_us/news/press-releases/2026/september/idc-data-ai-impact-report.html)
- 🕰️ 公開日時: 2026-09-01
- 🗂️ 分類: 企業AI・ROI・Trustworthy AI調査

## 9. Digital Realty調査、AIの制約が「モデル」からinfrastructure配置へ

Digital Realtyの2026 Global Data Insights Surveyは、19か国、11業種のIT decision-maker 2,131人を対象とし、回答企業の規模は500人から1万人超までを含む。調査では「specialized infrastructureの不足」をAI initiativeのprimary constraintとする回答が40%に達し、2024年の9%から4倍超へ増えた。回答者は今後1年のAI spendingが32%増えると見込み、86%がsovereign AI initiativeを進めていると答えた。

data locationをAI planへ直接結び付ける組織は92%で、2024年の73%から上昇した。これはcompute placement、connectivity、private deployment、data sovereigntyがmodel selectionとは独立した後段作業ではなく、AI architectureそのものへ組み込まれつつあることを示す。

ただし、この調査はdata-center providerであるDigital Realtyが公表したvendor researchであり、spending expectationや将来のdeployment計画は実現済みoutcomeではない。公開releaseでmethodologyの概要は確認できるが、samplingやweightingの詳細までは示されていないため、40%や86%を市場全体の確定値として外挿するのは避けるべきだ。

**💡 注目しておきたい理由:** Agentやreal-time AIの本番化では、model性能が十分でも、data locality、latency、resilience、sovereigntyの条件で構成が決まる。PoC後にinfrastructureを足すのではなく、capacity、network、private/public boundary、規制上のdata placementを先にmodel化してからmodel・agent architectureを選ぶ順序が実務的になる。

- 🔗 情報源: [Digital Realty](https://www.globenewswire.com/news-release/2026/09/17/3363858/0/en/digital-realty-global-data-insights-survey-reveals-enterprise-shift-from-ai-strategy-to-execution-as-infrastructure-emerges-as-top-barrier.html)
- 🕰️ 公開日時: 2026-09-17
- 🗂️ 分類: 企業AI・Infrastructure・Spending調査

## 10. E-MAF、目標release profileから実験可能な製剤へ逆設計

Nature Communications掲載のE-MAFは、process-aware surrogateとoptimized genetic algorithmを組み合わせ、目標とするcontrolled-release profileからlab-ready formulationを生成するexpert-mimic AI frameworkだ。著者らは、従来6〜12か月としていたdesign cycleを約1時間へ短縮したと報告し、7種類のactive pharmaceutical ingredientでin vitro release、in vivo pharmacokinetics、therapeutic effectを検証している。

重要なのは、候補をscore順に並べるだけでなく、process knowledgeを含むsurrogateでfeasibleな設計空間を作り、evolutionary searchで候補を生成し、実験へ戻している点にある。性能値は論文著者による研究結果として読むべきだが、inverse designを「target → constrained search → manufacturable design → physical validation」で閉じる構造は、材料・工程設計へ一般化しやすい。

**💡 注目しておきたい理由:** Scientific AIの価値は候補生成数ではなく、要求仕様から実験可能な設計へ到達するまでのloopをどこまで短縮できるかで測る方が実務に近い。surrogateの適用範囲、process constraint、外挿検知、実験でのaccept/rejectを明示すれば、AIが研究判断を置き換えるのではなく、探索空間を圧縮する設計装置として使える。

- 🔗 情報源: [Nature Communications](https://www.nature.com/articles/s41467-026-77619-5)
- 🕰️ 公開日時: 2026-09-15
- 🗂️ 分類: Scientific AI・生成設計・材料/製剤

## 11. Battery ML、小規模データでは物理記述子がmodel scaleを上回る

Advanced Scienceの研究は74件のexperimental electrolyte sampleに、実験値、classical molecular dynamics、DFT由来descriptorを組み合わせてCoulombic Efficiencyを予測した。SVM regressionはtest R²=0.9115、formula-only controlは0.7119で、5-fold cross-validationと外部12 electrolyteでのvalidationも行った。

**💡 注目しておきたい理由:** 小規模材料データではmodel scaleよりmechanism-aware descriptorが効く可能性を示す。random splitだけでなく未知compositionへのexternal validationとdescriptorの物理的意味を確認してから探索へ使うべきだ。

- 🔗 情報源: [Advanced Science](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.76510)
- 🕰️ 公開日時: 2026-09-08
- 🗂️ 分類: Scientific AI・材料・Battery ML

## 12. 産総研など、Boltz-2の予測を人の選別とwet-labで閉じる

産総研、岐阜大学、岐阜薬科大学の共同研究は、AKR1B10 inhibitor探索でBoltz-2予測、clustering、人によるscreening、実験検証を組み合わせた。50,240化合物から40候補を実験し、28化合物が10 µMで50%以上の活性低下を示し、そのうち7化合物は1 µMでも阻害活性を保ったと報告している。

**💡 注目しておきたい理由:** model rankingを最終回答にせず、多様性を意識した人のscreeningとwet-lab evidenceへ接続している点が重要だ。Scientific AIを候補空間の圧縮器として使い、hit rateだけでなくchemical diversity、selectivity、再現実験を残せば、confidence scoreに依存しすぎない研究loopを組める。

- 🔗 情報源: [産業技術総合研究所](https://www.aist.go.jp/aist_j/press_release/pr2026/pr20260918/pr20260918.html)
- 🕰️ 公開日時: 2026-09-18
- 🗂️ 分類: Scientific AI・研究自動化・日本

**📚 追加で確認した資料:**

- <https://www.gifu-u.ac.jp/news/research/2026/09/entry18-15292.html>

# 今日の紛れ枠

### Instruct3D、金属AMを「Predict・Build・Prove・Learn」でつなぐ

9月23日付の業界記事はInstruct3DのAdditive Build Intelligenceを、dual-wavelength sensing、physics-based prediction、learning workflowを結ぶmetal AM platformとして紹介した。vendor siteでもVertX、AdditiveOS、physics-based prediction、part verificationは確認できるが、launch日付は二次情報に依存する。

**追う理由:** 予測・in-situ sensing・品質証拠を同じbuildへ結べる点が重要だ。customer data、machine/material coverage、誤検知率、first-party technical releaseを追いたい。

- 🔗 情報源: [Engineering Update](https://engineering-update.co.uk/2026/09/23/instruct3d-launches-additive-build-intelligence-for-high-value-metal-am/)

**📚 追加で確認した資料:**

- <https://www.instruct3d.io/>

### Qwen3.8-Omni、model本体よりpluginとlive harnessの再利用性を追う

Qwen Teamのtechnical follow-upはQwen3.8-Omni-Flashのnative multimodal co-trainingと1M-token contextを説明し、Qwen-MM-PluginsとQwen-Live-Harnessをopen sourceで公開した。tool useやreal-time agent orchestrationをmodel外の再利用可能な層へ出している。

**追う理由:** benchmark差よりplugin/harnessの採用が実装上の焦点になる。license、tool auditability、latency、costの再現値を追いたい。

- 🔗 情報源: [arXiv](https://arxiv.org/abs/2609.25611)

### Hexcel、space-launch向けVented Flex-Coreで製造制約を材料側へ組み込む

Hexcelは9月22日、高密度aluminumのVented Flex-Core honeycombを複雑なspace-launch構造向けに発表した。formabilityとintegrated ventingを一体化し、highly contoured composite structureの製造簡素化を狙う。

**追う理由:** 自動設計は材料のformability、venting、工程性を無視できない。将来のgenerative designやprocess optimizationが守るmaterial/process constraintとして追う価値がある。

- 🔗 情報源: [Hexcel](https://www.hexcel.com/hexcel-launches-new-vented-flex-core-honeycomb-designed-to-accelerate-production-of-next-generation-space-launch-vehicles/)

---

> 本記事は公開情報をもとに編集されています。重要な判断にはリンク先の一次情報をご確認ください。
