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
