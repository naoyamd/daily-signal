# Daily Signal

検証済み候補をOpenClawで編集し、Hugo記事として公開するブログリポジトリです。
表示テーマには[Blowfish](https://github.com/nunocoracao/blowfish)を使用しています。

## Responsibility boundary

情報収集、Webスカウト、適応学習、必須企業ウォッチリスト、Obsidian Markdown Vaultは、
独立した`daily-signal-collector`リポジトリが担当します。このブログはRSSやWebへ収集アクセスせず、
学習SQLiteやVaultにも書き込みません。

両リポジトリの境界は`/var/lib/daily-signal-exchange`のバージョン付きJSONだけです。

- 入力 `daily-signal-candidates/v1`: 期限、版、batch ID、候補、収集由来を検証してから使用
- 出力 `daily-signal-feedback/v1`: 記事採否と全候補の`relevance / quality / novelty`評価を返却

collector側はブログのGit資格情報を持たず、ブログ側はcollectorの収集・蓄積権限を持ちません。

## Publishing flow

1. systemdが対応する`daily-signal-collector@<edition>.service`を先に実行
2. collectorの期限付き候補JSONをblog workspaceへコピーせず読み取り、ローカル作業JSONへ検証インポート
3. OpenClaw編集エージェントが一次URLを確認し、公開項目と全候補評価を構造化JSONで作成
4. 決定論的publisherが候補ID、HTTPS引用、匿名編集文体、出力先を検証してHugo Markdownへ変換
5. host runnerだけが記事と既読stateをcommit/push
6. 評価イベントをexchangeへ原子的に返し、次回collector実行時に学習とVault状態へ反映

編集エージェントにはGitHub資格情報を渡しません。公開ファイルのcommit/pushはhost runnerの許可リストを
通過した後にだけ行います。

## Local development

```bash
python -m unittest discover -s tests
python -m scripts.emma_pipeline prepare \
  --handoff /path/to/exchange/candidates/digest.json \
  --output .daily-signal/candidates.json
```

手動で`.daily-signal/draft.json`を用意した場合:

```bash
python -m scripts.emma_pipeline publish \
  --bundle .daily-signal/candidates.json \
  --draft .daily-signal/draft.json \
  --feedback-outbox /path/to/exchange/feedback
```

## VPS deployment

先に`daily-signal-collector`をインストールし、その後このリポジトリを導入します。

```bash
python3 -m venv .venv
sudo bash ops/install-vps.sh

# collectorの手動成功確認後にのみ有効化
sudo systemctl enable --now \
  daily-signal-emma.timer \
  daily-signal-emma-deep-dive.timer \
  daily-signal-emma-market.timer
```

既定パス:

- blog: `/opt/openclaw/data/workspace/daily-signal`
- collector: `/opt/openclaw/data/workspace/daily-signal-collector`
- JSON exchange: `/var/lib/daily-signal-exchange`

これらのパスと実行ユーザーはsystemd unitと揃えた固定値です。installerはcollector unit、Git状態、
仮想環境、exchange書込権限を事前確認し、timerを自動起動しません。

Discord通知が必要な場合、`/etc/default/daily-signal-emma`へ次を設定します。

```bash
DAILY_SIGNAL_DISCORD_USER_ID=your-discord-user-id
# DAILY_SIGNAL_EXCHANGE_DIR=/var/lib/daily-signal-exchange
```

```bash
sudo systemctl start daily-signal-emma.service
sudo journalctl -u daily-signal-emma.service -n 200 --no-pager
systemctl list-timers 'daily-signal-emma*.timer'
```

## Publishing schedule

| 時刻（JST） | 頻度 | 内容 |
|:---|:---|:---|
| 03:30 | 毎日 | Tech Deep-Dive |
| 07:00 | 毎日 | AI・科学・産業デイリーダイジェスト。日曜は週間レビュー |
| 16:45 | 月〜金 | 大引け後の株式レポート |

市場データを確認できない日は株式レポートを推測で作らず休刊します。

## GitHub setup

1. **Settings → Pages → Source** を `GitHub Actions` にする
2. VPSのDeploy Key公開鍵を **Settings → Deploy keys** へ書き込み権限付きで追加
3. GitHub ActionsはHugo buildとPages公開だけを担当

## Editorial policy

- 一次情報と公式発表を優先する
- すべての項目に元情報リンクを付ける
- 確認できない事実や数値を補完しない
- 技術的新規性と実務上の意味を明確にする
- 執筆者名やキャラクターを表に出さず、中立的な編集記事として書く

## License

MIT
