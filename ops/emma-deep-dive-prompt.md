旧ブログの「Tech Deep-Dive」の構成を継承し、技術系の長文解説記事を作成してください。

作業対象:

- 候補: `/home/node/.openclaw/workspace/daily-signal/.daily-signal/deep-dive/candidates.json`
- 出力: `/home/node/.openclaw/workspace/daily-signal/.daily-signal/deep-dive/draft.json`

方針:

1. `editorial_note`の本日テーマを優先し、候補から一つの論点を選ぶ。
2. 候補の元URLを読み、論文・公式ドキュメント・企業発表など一次資料まで確認する。
3. 読者は材料科学、航空宇宙、CAE、CFD、ソフトウェアに詳しい技術系管理職。基礎は短く、原理、定量比較、限界、実務応用を深く書く。
4. 旧ブログのようにTL;DR、体系的な章、表にできる比較、実務への示唆、編集部のまとめを含める。
5. 確認できない数値、将来予測、架空の固有名詞を書かない。査読前研究は明記する。
6. 執筆者名、自分への言及、一人称、署名、挨拶、キャラクター口調を出さず、中立で抑制された編集文体にする。
7. 本文フィールドにURLを書かず、必ず`citations`または`references`へ分離する。
8. 全候補について、業務関連性・情報源品質・新規性を0.0〜1.0で評価し、記事に使わない候補も
   `candidate_feedback`へ元順序で必ず残す。これは次回収集の学習データになる。
9. Git操作やMarkdownファイルの作成は行わず、次のJSONだけを出力先へ保存する。

```json
{
  "title": "日付を含まない日本語タイトル",
  "description": "280字以内の紹介",
  "tags": ["3〜8個のタグ"],
  "source_ids": ["実際に使用した候補id（1件以上）"],
  "tldr": ["3〜6項目の要点"],
  "introduction": "導入",
  "sections": [
    {
      "heading": "章見出し",
      "body": "URLを含まない解説本文",
      "citations": ["確認に使ったhttps URL（1〜5件）"]
    }
  ],
  "takeaways": ["技術・研究開発・経営上の示唆を3〜7項目"],
  "conclusion": "論点と実務上の判断軸を簡潔にまとめた結論",
  "references": ["主要なhttps URLを2〜25件"],
  "candidate_feedback": [
    {"id": "候補id", "relevance": 0.0, "quality": 0.0, "novelty": 0.0, "reason": "短い根拠"}
  ]
}
```

`sections`は3〜9章にしてください。保存後にJSONを読み直し、使用した`source_ids`が候補内に存在すること、全URLがHTTPSであること、全候補の評価が揃っていることを確認してください。
