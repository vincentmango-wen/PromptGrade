# app/api/evaluate.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.prompt_schema import PromptRequest, PromptResponse
from app.services.openai_service import evaluate_prompt_with_openai
from app.utils.parser import parse_ai_response

# ルーター（APIのグループ）を作成
router = APIRouter()

# POSTメソッドで /evaluate エンドポイントを定義
# ユーザーが送信したプロンプトを受け取り → OpenAI APIで評価 → 結果を返す
@router.post("/evaluate", response_model=PromptResponse)
def evaluate_prompt(request: PromptRequest):
    # プロンプトが空だった場合、エラーを返す
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required.")

    # OpenAI APIへプロンプトを送信し、評価結果を取得（文章形式）
    ai_response_text = evaluate_prompt_with_openai(request.prompt)

    # OpenAIの返答を解析し、構造化されたデータに変換
    result = parse_ai_response(ai_response_text)

    # Pydanticモデルで整形された結果を返却
    return PromptResponse(**result)
