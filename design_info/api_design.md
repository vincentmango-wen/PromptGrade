# OpenAI API 利用設計書（PromptGrade）

## 📌 目的

このドキュメントは、プロンプト評価アプリ「PromptGrade」において、OpenAI API（`chat/completions`）をどのように利用するかを定義します。

---

## ✅ 使用する API

- エンドポイント：`https://api.openai.com/v1/chat/completions`
- モデル：`gpt-4`（初期は固定／後に切替可能）
- 使用ライブラリ：`openai`（Python 公式 SDK）

---

## 🔐 認証

- 使用する API キーは環境変数 `.env` に保存し、プログラムでは `os.environ` 経由で読み込み
- `.env` ファイル例：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧠 プロンプト構造（Chat 形式）

```json
[
  {
    "role": "system",
    "content": "あなたはプロンプトエンジニアです。以下のプロンプトを評価し、点数（1〜10点）、良い点、改善点、改善プロンプトを出力してください。"
  },
  {
    "role": "user",
    "content": "<ユーザーが入力したプロンプト>"
  }
]
```

---

## 📤 リクエストパラメータ（JSON）

```json
{
  "model": "gpt-4",
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 1024,
  "top_p": 1.0,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
```

---

## 📥 レスポンス期待形式（例）

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "評価: 8/10\n\n良い点:\n- 明確な目的がある\n- 出力形式が指定されている\n\n改善点:\n- 対象の読者やトーンが曖昧\n\n改善プロンプト:\n「営業担当者向けに、フォーマルな文体で商品紹介のメールを生成してください。」"
      }
    }
  ]
}
```

---

## 🧪 出力内容のパース方法

FastAPI 側で以下の項目を抽出し、JSON で返却：

| 項目               | 抽出方法                                | データ例            |
| ------------------ | --------------------------------------- | ------------------- |
| `score`            | 正規表現で `\d{1,2}/10` を抽出          | 8                   |
| `feedback`         | `"良い点:"` から `"改善点:"` までの内容 | 明確な目的...       |
| `suggested_prompt` | `"改善プロンプト:"` 以降の内容          | 「営業担当者向け... |

---

## 🧰 Python 処理概要（擬似コード）

```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=message_list,
    temperature=0.7,
    max_tokens=1024
)

content = response['choices'][0]['message']['content']
# contentから score, feedback, suggested_prompt を抽出して整形
```

---

## 🚫 注意点・エラーハンドリング

| ケース                     | 対策                                                 |
| -------------------------- | ---------------------------------------------------- |
| API キー未設定             | `.env`の存在チェックと例外処理                       |
| OpenAI API 側のエラー      | ステータスコードとエラーメッセージをキャッチして表示 |
| レスポンスが想定形式でない | 出力全体をログに残す / ユーザーに「解析不能」と通知  |

---

## 🛠 今後の拡張案

- 出力フォーマットを JSON に指定しやすくする（function calling などの導入）
- カスタムテンプレートを UI から入力可能に
- 各評価項目を別々に出力（明確さ、具体性、網羅性など）
