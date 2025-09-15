# app/schemas/prompt_schema.py

from pydantic import BaseModel

# ユーザーから送られる入力データ
class PromptRequest(BaseModel):
    prompt: str  # 入力されたプロンプト文字列

# ユーザーに返す出力データ
class PromptResponse(BaseModel):
    score: int  # 評価スコア（1〜10）
    feedback: str  # 改善点などのコメント
    suggested_prompt: str  # 改善されたプロンプト例
