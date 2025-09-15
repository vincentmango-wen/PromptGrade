# ディレクトリ構成設計書（PromptGrade）

## 📌 目的

このドキュメントは、プロンプト評価アプリ「PromptGrade」における**プロジェクトディレクトリ構成**と、各ファイル・ディレクトリの**役割**を明確に定義するものです。

---

## 📂 推奨ディレクトリ構成（初期）

```
promptgrade/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── evaluate.py
│   ├── services/
│   │   └── openai_service.py
│   ├── schemas/
│   │   └── prompt_schema.py
│   └── utils/
│       └── parser.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📁 各フォルダ・ファイルの説明

### 🔸 app/

アプリケーションのルートディレクトリ。以下の機能別にモジュールを分割します。

---

#### ・`main.py`

- FastAPI インスタンスの生成・起動ポイント
- ルーティングの集約（`include_router`）

---

#### ・`api/evaluate.py`

- `/evaluate` エンドポイントのルーティング定義
- POST リクエストを受け取り、OpenAI API に渡す処理を呼び出す

---

#### ・`services/openai_service.py`

- OpenAI API との通信ロジックを管理
- モデルやパラメータの設定、レスポンスの取得処理を行う

---

#### ・`schemas/prompt_schema.py`

- `pydantic` を使ったリクエスト・レスポンスのデータ型定義
- 入力検証や出力整形を行う

---

#### ・`utils/parser.py`

- OpenAI API から返されたレスポンスの文字列から、`score`・`feedback`・`suggested_prompt` を抽出するロジックを記述

---

### 🔸 `.env`

- OpenAI API キーなどの環境変数を記述
- Git 管理から除外する

---

### 🔸 `.gitignore`

- `.env`、`__pycache__`、仮想環境などの除外対象を指定

---

### 🔸 `requirements.txt`

- 使用するライブラリとバージョンの一覧
- `pip freeze > requirements.txt` で作成

---

### 🔸 `README.md`

- プロジェクトの概要、セットアップ手順、使い方などを記述

---

## 📦 拡張候補（必要に応じて追加）

| フォルダ名  | 用途                                  |
| ----------- | ------------------------------------- |
| `tests/`    | 自動テスト用ディレクトリ（pytest）    |
| `frontend/` | フロントエンドを別構成で管理する場合  |
| `docs/`     | Markdown や画像ベースの設計資料の格納 |

---

## 🗂 モジュール分離の意義

- **可読性**：役割ごとに整理された構造で、学習効率が上がる
- **再利用性**：サービスロジックやパーサーを他機能でも再利用可能
- **拡張性**：機能追加やエラーハンドリング強化時に容易に対応できる

---

## 💾 推奨保存ファイル名

```
directory_structure.md
```
