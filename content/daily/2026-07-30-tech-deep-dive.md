---
title: "PhysicsNeMoの設計を読む：Scientific MLをPyTorchからドメイン並列へ拡張する方法"
date: 2026-07-30T04:03:30.278374+09:00
draft: false
description: "NVIDIA PhysicsNeMoを題材に、Scientific ML基盤をモデル、データ、メッシュ、物理残差、分散実行へ分解する設計を解説する。DDP・FSDP2・ドメイン並列とShardTensorの違い、公式ベンチマークの読み方、CAE導入の検証ゲートを整理する。"
categories: ["Tech Deep-Dive"]
tags: ["PhysicsNeMo", "Scientific ML", "PyTorch", "分散システム", "ドメイン並列", "CAE", "ニューラルオペレータ", "ソフトウェア設計", "Tech Deep-Dive"]
generated_by: "OpenClaw Editorial System"
model: "openai/gpt-5.6-luna"
source_count: 1
generation_cost_usd: 0
---

## 📋 要約（TL;DR）

- PhysicsNeMoはニューラルオペレータやGNNのモデル集にとどまらず、科学データの入出力、GPUネイティブなメッシュ、物理残差、分散実行、推論までをPyTorchの周囲に組み合わせるオープンソースPython基盤である。
- 現行のv2.0設計では、再利用可能な層、完成したモデル、メッシュ処理、データパイプライン、拡散モデル、物理計算、ドメイン並列を分離し、依存関係と拡張点を明確にしている。
- 通常のDDPはサンプルをGPUへ分配し、FSDP2はモデル状態を分割する。一方、ドメイン並列は高解像度の一つのメッシュや場を複数GPUへ分割するため、Scientific MLでは別の通信設計が必要になる。
- ShardTensorはPyTorchのDTensorを基礎に、不均一なメッシュや点群を想定したドメイン分割を扱う。公式チュートリアルには、特定条件で8 GPUのスケーリング効率が95%を超える例があるが、一般性能ではない。
- CAE導入の判断は推論速度だけで決められない。場の誤差、保存則、境界フラックス、設計指標、外挿検出、再学習とフォールバックを一つの検証閉ループとして管理する必要がある。

Scientific MLの実装は、モデルの選択だけで終わらない。CFDや構造解析では、形状、メッシュ、境界条件、時系列、物性、物理残差、分散学習、推論時の監視が同時に設計対象になる。どれか一つを既存の深層学習コードから借りてくるだけでは、データ生成から検証、運用までの再現性を保ちにくい。

NVIDIA PhysicsNeMoは、この問題を専用の一つのニューラルネットワークで解決しようとするのではなく、PyTorchと相互運用できる複数のモジュールへ分解する。注目点は、物理AIの精度そのものだけではない。科学計算のデータ構造と通信パターンを、ソフトウェアの公開インターフェースとしてどのように表現するかにある。本稿では、PhysicsNeMoを採用すべきかという製品評価ではなく、Scientific MLを工学システムへ組み込む際の設計原則として読み解く。

## 1. PhysicsNeMoはモデル集ではなく、科学計算向けランタイムの組み立てである

PhysicsNeMoの公式説明は、ニューラルオペレータ、GNN、PINN、拡散モデルなどを含むPhysics AIの構築・学習・微調整・推論用フレームワークと位置付けている。ただし、実務上の中心はモデル一覧ではなく、モデルをデータと計算環境へ接続する境界の設計にある。

|層|主な責務|CAE・CFDでの対応|
|---|---|---|
|モデル|FNO、DeepONet、GNN、Transformer、拡散モデルなど|場の予測、時系列発展、点群・メッシュ上の回帰|
|データ|Reader、Transform、Dataset、DataLoader|HDF5、Zarr、VTK、点群、メッシュ、時系列|
|幾何・メッシュ|点、セル、隣接、微分、空間検索、リメッシュ|CAD由来形状、表面・体積メッシュ、局所近傍|
|物理|記号的なPDE、空間微分、残差|物理情報付き損失、境界条件、保存則の評価|
|分散|DDP、FSDP2、DeviceMesh、ShardTensor、collective|データ並列、モデル状態の分割、領域分割|
|運用|チェックポイント、評価、推論、デプロイ|設計探索、デジタルツイン、監視付きサロゲート|

