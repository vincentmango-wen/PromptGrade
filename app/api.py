# grade_prompt の軽量モック実装
# 初心者向けコメント付き

def grade_prompt(prompt_text: str, model: str = "gpt-4", temperature: float = 0.0):
    """
    プロンプト（文字列）を受け取り、評価のモック結果を返す関数。
    実運用ではここで OpenAI API 呼び出しを行うが、まずはモックで動作確認する。

    引数:
      prompt_text: ユーザーが入力したプロンプト
      model: 使用モデル名（UI で選べるが、モックでは影響なし）
      temperature: モデルの温度（モックでは影響なし）

    返り値（辞書）:
      {
        "score": float (0.0-100.0),
        "feedback": str (改善案),
        "raw": dict (元の生データ / 将来的に API レスポンスを格納)
      }
    """
    # とても単純な評価ロジック（文字数ベース）。本物の LLM 評価の代わり。
    length = len(prompt_text.strip())
    if length == 0:
        return {"score": 0.0, "feedback": "プロンプトが空です。具体的な指示を入力してください。", "raw": {}}
    # 文字数に応じて仮スコアを計算（最大 100）
    score = min(100.0, float(length) * 2.0)
    feedback = "良い開始です。" if score >= 60 else "もう少し具体的に目的や制約を明示してください。"
    return {"score": score, "feedback": feedback, "raw": {"length": length}}
