# app/services/openai_service.py

import os
import openai
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()
# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

print("DEBUG: ", os.getenv("OPENAI_API_KEY"))  # デバッグ用にキーを表示（本番環境では削除推奨）

# OpenAI APIを呼び出してプロンプトを評価する関数
def evaluate_prompt_with_openai(prompt: str) -> dict:
    """OpenAI APIを使ってプロンプトを評価し、結果を返す
    JSON形式の文字列を返す想定"""

    # ChatGPT に渡す会話形式のメッセージ
    messages = [
        {
            "role": "system",
            "content": """
            あなたはプロンプトエンジニアです。渡されたプロンプトを評価し、
            以下の形式で必ず**JSONだけ**を出力してください。

            {
                "score": <1-10の整数>,
                "feedback": "<改善点やコメント>",
                "suggested_prompt": "<改善したプロンプト>"
            }
            """
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # ChatCompletion API を呼び出し
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # 必要に応じて gpt-3.5-turbo に変更可能
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 結果を返す（後でパースする）
    return response['choices'][0]['message']['content']