この分解は、研究段階でモデルを交換しやすくするだけではない。例えば、同一のメッシュとデータ変換を使ったままFNOをMeshGraphNetへ置き換えたり、学習用の場予測モデルに物理残差を追加したり、単一GPUの検証コードを分散学習へ拡張したりできる。モデル、物理、データ、並列化の責務を一つの巨大な学習スクリプトへ埋め込まないことが、比較実験と保守の前提になる。

v2.0の移行ガイドは、再利用部品を`physicsnemo.nn`、完成したモデルを`physicsnemo.models`、拡散処理を`physicsnemo.diffusion`、メッシュ処理を`physicsnemo.mesh`、科学データのパイプラインを`physicsnemo.datapipes`、ドメイン並列を`physicsnemo.domain_parallel`へ分ける方針を示す。これは単なる名前変更ではなく、循環依存を減らし、オプション依存を利用分野ごとに閉じ込めるための境界整理である。

**参照:**

- <https://developer.nvidia.com/physicsnemo>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://github.com/NVIDIA/physicsnemo/blob/main/v2.0-MIGRATION-GUIDE.md>

## 2. データと幾何をテンソルの外側に置かない設計

通常の深層学習では、入力を固定形状のテンソルへ変換した後のモデルが主役になりやすい。しかしCAEでは、変換前の情報に物理的意味がある。点の座標、セルの接続、境界面、点ごとの温度や速度、セルごとの応力、メッシュ全体の条件を、分離した配列として管理すると、前処理と推論の間で対応関係を失いやすい。

PhysicsNeMo-Meshは、点座標、セル接続、点データ、セルデータ、グローバルデータをまとめて保持するTensorDict系のデータ構造を中心に据える。テンソルとしてGPUへ移動でき、PyTorchの自動微分と結び付けられるため、幾何変換、空間微分、学習モデルの入力を同じ計算グラフの中で扱える。これは、メッシュを単なる前処理ファイルではなく、学習対象に付随する状態として扱う設計である。

データパイプラインも同じ思想で分割される。ReaderはHDF5、Zarr、VTKなどの形式を読み、Transformは正規化やサブサンプリングを行い、DatasetとDataLoaderがPyTorchの学習ループへ渡す。大規模データでは、I/O、CPUでの変換、GPU転送、モデル計算のどこが律速かを個別に計測できる。データ変換を学習スクリプト内の無名関数へ散在させる構成と比較すると、再現性、キャッシュ、テストの責務が明確になる。

|設計対象|固定テンソル中心の実装|PhysicsNeMoが想定する分解|実務上の確認点|
|---|---|---|---|
|形状|画像や配列へ事前変換|Mesh、DomainMesh、点群、グラフ|座標系、単位、接続、境界ID|
|場データ|入力テンソルに連結|点・セル・全体の属性として保持|時刻、物理量、欠測、スケール|
|前処理|学習コードへ埋め込む|Reader、Transform、Datasetへ分離|再現性、キャッシュ、並列I/O|
|物理量|損失関数に直接記述|記号式と空間微分を別モジュール化|残差の単位、境界、微分精度|

この設計は、すべてのCAEデータがそのまま扱えることを意味しない。異なるメッシュ、境界ラベル、物性テーブル、ソルバーの出力規約を一つの共通表現へ変換する作業は残る。重要なのは、その変換を暗黙の前処理ではなく、テスト可能なデータ契約として切り出せる点にある。

**参照:**

- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://github.com/NVIDIA/physicsnemo/blob/main/v2.0-MIGRATION-GUIDE.md>
- <https://docs.nvidia.com/physicsnemo/latest/physicsnemo/api/physicsnemo.datapipes.html>

