# app/utils/parser.py

import json


def parse_ai_response(response_text: str) -> dict:
    """
    OpenAI APIからのレスポンス(JSON文字列)を解析して、
    score, feedback, suggested_prompt を抽出する
    """

    try:
        # JSON文字列を辞書型に変換
        data = json.loads(response_text)

        return {
            "score": int(data.get("score", 0)),
            "feedback": data.get("feedback", "フィードバックなし"),
            "suggested_prompt": data.get("suggested_prompt", "改善プロンプトなし")
        }

    except Exception as e:
        # JSONとして読めなかった場合 → 全文をsuggested_promptに入れる
        return {
            "score": 0,
            "feedback": "内容を解析できませんでした。",
            "suggested_prompt": response_text
        }
