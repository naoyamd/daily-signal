---
article_schema: "daily-signal-article/v1"
policy_version: 2
title: "AI実装は「検証できる実行」へ――数値parity、Virtual First Flight、複合検査、Agent統治"
date: 2026-09-15T07:20:38+09:00
draft: false
description: "科学コードの数値parity、A350FのVirtual First Flight、航空エンジン製造の3D+2D+AI検査、材料データ抽出、長期Agentと企業ガバナンスを整理。AIの価値がモデル性能から、検証・実行・統制をつなぐ仕組みへ移る動きを追う。"
categories: ["AIエージェント・コーディング・Scientific Software", "民間・軍用航空機", "航空機エンジン", "Industrial AI・Scientific AI", "Scientific AI・材料インフォマティクス", "CAD・CAE", "企業AI・ガバナンス調査", "AIエージェント・企業AI", "企業AI・製造・データ基盤", "企業AI・支出調査", "HPC/GPU・推論基盤", "オープンウェイト・コーディングエージェント", "Scientific AI・機械システム", "Edge AI・AIハードウェア"]
tags: ["デイリーダイジェスト"]
generated_by: "ChatGPT Scheduled Writer"
model: "GPT-5.6 Sol"
source_count: 14
selected_count: 11
wildcard_count: 3
curated_source: "gpt_handoff/curated/2026-09-15.json"
published_item_ids: ["r-mistral-legacy", "c-airbus-a350f-vff", "c-aecc-ai-inspection", "r-lg-expert-ai", "r-concrete-llm", "c-lumafield-saturn", "r-onetrust-governance", "r-salesforce-longhorizon", "r-fujitsu-palantir", "r-futurum-overrun", "r-fujitsu-monaka", "w-bolt-forge", "w-vibration-benchmark", "w-mos2-tokenizer"]
event_keys: ["mistral:legacy-code-agent-modernization:2026-09-09", "airbus:a350f-virtual-first-flight:2026-09-14", "aecc-dongan:3d-2d-ai-inspection:2026-09-04", "lg-ai-research:expert-ai-manufacturing-science:2026-09-14", "npj-comp-mat:llm-concrete-data-extraction:2026-09-14", "lumafield:saturn-large-format-ct:2026-09-10", "onetrust:ai-ready-governance-survey-2026:2026-09-14", "salesforce:agentforce-long-horizon-runtime:2026-09-14", "fujitsu-palantir:global-fde-manufacturing-supplychain:2026-09-10", "futurum:2h2026-ai-budget-overrun-survey:2026-09-10", "fujitsu:monaka-sovereign-ai-server:2026-09-14", "bolt:forge-open-model-coding-agent:2026-09-14", "scientific-data:vibration-ai-mechanical-benchmark:2026-09-14", "nature-electronics:mos2-light-to-token:2026-09-14"]
generation_cost_usd: 0
---

## 今日のご案内 ☕✨

今日の中心は、AIを「賢い出力器」として導入するだけでは足りず、結果を検証できる実行系として組み込む設計が前面に出てきたことだ。Mistralの科学コード移行では、Fortran 77からC++へ書き換える前に数値parity harnessを作り、最終出力だけでなく中間状態まで照合した。AirbusのA350F Virtual First Flightも、simulationを単独で回すのではなく実機avionics benchへ接続し、失敗シナリオと認証試験計画へつなげている。

製造側でも、AECC Donganは3D scanだけでは拾いにくい狭所の小部品を2D visionとAIへ振り分け、Lumafieldは大型CTの内部欠陥・寸法情報をCAD比較やGD&T確認へつなぐ。Scientific AIでは、材料文献から構造化データを作るLLM pipelineや、LG AI Researchの材料設計・自律実験の方向性が、モデルを研究・品質保証の実務loopへ組み込む動きを示している。

企業Agentも同じく「動けること」だけでは不十分だ。Salesforceは日単位・週単位の長期実行、永続状態、承認境界を前面に出し、OneTrustの調査ではAgent利用を奨励する組織が87%に達する一方、明確な統制を持つのは47%にとどまった。AI予算の超過も広がっており、導入競争の焦点はモデル選定から、検証、権限、データ、運用費を含む実行アーキテクチャへ移っている。