## 3. Scientific MLの並列化は、データ・モデル状態・領域を分けて考える

Scientific MLの分散化では、GPU数を増やせば同じコードが速くなるとは限らない。何を分割するかによって、メモリの減り方、通信の頻度、モデル側に必要な変更が変わる。PhysicsNeMoの分散ドキュメントは、主にデータ並列、モデル並列、ドメイン並列を区別している。

|方式|分割するもの|一つのGPUが保持するもの|主な通信|向く状況|
|---|---|---|---|---|
|DDP|バッチ内のサンプル|モデル全体と担当サンプル|各反復の勾配all-reduce|モデルが1 GPUに収まり、サンプル数を増やしたい場合|
|FSDP2|パラメータ、勾配、オプティマイザ状態|モデル状態の一部と局所計算|必要な場面での状態集約と勾配同期|モデル状態が1 GPUのメモリに収まらない場合|
|ドメイン並列|一つの場、メッシュ、点群の空間領域|担当領域と境界・halo|隣接領域のデータ交換、collective|一つの高解像度サンプル自体が大きい場合|
|パイプライン並列|モデルの層や処理段階|担当ステージ|ステージ間の活性値転送|段階化できる大規模モデルや推論|

DDPは、各GPUが異なるサンプルを処理し、反復ごとに勾配を平均する。したがって、モデルと一つのサンプルが各GPUに収まることが出発点になる。FSDP2は、パラメータ、勾配、オプティマイザ状態を分割してメモリを下げるが、前向き・後向きで必要な状態を集める通信が増える。理想化すれば、状態メモリの一部はGPU数Pに対しておおむね1/Pへ近づくが、活性値、通信バッファ、複製されるテンソル、断片化は別に残る。これはベンチマーク値ではなく、方式を選ぶためのメモリ収支の見方である。

ドメイン並列は、サンプル数ではなく一つの物理領域を分割する。局所領域の体積をV、隣接交換に必要なhaloをHとすると、通信・重複の割合は概念的にHとVの比で決まる。領域を細かくし過ぎるとVが小さくなり、halo交換が支配的になる。逆に、高解像度で局所演算が多いモデルでは、単一GPUに収まらない場を複数GPUで処理できる価値が大きい。

この三方式は排他的ではない。例えば、各サンプルを複数GPUへドメイン分割し、その上でモデル状態をFSDP2で分散する二次元のDeviceMeshを構成できる。ソフトウェア設計上の要点は、並列化をモデルの内部実装へ全面的に埋め込まず、プロセスグループ、rank、device、DeviceMesh、collectiveを明示的なランタイム境界として管理することである。

**参照:**

- <https://docs.nvidia.com/physicsnemo/latest/user-guide/distributed_training.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://docs.nvidia.com/physicsnemo/latest/physicsnemo/api/physicsnemo.distributed.html>

## 4. ShardTensor――不均一な物理領域をPyTorchの分散テンソルへ接続する

科学データを単純なchunk分割で扱えない理由は、メッシュや点群が均一な長方形配列ではないからである。セル数が領域ごとに異なり、隣接関係が局所的で、境界面では通信の対象が変わる。PyTorchのDTensorは汎用的な分散テンソルの基盤として有用だが、公式チュートリアルは、科学データに多い不均一分布や単純なchunk規則ではドメイン並列に適用しにくい場合を指摘する。

ShardTensorはDTensorの分散配置とPyTorchのDeviceMeshを基礎に、物理領域の分割、局所テンソル、配置仕様、勾配伝播を扱う層として説明されている。単一GPU上のテンソルを指定した軸で散布し、分散されたモデルへ渡し、必要な時点で全体テンソルへ戻すという流れを、autogradと接続する。実装上は、分散テンソルと通常テンソルの変換、配置仕様の推定、局所形状、all-gatherやall-to-allのような通信を考慮しなければならない。

