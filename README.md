# Daily Signal

論文、技術、科学、社会のフィードを毎日収集し、短い日本語ダイジェストとして公開するHugoサイトです。

表示テーマには[Blowfish](https://github.com/nunocoracao/blowfish)を使用し、柔らかい女性秘書風の案内と絵文字を取り入れています。

## Architecture

1. `config/sources.yaml` に登録されたRSS/Atomフィードを収集
2. URLの正規化、既読除外、鮮度とキーワードによるランキング
3. 上位項目をxAI Responses APIのWeb Searchで調査し、中立的な日本語に要約
4. `content/daily/` にHugo Markdownを生成
5. GitHub ActionsからGitHub Pagesへデプロイ

APIキーが設定されていない場合も、フィードの概要を使ったsource-only記事を生成できます。

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/daily_signal.py --dry-run
hugo server -D
```

## GitHub setup

Repository settingsで次を設定します。

1. **Settings → Pages → Source** を `GitHub Actions` にする
2. **Settings → Secrets and variables → Actions → Secrets** に `XAI_API_KEY` を追加
3. 必要ならActions Variable `XAI_MODEL` でモデルを変更（既定値: `grok-4.3`）

日次処理は日本時間7時17分頃に実行されます。GitHub Actionsの混雑により開始が遅れる場合があります。Actions画面から手動実行もできます。

## Configure sources

`config/sources.yaml` でフィード、分類、重み、関心キーワード、採用件数を変更できます。元記事本文は保存せず、URLと短い要約だけをリポジトリに残します。

## Editorial policy

- 一次情報と公式発表を優先する
- すべての項目に情報源リンクを付ける
- 入力にない事実を補完しない
- AI生成であることを記事内に明記する

## License

Code is released under the MIT License. Generated summaries and linked source content may be subject to their respective rights.