## 1. Mistral、科学コード移行で「翻訳」より数値parityを先に置く

Mistral AIは、物理計算を含む約30万行のFortran 77製reservoir simulatorのうち、最初のsprintで4万行をC++へ移行した事例を公開した。重要なのは、Agentにコードを書かせる前に、legacy側の最終結果と重要な中間状態を出力し、C++側で同じcheckpointを比較できるnumerical-parity harnessを構築した点だ。さらにcaller-callee treeを解析し、100体超のAgentで文書化を進めた。

完全自律でsubroutineごとに翻訳させた最初の試行では、動作はしてもCOMMON blockやGOTO構造をほぼそのまま持ち込むなど、modernizationとしては不十分だったという。最終的にはcoder、tester、reviewerを組み合わせ、人間がarchitecture reviewとmerge境界を担うworkflowへ落ち着いた。これは提供元の事例報告だが、「正しいコード」を自然言語評価ではなく数値一致で判定した点は再現性が高い。

**💡 注目しておきたい理由:** Scientific softwareやCFD/FEAの更新では、Agentの推論品質より先に「何を満たせば移行完了か」を機械的に判定できる境界が必要になる。既存solverのstate checkpoint、regression test、許容誤差を先に整備し、人間承認をarchitectureとmergeへ集中させる方が、全面自律化より現実的な導入設計になる。