|観点|通常のDDP|ShardTensorによるドメイン並列|
|---|---|---|
|サンプル|一つのサンプルは一つのGPUへ|一つのサンプルを複数GPUへ|
|分割対象|バッチ次元が中心|空間、メッシュ、点群、系列の一部|
|モデル条件|通常のPyTorchモデルをDDPで包む|対応する演算と配置規則が必要|
|通信|反復ごとの勾配同期|前後向きの境界交換、集約、勾配通信|
|失敗モード|バッチ不足、負荷不均衡|halo過多、未対応演算、配置不整合|

公式チュートリアルの図は、合成的な畳み込み・系列長の条件で、8 GPUにおける大きな系列長のスケーリング効率が95%を超える例を示している。これは、同じ問題を8 GPUで実行した特定実装の結果であり、CFD、構造解析、すべてのメッシュ形状へ外挿できる数値ではない。スケーリング効率をE = T1 / (8 × T8)と定義する通常の読み方なら、Eが0.95を超える条件は8 GPU時の理想比に対して7.6倍を超える速度に相当するが、単一GPUの基準、系列長、演算、通信ネットワークが変われば成立しない。

ドメイン並列を実務へ移す際は、全体場との一致だけでなく、局所境界での勾配、halo更新の順序、非同期通信の完了、空領域の負荷偏りをテストする必要がある。公式チュートリアルが示すように、ShardTensorの利用には、対応演算、FSDP2との組み合わせ、モデルのメモリアクセス特性が条件になる。DDPのラッパーを交換するだけの作業ではない。

**参照:**

- <https://docs.nvidia.com/physicsnemo/latest/user-guide/domain_parallelism/domain_parallelism.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/domain_parallelism/fsdp_and_shard_tensor.html>
- <https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/domain_parallel/shard_tensor.py>

## 5. モデルの選択は、物理の種類よりデータ構造と通信パターンで決まる

PhysicsNeMoのモデル一覧を、単純な精度ランキングとして読むのは適切でない。公式のモデルアーキテクチャ表は、各レシピをデータ構造、スケーリング方式、最適化手法と一緒に記載している。これは、同じCFDでも、規則格子、非構造メッシュ、CAD点群、球面格子で必要な計算パターンが違うからである。

|モデル系統|主なデータ構造|公式ドキュメントが示すスケール設計|設計上の含意|
|---|---|---|---|
|FNO・PINO|2D・3Dの規則格子|DDPを用いるレシピ|FFTやスペクトル演算、境界表現、格子解像度が支配的|
|MeshGraphNet|グラフ、メッシュ、時系列|複数GPU・複数ノードのDDP|ノード・エッジの近傍集約と負荷分散が中心|
|X-MeshGraphNet|CAD点群、局所・多重解像度グラフ|ドメイン並列、100 million cells以上を想定する記載|大規模形状の領域分割とhaloが中心|
|SFNO|球面などのN次元規則格子|モデルとデータを複数GPUへ分ける空間モデル並列|空間軸とモデル軸のDeviceMesh設計が必要|
|DeepONet|規則格子と不規則な評価点|公式表では単一GPU|branch・trunkの入力形状と評価点のサンプリングが中心|

例えば、規則格子上のFNOでは、FFTやテンソル演算を大きなバッチで処理する設計が比較的自然である。非構造メッシュ上のMeshGraphNetでは、近傍関係とエッジメッセージが中心になり、グラフの分割が通信量を決める。CAD形状を点群として扱うモデルでは、メッシュ生成を完全に省けるとは限らないが、学習時に利用する幾何表現と局所検索のコストを別に評価できる。

公式表には、X-MeshGraphNetについて100 million cells以上へのスケール、Transformer系の一部についてTransformer Engine使用時の25%速度向上、特定の点群空間投影について素朴なPyTorch実装に対する最大1,384倍という数値も記載されている。これらはそれぞれ、特定のモデル、カーネル、入力、GPU、実装条件に閉じた値であり、モデル間の総合順位ではない。特に、カーネル単体のスループットを、データ読み込み、近傍構築、通信、学習収束、検証を含むエンドツーエンドのCAE時間へ置き換えてはならない。

