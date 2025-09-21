import streamlit as st
from app.api import grade_prompt

# 基本 UI を定義する関数
# コメントは初心者向けに詳しく書いています

def render_ui():
    """
    Streamlit を使った簡易 UI を表示する関数。
    - 左側に入力領域
    - 右側に結果表示
    """
    st.title("PromptGrade - プロンプト簡易評価")

    # テキスト入力ウィジェット
    prompt_text = st.text_area("評価したいプロンプトを入力してください", height=200)

    # モデルと temperature の簡易設定
    model = st.selectbox("モデル", options=["gpt-4", "gpt-4o", "gpt-3.5-turbo"], index=0)
    temperature = st.slider("temperature", 0.0, 1.0, 0.0)

    # 実行ボタン
    if st.button("評価する"):
        with st.spinner("評価中..."):
            result = grade_prompt(prompt_text, model=model, temperature=temperature)
        # 結果を表示
        st.subheader("評価結果")
        st.metric(label="Score", value=f"{result['score']:.1f}")
        st.write("フィードバック:", result["feedback"])
        st.write("生データ:", result["raw"])  # 開発中は raw を表示しておく
