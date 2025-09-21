"""
app.api - プロンプト評価ロジック

このファイルでは `grade_prompt()` を提供します。
 - 開発中はモック（ローカルの簡易ロジック）を返すことができます。
 - 実運用では環境変数またはユーザーが渡した API キーで OpenAI に問い合わせます。

初心者の方にも分かるように日本語コメントを多めに入れています。
"""

import os
import json
from typing import Optional, Dict, Any

try:
  # OpenAI ライブラリは optional（requirements.txt に入っていますが、無ければ import エラーを防ぐ）
  import openai
except Exception:
  openai = None

# 環境変数からデフォルトの API キーを読む
DEFAULT_OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def _mock_grade(prompt_text: str) -> Dict[str, Any]:
  """
  簡易モック評価関数（内部使用）
  - 文字数ベースでスコアを返す（0-100）
  - 開発中や API キーが無い場合のフォールバックとして使う
  """
  length = len(prompt_text.strip())
  if length == 0:
    return {"score": 0.0, "feedback": "プロンプトが空です。具体的な指示を入力してください。", "raw": {}}
  score = min(100.0, float(length) * 2.0)
  feedback = "良い開始です。" if score >= 60 else "もう少し具体的に目的や制約を明示してください。"
  return {"score": score, "feedback": feedback, "raw": {"length": length, "mock": True}}


def _extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
  """
  モデルが返すテキストの中から JSON 部分を抽出してパースするヘルパー。
  LLM はしばしば前後に説明を付与するため、最初に見つかった {...} ブロックを試す。
  成功すれば辞書を返し、失敗すれば None を返す。
  """
  # 単純な戦略: 最初の { から最後の } までを取ってみる（ネストに弱いが簡易実装）
  try:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
      return None
    candidate = text[start:end+1]
    return json.loads(candidate)
  except Exception:
    return None


def _validate_and_clamp_score(score_raw: Any) -> float:
  """
  スコアが数値として受け入れ可能か検証し、0.0-100.0 の範囲にクランプして返す。
  パースできない場合は 0.0 を返す。
  """
  try:
    s = float(score_raw)
  except Exception:
    return 0.0
  # 範囲でクランプ
  if s < 0.0:
    return 0.0
  if s > 100.0:
    return 100.0
  return s


def grade_prompt(prompt_text: str,
         model: str = "gpt-4",
         temperature: float = 0.0,
         use_mock: Optional[bool] = None,
         user_api_key: Optional[str] = None) -> Dict[str, Any]:
  """
  プロンプトを評価して結果を返すメイン関数。

  引数:
    prompt_text: 評価対象のプロンプト文字列
    model: 使用するモデル名（文字列）
    temperature: モデルの temperature（0.0-1.0）
    use_mock: True ならモックを強制使用、False なら必ず OpenAI 呼び出しを試みる、None ならキーの有無で自動判定
    user_api_key: UI から渡されたユーザーの API キー（あればこれを優先して使用）

  返り値（辞書）:
    {
    "score": float,
    "feedback": str,
    "raw": dict  # 実際の API レスポンスやデバッグ情報を入れる
    }

  実行方針:
    - use_mock が True の場合はローカルのモックを返す
    - OpenAI ライブラリが無い、または API キーが無い場合はモックを返す（安全策）
    - それ以外は OpenAI に問い合わせ、JSON をパースしてスコア/フィードバックを抽出する
  """
  # まず明示的なモックの要求があればそれを使う
  if use_mock is True:
    return _mock_grade(prompt_text)

  # API キーの決定（ユーザー指定 > 環境変数）
  api_key = user_api_key or DEFAULT_OPENAI_API_KEY

  # OpenAI クライアントが使えない場合や強制的にモックにしたい場合はモックを返す
  if openai is None:
    return {**_mock_grade(prompt_text), "raw": {"error": "openai library not installed", "mock": True}}
  if api_key is None and use_mock is not False:
    # キーが無い場合は安全にモックを返す
    return {**_mock_grade(prompt_text), "raw": {"error": "no api key provided", "mock": True}}

  # ここからは実際に OpenAI に問い合わせるロジック（API キーが存在する想定）
  # 注意: 実行環境により openai の API 呼び出し方法が変わる場合があります。
  try:
    openai.api_key = api_key

    # LLM に渡す指示（簡単な grader）
    system_prompt = (
      "あなたはプロンプト評価アシスタントです。与えられたプロンプトを" 
      "0.0〜100.0 のスコアで評価し、改善点を短く説明してください。" 
      "出力は JSON で {\"score\": number, \"feedback\": string} の形式のみを返してください。"
    )
    user_message = f"Evaluate the following prompt for quality and clarity:\n\n{prompt_text}"

    # 安全のため、簡易リトライを行う（最大 2 回）
    max_retries = 2
    last_exception = None
    for attempt in range(max_retries):
      try:
        # ChatCompletion を使って問い合わせる（API バージョンに応じて調整が必要な場合あり）
        # `request_timeout` を指定してタイムアウトを設定（秒）。openai パッケージによっては名前が異なる場合があります。
        resp = openai.ChatCompletion.create(
          model=model,
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
          ],
          temperature=temperature,
          max_tokens=500,
          request_timeout=15,
        )
        # 成功したらループを抜ける
        break
      except Exception as e:
        last_exception = e
        # 再試行前に短いバックオフ
        if attempt < max_retries - 1:
          import time
          time.sleep(1)
        else:
          # 最終試行で失敗したら例外を再送出して下流で処理する
          raise

    # レスポンスからテキストを取り出す
    text = ""
    try:
      # 通常は choices[0].message.content に結果が入る
      text = resp["choices"][0]["message"]["content"]
    except Exception:
      # 古い/別のレスポンス形式に対応
      text = str(resp)

    # 返ってきたテキストを JSON としてパースを試みる（モデルに JSON 出力を要求しているため期待される）
    parsed = _extract_json_from_text(text)
    if parsed is not None:
      # JSON が抽出できた場合はスコアを検証して返す
      score = _validate_and_clamp_score(parsed.get("score", 0.0))
      feedback = parsed.get("feedback", "(フィードバックなし)")
      return {"score": score, "feedback": feedback, "raw": {"response_text": text, "api_response": resp}}
    else:
      # パースに失敗したら、生のテキストから穏やかに結果を構築する
      return {"score": 0.0, "feedback": text, "raw": {"response_text": text, "api_response": resp}}

  except Exception as e:
    # ネットワークや API エラー時はモックでフォールバックし、エラー情報を raw に入れる
    mock = _mock_grade(prompt_text)
    # 例外情報をわかりやすく整形して追加
    mock["raw"]["error"] = str(e)
    # もし最後の例外オブジェクトがあれば追加情報として入れる
    if 'last_exception' in locals() and last_exception is not None:
      mock["raw"]["last_exception"] = str(last_exception)
    return mock