したがって、モデル選択の一次質問は「どのモデルが最も高精度か」ではなく、「場をどのデータ構造で表し、どの軸を分割し、何を通信し、どの工学量を出力するか」である。精度比較は、その設計が固定された後に行うべきである。

**参照:**

- <https://docs.nvidia.com/physicsnemo/latest/user-guide/model_architectures.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://github.com/NVIDIA/physicsnemo>

## 6. 物理情報付き学習と評価は、別々の検証層として設計する

物理残差を損失へ入れたからといって、予測場が自動的に工学的に正しいわけではない。PhysicsNeMoの記号的なPDE機能は、SymPyで式を定義し、空間微分と残差をPyTorchの学習ループへ渡すための部品である。これは物理法則を実装しやすくするが、学習データ、境界条件、数値微分、損失重み、モデル容量、外挿領域の問題を消すものではない。

評価は少なくとも五層へ分ける必要がある。

|評価層|代表的な量|見逃しやすい失敗|
|---|---|---|
|予測誤差|MSE、MAE、相対誤差、時系列誤差|局所ピークや境界付近の失敗|
|物理残差|PDE残差、発散、運動量・エネルギー残差|平均誤差が小さいが保存則を破る場|
|収支・境界|質量・熱・電荷のフラックス、境界条件誤差|流入出の整合が崩れる失敗|
|工学指標|揚力、抗力、圧力損失、最高温度、応力、変位|場の誤差が小さくても設計判断を誤る失敗|
|適用範囲|OOD検出、分布ドリフト、不確実性、フォールバック率|学習域外でもっともらしい値を返す失敗|

公式のモデル評価ページは、チェックポイントと推論スクリプトを用いた評価・推論をワークフローの一部として扱う。これは再現可能な実験の入口だが、認証や設計許可に必要な独立検証を代替しない。高忠実度ソルバー、風洞・材料試験、実運用センサなど、学習に使っていない情報源との照合が必要になる。

定量比較では、同じ精度水準で比較することが重要である。例えばニューラルモデルの推論時間だけを、粗いメッシュの数値ソルバーと比較すれば、速度差は大きく見える。反対に、学習データ生成、前処理、メッシュ検索、GPU転送、再学習、外れ値の高忠実度再計算まで含めれば、総保有計算量は変わる。採用判断では、1回の推論時間ではなく、設計探索で必要な評価回数Nに対して、データ生成費用、学習費用、推論費用、検証費用を合計した総コストで比較するべきである。

**参照:**

- <https://docs.nvidia.com/physicsnemo/latest/user-guide/model_evaluation.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://developer.nvidia.com/physicsnemo>

## 7. CAE・航空宇宙へ導入するための四つのゲート

PhysicsNeMoのような基盤を実務へ導入する場合、最初から従来ソルバーを置き換えるのはリスクが高い。対象の物理、形状、運転条件、出力指標を狭く定義し、サロゲートが判断を補助する範囲から始める方が、検証と撤退条件を明確にしやすい。

|ゲート|確認する契約|合格条件の例|
|---|---|---|
|1. データ契約|座標系、単位、メッシュ、境界、物性、時刻、欠測|学習・検証・推論で同じ意味を持つスキーマが固定されている|
|2. 並列契約|DDP、FSDP2、ドメイン並列の対象軸、通信、rank間の再現性|GPU数を変えても場、勾配、収束判定、チェックポイントが整合する|
|3. 物理・工学契約|PDE残差、保存則、境界フラックス、設計指標|平均損失だけでなく、最悪ケースと極値が許容範囲内にある|
|4. 運用・経済契約|OOD検出、フォールバック、再学習、監査、総コスト|適用範囲外で高忠実度解析へ戻り、更新後のモデルを追跡できる|

