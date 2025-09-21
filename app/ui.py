import streamlit as st
from app.api import grade_prompt

# 基本 UI を定義する関数
# コメントは初心者向けに詳しく書いています


def render_ui():
    """
    Streamlit を使った簡易 UI を表示する関数。
    追加した機能:
      - ユーザーの OpenAI API キー入力欄（任意）
      - モックを強制使用するチェックボックス
      - 実行時のエラーを丁寧に表示
      - 生データ（raw）の折りたたみ表示
    """
    st.title("PromptGrade - プロンプト簡易評価")

    # ------------------ 入力エリア ------------------
    st.header("入力")
    # テキスト入力ウィジェット（評価対象のプロンプト）
    prompt_text = st.text_area("評価したいプロンプトを入力してください", height=200)

    # モデルと temperature の簡易設定（将来的に拡張可能）
    model = st.selectbox("モデル", options=["gpt-4", "gpt-4o", "gpt-3.5-turbo"], index=0)
    temperature = st.slider("temperature", 0.0, 1.0, 0.0)

    # ユーザーが自身の OpenAI API キーを入力できる（任意）。入力はパスワード形式で隠される。
    api_key = st.text_input("(任意) OpenAI API キーを入力 (有効にするとそのキーが使われます)", type="password")

    # モックを強制的に使うかどうかのオプション
    use_mock = st.checkbox("モックを強制使用する（API 呼び出しを行わない）", value=False)

    # ------------------ 実行ボタン ------------------
    if st.button("評価する"):
        # 実行中のユーザーにフィードバックを表示
        with st.spinner("評価中..."):
            try:
                # grade_prompt の引数にユーザーの API キーとモックフラグを渡す
                result = grade_prompt(prompt_text, model=model, temperature=temperature, use_mock=use_mock, user_api_key=(api_key or None))
            except Exception as e:
                # 万が一の例外は画面に表示して処理を中断
                st.error(f"評価中にエラーが発生しました: {e}")
                result = None

        # ------------------ 結果表示 ------------------
        if result is None:
            st.warning("結果が取得できませんでした。エラーメッセージを確認してください。")
        else:
            st.subheader("評価結果")
            # スコアは浮動小数点数が来る想定。安全のため例外処理をする。
            try:
                score_val = float(result.get("score", 0.0))
                st.metric(label="Score", value=f"{score_val:.1f}")
            except Exception:
                st.write("Score:", result.get("score"))

            # フィードバック本文を表示
            st.write("フィードバック:")
            st.info(result.get("feedback", "(フィードバックがありません)"))

            # 生データは折りたたみで表示（開発時のデバッグ用）
            with st.expander("生データ / デバッグ情報（クリックで展開）"):
                st.write(result.get("raw", {}))

            # 追加ヒントや次のアクション
            st.caption("ヒント: スコアに納得がいかない場合は、プロンプトに目的・制約・期待結果をより具体的に書いてみてください。")
