import streamlit as st
from app.api import grade_prompt
from app import storage
import os
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
    # サンプルプロンプト（初心者がすぐ試せる例）
    samples = {
        '顧客対応（簡潔）': "ユーザーが注文状況を尋ねるときの丁寧で簡潔な返信を作ってください。",
        '要約（会議メモ）': "以下の会議メモを3行で要約してください: ...",
        'コード補完（Python）': "この関数を効率化する最短の Python コードを書いてください: def foo(x):",
    }
    sample_key = st.selectbox('サンプルプロンプトを選択', options=['-- なし --'] + list(samples.keys()))
    # テキスト入力ウィジェット（評価対象のプロンプト）
    if sample_key and sample_key != '-- なし --':
        # 選択されたサンプルを初期値に入れる
        prompt_text = st.text_area("評価したいプロンプトを入力してください", value=samples[sample_key], height=200)
    else:
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

            # 保存ボタン
            if st.button("この結果を履歴に保存する"):
                try:
                    entry = storage.save_result(prompt_text, model, temperature, result)
                    st.success("履歴に保存しました。")
                    st.write(entry)
                except Exception as e:
                    st.error(f"履歴保存に失敗しました: {e}")

            # 追加ヒントや次のアクション
            st.caption("ヒント: スコアに納得がいかない場合は、プロンプトに目的・制約・期待結果をより具体的に書いてみてください。")

            # コピー用の小さな JavaScript を埋める（クリップボードへコピー）
            if st.button("プロンプトをコピー"):
                # st.write で JS を実行してクリップボードにコピーする
                js = f"navigator.clipboard.writeText({json.dumps(prompt_text)}).then(()=>{{alert('コピーしました');}})"
                st.components.v1.html(f"<script>{js}</script>", height=0)

    # ------------------ 設定パネル ------------------
    st.sidebar.header('設定')
    default_model = st.sidebar.selectbox('デフォルトモデル', options=["gpt-4", "gpt-4o", "gpt-3.5-turbo"], index=0)
    default_temp = st.sidebar.slider('デフォルト temperature', 0.0, 1.0, 0.0)

    # ------------------ 履歴ダウンロード ------------------
    st.header("履歴ダウンロード")
    try:
        hist_path = storage._history_file_path()
        if os.path.exists(hist_path):
            with open(hist_path, 'r', encoding='utf-8') as f:
                data = f.read()
            st.download_button('履歴を JSON としてダウンロード', data=data, file_name='history.json', mime='application/json')
        else:
            st.info('ダウンロード可能な履歴ファイルがありません。')
    except Exception as e:
        st.error(f'履歴の読み取りに失敗しました: {e}')

    # ------------------ 履歴タブ ------------------
    st.header("履歴")
    try:
        entries = storage.list_history()
    except Exception:
        entries = []

    if not entries:
        st.info("保存された履歴はまだありません。")
    else:
        # 簡単な履歴一覧表示（先頭の数件）
        for e in entries:
            with st.expander(f"{e.get('timestamp')} - {e.get('prompt')[:60]}..."):
                st.write("モデル:", e.get('model'))
                st.write("temperature:", e.get('temperature'))
                st.write("結果:")
                st.write(e.get('result'))
                if st.button(f"削除: {e.get('id')}"):
                    ok = storage.delete_entry(e.get('id'))
                    if ok:
                        st.success("削除しました。ページを再読み込みしてください（または再実行）。")
                    else:
                        st.error("削除に失敗しました。")
