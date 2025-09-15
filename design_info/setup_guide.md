# 環境構築手順書（PromptGrade）

## 📌 目的

このドキュメントは、プロンプト評価アプリ「PromptGrade」をローカル環境で開発・動作させるために必要なセットアップ手順をまとめたものです。

---

## 🖥 前提環境

| 項目           | 推奨バージョン                  |
| -------------- | ------------------------------- |
| OS             | Windows 10 以降 / macOS / Linux |
| Python         | 3.10 以上                       |
| パッケージ管理 | pip または poetry               |
| 仮想環境       | venv 推奨                       |
| その他         | Git（バージョン管理用）         |

---

## ✅ ステップ一覧

### 1. リポジトリ作成

```bash
mkdir promptgrade
cd promptgrade
git init
```

---

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv venv

# 有効化（Windows）
venv\Scripts\activate

# 有効化（macOS / Linux）
source venv/bin/activate
```

---

### 3. 必要なパッケージのインストール

```bash
pip install fastapi uvicorn openai python-dotenv
```

---

### 4. フォルダ構成の初期化

```bash
mkdir app
touch app/main.py
touch .env
```

---

### 5. `.env` ファイルの作成

```env
# .env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

※ `.env` は `.gitignore` に追加して Git 管理外にすること。

---

### 6. 開発サーバーの起動

```bash
uvicorn app.main:app --reload
```

起動後にブラウザでアクセス：  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 動作確認

FastAPI の初期動作確認用コード（`main.py`）

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PromptGrade API is running"}
```

---

## 🔐 セキュリティ補足

- `.env` ファイルは絶対に Git にコミットしないこと
- `openai` ライブラリで `os.getenv("OPENAI_API_KEY")` を用いて安全に読み込む
- `requirements.txt` を使ってパッケージを明示する

```bash
pip freeze > requirements.txt
```

---

## 🔁 今後の拡張予定

- 自動デプロイスクリプトの作成（Docker など）
- Poetry や Makefile での環境管理
- フロントエンドとの統合セットアップ

---

## 💾 推奨保存ファイル名

```
setup_guide.md
```