ソフトウェア面では、単一GPUの最小実装、DDP、FSDP2、ドメイン並列の順に段階化するのが妥当である。各段階で同じ小規模ケースの予測、勾配、チェックポイント、工学指標を比較し、並列化による数値差とモデル変更による数値差を分離する。ShardTensorを使う場合は、対応演算とhalo通信を個別にベンチマークし、局所領域を増やしたときに通信がどの時点で支配的になるかを測る。

v2.0の移行では、インポートパス、チェックポイント、オプション依存、物理記号式の定義方法が変わる。特に、メッシュやVTKのようなCAE固有依存を使わない利用者まで同じインストールを要求しない設計へ整理された一方、既存コードの移行確認は必要である。これはライブラリ更新の問題であると同時に、研究成果を再現可能な実験資産として管理する問題でもある。

最終的な意思決定は、GPUを何枚使えるかではなく、どの反復計算を短縮すれば設計・保全・試験計画の価値が増えるかで決まる。高忠実度解析を残したまま候補点のスクリーニング、実験条件の絞り込み、センサ状態の推定へ使うなら、失敗時の戻り先を保ったまま導入できる。逆に、適用域外を検出できず、設計許可や安全余裕を単独で決めるなら、公式ベンチマークの数値だけでは根拠が不足する。

**参照:**

- <https://github.com/NVIDIA/physicsnemo/blob/main/v2.0-MIGRATION-GUIDE.md>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/distributed_training.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/domain_parallelism/fsdp_and_shard_tensor.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/model_evaluation.html>

## 🎯 実務への示唆

- Scientific ML基盤はモデル精度だけでなく、データ契約、幾何表現、物理残差、分散実行、評価、推論監視を交換可能な部品として設計する必要がある。
- DDPはサンプルを分け、FSDP2はモデル状態を分け、ドメイン並列は一つの高解像度場を分ける。GPU不足の原因を特定してから並列方式を選ぶべきである。
- ShardTensorはメッシュや点群のような不均一データに対応するための拡張であり、DDPのラッパー交換だけで導入できる機能ではない。対応演算、halo通信、FSDP2との組み合わせを検証する必要がある。
- 公式の95%超の8 GPU効率、100 million cells以上、最大1,384倍といった数値は、特定のモデル・入力・カーネル・ハードウェアに限定された結果であり、エンドツーエンド性能や認証性能ではない。
- CAEではMSEを最終指標にせず、保存則、境界フラックス、空力・熱・構造の設計指標、適用範囲外検出を独立に評価する必要がある。
- 実務導入は高忠実度ソルバーを残したサロゲート利用から開始し、再学習、監査、フォールバック、総保有計算量を含めて投資効果を判定するのが合理的である。

## 💭 まとめ

PhysicsNeMoが示す重要な論点は、物理AIを一つのモデルとして扱うのではなく、データ、幾何、物理、モデル、通信、評価を明示的なソフトウェア境界へ分解することである。DDP・FSDP2・ドメイン並列は目的が異なり、ShardTensorは高解像度の不均一データを扱うための追加設計を要求する。採用判断では、限定されたベンチマークの速度倍率より、対象PDEと運転範囲、工学指標、外挿検出、フォールバック、総コストを含む検証閉ループを優先すべきである。

## 📚 参考リンク

- <https://developer.nvidia.com/physicsnemo>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/physicsnemo_for_pytorch.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/distributed_training.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/domain_parallelism/domain_parallelism.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/domain_parallelism/fsdp_and_shard_tensor.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/model_architectures.html>
- <https://docs.nvidia.com/physicsnemo/latest/user-guide/model_evaluation.html>
- <https://docs.nvidia.com/physicsnemo/latest/physicsnemo/api/physicsnemo.distributed.html>
- <https://docs.nvidia.com/physicsnemo/latest/physicsnemo/api/physicsnemo.datapipes.html>
- <https://github.com/NVIDIA/physicsnemo>
- <https://github.com/NVIDIA/physicsnemo/blob/main/v2.0-MIGRATION-GUIDE.md>
- <https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/domain_parallel/shard_tensor.py>

---

> 本記事は公開情報をもとに編集されています。重要な判断には一次情報をご確認ください。
