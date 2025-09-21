# PromptGrade

簡易プロンプト評価アプリ（MVP）

セットアップ:

1. Python 仮想環境を作成

   python -m venv .venv
   source .venv/bin/activate

2. 依存関係をインストール

   pip install -r requirements.txt

3. `.env` を `.env.example` から作成し、必要なら `OPENAI_API_KEY` を設定

4. アプリを起動

   streamlit run app.py

## API キーの扱い（注意）

- このアプリではローカルの環境変数 `OPENAI_API_KEY` を使うか、UI 上で一時的にユーザーが入力した API キーを使うことができます。
- セキュリティのため、公開リポジトリに API キーをコミットしないでください。`.env` に保存する場合は `.gitignore` に含めておきます。
- 公共の場所でアプリをホストする場合は、ユーザーが直接自分のキーを入力する設計（今回の UI）か、サーバー側で安全に管理されたキーを使う設計に切り替えてください。
- 開発中は `モックを強制使用する` オプションを利用すると、API コールを行わずに動作確認できます。

# JSON -> SQLite 移行手順

保存された履歴（data/history.json）を SQLite (`data/history.db`) に移行する手順:

1. 必要に応じて `data/history.json` のバックアップを作成します。

2. 移行スクリプトを実行します（プロジェクトルートは `promptgrade` フォルダ）:

```bash
python scripts/migrate_to_sqlite.py
```

3. スクリプトは `app/db.py` の `init_db()` を呼び出し、`history.json` の各エントリを SQLite に書き込みます。

注意: 移行前に SQLite DB のバックアップを取りたい場合は `data/history.db` を別名でコピーしてください。
