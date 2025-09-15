from fastapi import FastAPI
from app.api import evaluate
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# /evaluate のルートをアプリに追加
app.include_router(evaluate.router)

# 静的ファイルの提供（例: フロントエンドのビルドファイル）
# http://127.0.0.1:8000/ でindex.htmlが提供される
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")