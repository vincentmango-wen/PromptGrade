import streamlit as st
from app.api import grade_prompt
import json
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

    # ------------------ 設定パネル ------------------
    # サイドバーでモデルや API キー、モック指定を先に決めておく
    st.sidebar.header('設定')
    model = st.sidebar.selectbox("モデル", options=["gpt-4", "gpt-4o", "gpt-3.5-turbo"], index=0)
    temperature = st.sidebar.slider("temperature", 0.0, 1.0, 0.0)
    api_key = st.sidebar.text_input("(任意) OpenAI API キーを入力 (有効にするとそのキーが使われます)", type="password")
    use_mock = st.sidebar.checkbox("モックを強制使用する（API 呼び出しを行わない）", value=False)

    # ------------------ 入力エリア ------------------
    st.header("入力")
    prompt_text = st.text_area("評価したいプロンプトを入力してください", height=200)

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
                score_val = float(result.get("total_score", 0.0))
                st.metric(label="total_score", value=f"{score_val:.1f}")
            except Exception:
                st.write("Score:", result.get("total_score"))

            # フィードバック本文を整形して表示
            st.write("フィードバック:")
            feedback = result.get("feedback")
            if not feedback:
                st.info("(フィードバックがありません)")
            else:
                # フィードバックがリストの場合: 各要素を番号付きで表示
                if isinstance(feedback, list):
                    for idx, item in enumerate(feedback, start=1):
                        # 要素が dict の場合は key: value を繋げて1行にする
                        if isinstance(item, dict):
                            parts = [f"{k}：{v}" for k, v in item.items()]
                            st.info(f"改善ポイント{idx}：" + " / ".join(parts))
                        else:
                            # 文字列やその他の型はそのまま表示
                            st.info(f"改善ポイント{idx}：{item}")

                # フィードバックが dict の場合: key: value を行ごとに表示
                elif isinstance(feedback, dict):
                    for k, v in feedback.items():
                        st.info(f"{k}：{v}")

                # 文字列の場合は改行で分割して可能なら番号を付与
                elif isinstance(feedback, str):
                    # 例: "改善ポイント1\n改善ポイント2" のような場合は行ごとに表示
                    lines = [ln.strip() for ln in feedback.splitlines() if ln.strip()]
                    if len(lines) > 1:
                        for idx, ln in enumerate(lines, start=1):
                            # 既に「：」が含まれていればそのまま表示
                            if '：' in ln or ':' in ln:
                                st.info(ln)
                            else:
                                st.info(f"改善ポイント{idx}：{ln}")
                    else:
                        st.info(feedback)

                else:
                    # 不明な型は安全に文字列化して表示
                    st.info(str(feedback))
            # 改善案（examples）があれば表示
            examples = result.get("examples")
            if examples:
                st.write("改善案:")
                if isinstance(examples, list):
                    for idx, ex in enumerate(examples, start=1):
                        st.info(f"改善案{idx}：{ex}")
                else:
                    st.info(str(examples))


            # （履歴保存機能は無効化されています）
            st.caption("履歴の保存/ダウンロード機能は現在無効化されています。")

            # 追加ヒントや次のアクション
            st.caption("ヒント: スコアに納得がいかない場合は、プロンプトに目的・制約・期待結果をより具体的に書いてみてください。")

            # コピー用の小さな JavaScript を埋める（クリップボードへコピー）
            if st.button("プロンプトをコピー"):
                # st.write で JS を実行してクリップボードにコピーする
                js = f"navigator.clipboard.writeText({json.dumps(prompt_text)}).then(()=>{{alert('コピーしました');}})"
                st.components.v1.html(f"<script>{js}</script>", height=0)



    # 履歴ダウンロードは削除されました

    # 履歴一覧表示は削除されました
