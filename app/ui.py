import streamlit as st
from app.api import grade_prompt
from app import storage
import os
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
