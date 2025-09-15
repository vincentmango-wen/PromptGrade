# PromptGrade（プロンプト評価アプリ）

## 🚀 概要

**PromptGrade** は、ユーザーが入力したプロンプトに対して、OpenAI API（GPT-4 など）を用いて **評価（スコアリング）** および **改善提案** を行うアプリケーションです。

初心者〜中級者がプロンプトエンジニアリングの理解を深めるために設計されており、簡易 UI と FastAPI で構成されています。

---

## ✨ 主な機能

- ✅ プロンプトを AI が評価（1〜10 点）
- ✅ 良い点・悪い点をフィードバック表示
- ✅ 改善案として「より良いプロンプト例」を提示
- ✅ 履歴をローカルに保存（オプション）

---

## 🛠 使用技術

| 分類           | 技術                             |
| -------------- | -------------------------------- |
| バックエンド   | FastAPI (Python)                 |
| フロントエンド | HTML / JavaScript（軽量構成）    |
| API            | OpenAI API（`chat/completions`） |
| モデル         | GPT-4（または GPT-3.5）          |
| 開発環境管理   | venv + .env（API キー管理）      |

---

## 🔧 セットアップ手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/promptgrade.git
cd promptgrade
```

### 2. 仮想環境を作成・有効化

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. `.env` ファイルを作成

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. サーバー起動

```bash
uvicorn app.main:app --reload
```

アクセス：[http://localhost:8000](http://localhost:8000)

---

## 💬 API 使用例

### エンドポイント：`POST /evaluate`

```json
{
  "prompt": "中学生でも理解できるように、量子コンピュータについて説明してください。"
}
```

レスポンス例：

```json
{
  "score": 9,
  "feedback": "対象が明確で、語調も親切。ただし専門用語がやや多いです。",
  "suggested_prompt": "中学生向けに、難しい言葉を使わず量子コンピュータの仕組みを説明してください。"
}
```

---

## 📁 ディレクトリ構成（抜粋）

```
app/
├── main.py
├── api/
│   └── evaluate.py
├── services/
│   └── openai_service.py
├── schemas/
│   └── prompt_schema.py
├── utils/
│   └── parser.py
.env
requirements.txt
README.md
```

---

## 🔐 注意事項

- OpenAI API キーは `.env` に記載し、絶対に公開しないでください。
- 本アプリは学習目的の MVP であり、セキュリティ・運用面は商用利用を前提に設計されていません。

---

## 📄 関連資料

- [要件定義書](./requirements.md)
- [API 仕様書](./api_spec.md)
- [OpenAI API 利用設計書](./openai_api_design.md)
- [ディレクトリ構成](./directory_structure.md)
- [実装計画書](./implementation_plan.md)
- [利用規約・プライバシーポリシー](./terms_and_privacy.md)

---

## ✍️ 開発者

- 開発者：あなた（プログラミング学習者）
- 開発期間：2〜4 週間（学習兼ねて進行）

---

## 📄 推奨保存ファイル名

```
README.md
```
