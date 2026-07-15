# Daily Signal

論文、技術、科学、社会のフィードを毎日収集し、Emma先生が短い日本語ダイジェストとして編集・公開するHugoサイトです。

表示テーマには[Blowfish](https://github.com/nunocoracao/blowfish)を使用しています。

## Architecture

1. VPSのsystemd timerが日本時間7時17分頃に日次処理を開始
2. `config/sources.yaml` のRSS/Atomフィードを収集し、既読・鮮度・関心分野で候補を決定
3. OpenClaw上のEmma先生（`openai/gpt-5.6-luna`, thinking `high`）が元URLを確認して構造化原稿を執筆
4. 決定論的なpublisherが候補ID、HTTPS引用、出力先を検証してHugo Markdownへ変換
5. host側のランナーだけがリポジトリ専用Deploy Keyを使い、検証済みの2ファイルをcommit/push
6. GitHub ActionsはHugoのビルドとGitHub Pagesへの公開のみを担当

EmmaにはGitHub資格情報を渡しません。Emmaが変更できるのは共有workspace内の原稿で、pushはhost側の許可リスト検証を通過した後に実行されます。

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests
python -m scripts.emma_pipeline prepare
```

`prepare`は`.daily-signal/candidates.json`を作成します。Emmaの代わりに手動で`.daily-signal/draft.json`を用意した場合は、次のコマンドで検証・記事化できます。

```bash
python -m scripts.emma_pipeline publish
```

## VPS deployment

想定パス:

- Repository: `/opt/openclaw/data/workspace/daily-signal`
- OpenClaw compose: `/opt/openclaw/source/docker-compose.yml`
- Deploy Key: `/home/ubuntu/.ssh/daily-signal_deploy`
- Optional environment: `/etc/default/daily-signal-emma`

初回セットアップ:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
sudo install -m 0644 ops/daily-signal-emma.service /etc/systemd/system/
sudo install -m 0644 ops/daily-signal-emma.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now daily-signal-emma.timer
```

Discordへ結果を通知する場合、`/etc/default/daily-signal-emma`へ次を設定します。

```bash
DAILY_SIGNAL_DISCORD_USER_ID=your-discord-user-id
```

手動実行と状態確認:

```bash
sudo systemctl start daily-signal-emma.service
sudo journalctl -u daily-signal-emma.service -n 200 --no-pager
systemctl list-timers daily-signal-emma.timer
```

## GitHub setup

Repository settingsで次を設定します。

1. **Settings → Pages → Source** を `GitHub Actions` にする
2. VPSで生成したDeploy Keyの公開鍵を **Settings → Deploy keys** へ書き込み権限付きで追加
3. Actionsの旧`XAI_API_KEY` secretと`XAI_MODEL` variableは不要になったため削除可能

GitHub Actionsの日次生成scheduleは廃止しています。Pages workflowはEmmaのpushを検知して公開します。

## Configure sources

`config/sources.yaml` でフィード、分類、重み、関心キーワード、採用件数を変更できます。元記事本文は保存せず、URLと短い要約だけをリポジトリに残します。

## Editorial policy

- 一次情報と公式発表を優先する
- すべての項目に元情報リンクを付ける
- 確認できない事実や数値を補完しない
- 基礎説明を短くし、技術的新規性と実務上の意味を明確にする
- Emma/OpenClawによる生成であることを記事内に明記する

## License

Code is released under the MIT License. Generated summaries and linked source content may be subject to their respective rights.