- 🔗 情報源: [Mistral AI](https://mistral.ai/news/legacy-code-modernization/)
- 🕰️ 公開日時: 2026-09-09
- 🗂️ 分類: AIエージェント・コーディング・Scientific Software

## 2. Airbus A350F、Virtual First Flightを実機avionicsと認証計画へ接続

AirbusはA350Fの初飛行前に、1回約5時間のVirtual First Flightを13 session実施している。development flight-test simulatorは実際のflight controlやdigital engine controlを含むaircraft avionics test benchへ接続され、system failureの組み合わせ、flight control law、crew procedureを確認する。Airbusはこの構成を実機に対して約90% representativeと説明し、残る大きな不確定要素をfreighter固有のaerodynamic modelとしている。

A350FはA350-900相当の前部fuselageとA350-1000相当の後部・wingを組み合わせるため、既存A350の派生だからといって飛行試験を省けない。計画では2機で約400 flight hoursを実施し、EASAはflight-test planの監視・承認に加え、performance flightへ直接参加する予定だ。simulation、hardware bench、実飛行、regulatorの証拠連鎖が明示されている。

**💡 注目しておきたい理由:** 高忠実度simulationの価値は、単に実機へ「似ている」ことではなく、どの部分が検証済みで、何が未検証で、次の物理試験へどう受け渡すかを追跡できることにある。Engineering AIやdigital threadでも、model fidelityとcertification evidenceを分け、hardware・failure case・formal acceptance planへ紐付ける設計が重要になる。

- 🔗 情報源: [Airbus](https://www.airbus.com/en/newsroom/stories/2026-09-countdown-to-a350f-first-flight-preparing-for-the-sky)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: 民間・軍用航空機

## 3. AECC Dongan、3Dだけで解けない検査を2D+AIへ振り分ける

AECC Harbin Dongan Engineは、engine production lineへ導入した自動3D scanning systemを寸法検査に使い、10種類超の製品でreverse modelingと3D database構築も進めた。一方、狭い組立位置にある小型lock-tabでは3D scanの誤検出・見逃しが発生し、同社報告では認識精度が約75%にとどまった。

そこで小部品の局所検査を2D visual measurementへ切り替え、AI training機能を組み合わせた。1か月超の光源、位置決め、program調整を経て、同社は認識精度100%へ到達したと報告している。最終workflowは「3Dで全体、2D+AIで細部」を見る複合構成であり、100%という値は提供元のsite内評価として扱う必要がある。

**💡 注目しておきたい理由:** 工業検査では単一sensorや単一AIに全問題を押し込むより、geometry、visibility、feature sizeに応じて測定modalityを分担させる方が堅牢になりやすい。全体寸法とreverse-engineering記録は3Dで保持し、局所的な難所だけを2D+AIへroutingする設計は、traceabilityを残しつつ自動化範囲を広げる実務的な形である。

- 🔗 情報源: [AECC Harbin Dongan Engine](https://hde.aecc.cn/hde/xwzx/yxdt/2026090414044588813/index.html)
- 🕰️ 公開日時: 2026-09-04
- 🗂️ 分類: 航空機エンジン

## 4. LG AI Research、製造・科学・金融を分けた「Expert AI」へ

LG AI Researchは9月14日、製造・科学・金融に特化したExpert AI群を公開した。製造ではEXAONE Tabularと自律検査向けOmni Inspect、科学では材料設計と合成結果予測を扱うEXAONE Discoveryを示し、材料探索をrobotic experimentへ接続する自律実験系も掲げた。同社はbattery予測、defect screening、材料計画、drug discoveryなど100件超のindustrial challengeへ適用したとしているが、これは企業側の集計である。

**💡 注目しておきたい理由:** 製造・材料R&Dでは汎用LLMのscoreより、少量のsite dataで状態を予測できるか、検査条件が変わっても再学習を抑えられるか、実験提案を物理装置まで閉ループ化できるかが差になる。評価軸も一般benchmarkからdomain baseline、実験効率、品質保証へ移す必要がある。

- 🔗 情報源: [LG AI Research](https://lg.co.kr/media/release/30563)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Industrial AI・Scientific AI

**📚 追加で確認した資料:**

- <https://www.koreaherald.com/article/10872720>
- <https://www.koreajoongangdaily.com/business/lg-ai-discovers-hairloss-treatment-material-in-a-day-eyes-manufacturing-next/12874717>

## 5. LLMで材料文献を「読める文章」から「使えるdatabase」へ

npj Computational Materialsの研究は、concrete materialsを例に論文からcomposition・process・propertyを構造化するLLM pipelineを示した。著者らはF1最大0.98、2万7,000件超のpublicationから約9,000 record・100属性超を1時間未満で抽出したと報告する。公開databaseは8,979 recordで7,500件超が人手確認済み、評価用benchmarkも3,015 recordを公開している。著者全員は関連provisional patentの発明者である。

**💡 注目しておきたい理由:** Materials AIではmodel以前に、実験値が論文へ閉じ込められていることがボトルネックになる。LLM extractionを使う場合もsource DOIへのprovenance、human-audited benchmark、missing valueを維持し、下流modelへ流す前の品質管理が必要になる。

- 🔗 情報源: [npj Computational Materials](https://www.nature.com/articles/s41524-026-02304-6)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Scientific AI・材料インフォマティクス

**📚 追加で確認した資料:**

- <https://zenodo.org/records/18080351>
- <https://zenodo.org/records/22132837>

## 6. Lumafield Saturn、大型CTをNDIからCAD比較・寸法評価までつなぐ

Lumafieldはlarge-format industrial CT「Saturn」を公開した。scan volumeは直径580 mm×高さ1,100 mm、sourceは225 kVで、同社は条件次第でlight metal最大100 mm、steel/iron最大25 mmのpenetrationを示す。Voyagerではporosity、wall thickness、CAD comparisonに加え、distance・flatness・diameter・profileを抽出し、GD&T確認まで同じscanで扱える。

**💡 注目しておきたい理由:** 大型航空部品ではCTをdefect detectionだけでなく、内部欠陥、wall thickness、CAD deviation、dimensionを共通dataへ載せる方がfeedback価値が高い。penetration capabilityは材質・形状・resolutionに依存するvendor specificationとして扱う必要がある。

- 🔗 情報源: [Lumafield](https://www.lumafield.com/article/introducing-saturn-large-format-ct-for-the-parts-you-couldnt-scan-before)
- 🕰️ 公開日時: 2026-09-10
- 🗂️ 分類: CAD・CAE

## 7. OneTrust調査、Agent利用87%に対し明確な統制は47%

OneTrustとSapio Researchは、2026年6〜7月に8市場のsenior business decision-maker 1,200人を対象にAI governance調査を実施した。対象はCPO、CDO、CISO、CMOを均等に含み、全員がannual revenue 1億ドル以上の組織に所属する。地域はAustralia、Canada、France、Germany、Singapore、Spain、United Kingdom、United Statesである。

調査では87%が組織としてAI Agent利用を奨励している一方、明確なgovernance、oversight、controlがあるとしたのは47%。AI lifecycle全体でcoordinationとaccountabilityが明確と答えたのは5%にとどまり、sanctioned/unsanctioned双方のAI利用を明確に把握できるとの回答も48%だった。さらに86%が過去1年に少なくとも1件のAI-related incidentを経験したとし、そのうち45%がformal review/approval processを導入したとしている。

前年度と直接比較できる同一系列は公開ページに示されておらず、2026年のcross-sectional baselineとして読むのが適切だ。また、governance software vendorが発行する自己申告surveyであり、incidentやmaturityの定義は回答者間で揺れ得る。

**💡 注目しておきたい理由:** Agent adoptionの速度に対して、誰が承認し、何を監視し、どこまで見えるかの運用設計が追いついていない。enterprise deploymentでは利用率をKPIにするだけでなく、unsanctioned use visibility、approval coverage、incident response、lifecycle ownershipを同時に計測しないと、普及そのものがcontrol gapを拡大し得る。

- 🔗 情報源: [OneTrust / Sapio Research](https://www.onetrust.com/resources/onetrust-2026-ai-ready-governance-report/)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: 企業AI・ガバナンス調査

## 8. Salesforce、Agentを「一問一答」から数日・数週間の実行へ

SalesforceはAgentforce向けに、goalをdays/weeks単位で維持するlong-horizon runtimeを発表した。Memory、durable execution、dynamic steeringを組み合わせ、どこまで自律実行し、どこでseller approvalを要求するかもguardrailとして持つ。Multi-Agent OrchestrationはGA、Agent Optimizerは2026年10月GA予定で、未提供機能を含み得るとの注意書きもある。

**💡 注目しておきたい理由:** 長期Agentの難しさはmemory容量より、状況変化時のresume、approval escalation、trace、specialized agent間handoffにある。PoCも単発task successだけでなく、数日間のinterrupt/restart、承認待ち、state consistencyまで試す必要がある。

- 🔗 情報源: [Salesforce](https://www.salesforce.com/ap/news/press-releases/2026/09/14/ph-salesforce-expands-agentforce-with-a-new-portfolio-of-ai-agents-built-for-high-value-work/)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: AIエージェント・企業AI

## 9. Fujitsu×Palantir、3,000 suppliers・18 factories規模でgoverned AIを実装

FujitsuとPalantirはpartnershipを拡大し、FujitsuはPalantir AIP/FoundryのGlobal FDE Partnerとして体制を強化する。日本のmanufacturing use caseでは3,000超のsupplier、18 factoryのdataを統合し、access control、audit、customer-controlled deploymentを組み込んだ。Fujitsuは1年で1,000万ドル超のcost saving、productivity 2倍を報告するが、顧客非公開のcase studyである。

**💡 注目しておきたい理由:** 大規模製造AIではmodelより、supplier・factory間のdata、権限継承、現場で改善を回す人材が導入コストを決める。ontology/data harmonization、access control、FDE capacityをworkstreamとして見積もる必要がある。

- 🔗 情報源: [Fujitsu / Palantir](https://global.fujitsu/en-global/pr/news/2026/09/10-01)
- 🕰️ 公開日時: 2026-09-10
- 🗂️ 分類: 企業AI・製造・データ基盤

## 10. Futurum調査、46.9%がAI支出を計画超過と回答

The Futurum Groupは2H 2026 CIO & Technology Buyers surveyとして、global enterprise technology decision-maker 1,636人の結果を公表した。46.9%がAI spendはbudget planを上回ると回答し、下回ったのは5.6%、formal AI budget自体がない回答も10.0%だった。公開releaseでは詳細なsampling frame、weighting、fieldwork dateまでは示されていない。

計画超過の767組織では47.6%が追加予算を求め、43.3%がoverrunを吸収し後で調整、17.2%がinitiativeをpauseまたは縮小すると回答した。IT budget内で組み替える297組織では60.9%が外部contractor/consultantを最初の削減対象としている。過去waveとの直接比較値は公開されておらず、2H 2026のsnapshotとして扱うべきである。

この調査はcommercial research providerによる自己申告surveyであり、response rateや国別構成などは公開ページから確認できない。それでも、AI費用が単なるAPI単価ではなく、外部人材費や他business-unit budgetの再配分まで含む経営課題になっていることは読み取れる。

**💡 注目しておきたい理由:** AI usageが増えた後にcost governanceを足すと、超過分が別予算の削減で見えなくなり、ROIを正しく測れない。導入時点からbudget owner、unit-cost telemetry、利用量に対するstop/scale criteriaを持たせ、tokenやinferenceだけでなく人員・integration・supportまで含む総費用で管理する必要がある。

- 🔗 情報源: [The Futurum Group](https://futurumgroup.com/press-release/46-9-of-enterprises-report-ai-spend-over-budget-in-2h-2026/)
- 🕰️ 公開日時: 2026-09-10
- 🗂️ 分類: 企業AI・支出調査

## 11. FUJITSU-MONAKA、sovereign AIをCPU・国内製造・traceabilityまで広げる

Fujitsuは「FUJITSU-MONAKA」とMONAKA Serverを発表し、2026年11月からglobal salesを開始する。MONAKAは日本開発の2nm・3D-stacked CPU、serverも国内設計・製造とし、AI inference、enterprise、HPCを対象にtraceabilityとsupply-chain transparencyを訴求する。同社は他CPU比でinference throughput 2倍、必要server数と電力半減を主張するが、独立benchmarkではない。

**💡 注目しておきたい理由:** inference基盤はthroughputだけでなく、power/cooling、server density、製造地、supply-chain traceability、運用地域を同じ比較表へ載せる必要がある。regulated workloadでは「誰が作り、どこで運用し、部品経路を追えるか」もarchitecture要件になる。

- 🔗 情報源: [Fujitsu](https://www.prnewswire.com/news-releases/fujitsu-launches-made-in-japan-next-generation-cpu-fujitsu-monaka-and-fujitsu-monaka-server-for-sovereign-ai-infrastructure-302877394.html)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: HPC/GPU・推論基盤

# 今日の紛れ枠

### Bolt Forge、open coding agentの利用dataを次のmodel学習へ戻す

Bolt.newはopen modelだけを使うcoding agent「Forge」をresearch previewとして公開した。Forgeではopt-inしたanonymized build sessionをArcee AIと共有し、将来のopen-weight model学習へ使う。通常のStandard/Max agentは学習対象外としている。

**追う理由:** production coding interactionをmodel改善へ戻すflywheelは強力だが、source codeを含むsession dataのconsent、anonymization、governanceが成立することが前提になる。

- 🔗 情報源: [Bolt.new](https://bolt.new/blog/what-is-bolt-forge)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: オープンウェイト・コーディングエージェント

### 7,000件の振動signal、単一bearingではない故障伝播benchmark

Scientific Dataはmodular mechanical transmission systemから取得した7,000 vibration signalを公開した。gear、V-belt、roller chainのhealthy/faulty stateとmodule間のfault propagationを含み、unsupervised baselineでは低いclustering accuracyとlabel alignmentが報告されている。

**追う理由:** condition monitoringではisolated componentのdatasetより、load、configuration、連成故障が変わる環境でrepresentationを再利用できるかが重要になる。

- 🔗 情報源: [Scientific Data](https://www.nature.com/articles/s41597-026-07435-5)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Scientific AI・機械システム

### MoS2 sensorで光をtokenへ、前処理のdata movementを減らす

Nature Electronicsは、32×32のMoS2 phototransistor arrayとFPGA peripheral circuitでlight detection、patching、vector encodingをanalogue domain処理する研究を紹介した。modified CIFAR-10で87.3% accuracy、digital tokenizer比14倍超のenergy reductionが報告されている。

**追う理由:** edge visionでは演算だけでなくsensor→memory間のdata movementも効く。sensor側tokenizationの優位が、大型array、real-world noise、end-to-end workloadでも維持できるかが評価点だ。

- 🔗 情報源: [Nature Electronics](https://www.nature.com/articles/s41928-026-01719-9)
- 🕰️ 公開日時: 2026-09-14
- 🗂️ 分類: Edge AI・AIハードウェア

**📚 追加で確認した資料:**

- <https://doi.org/10.1038/s44460-026-00122-3>

---

> 本記事は公開情報をもとに編集されています。重要な判断にはリンク先の一次情報をご確認ください。
