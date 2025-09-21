# Streamlit アプリ起点ファイル
# 簡単な UI を起動します

from app.ui import render_ui

if __name__ == "__main__":
    # Streamlit は通常このファイルを直接実行するより
    # `streamlit run app.py` で起動しますが、開発中のためこの構成にしています。
    render_ui()
