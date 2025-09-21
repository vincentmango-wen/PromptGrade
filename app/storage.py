"""
app.storage - 履歴保存（JSON）ユーティリティ

このモジュールは評価結果をローカルの JSON ファイルに保存し、一覧取得・削除を提供します。
初心者向けに日本語コメントを多めにしています。
"""

import os
import json
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime


def _history_file_path() -> str:
  """履歴ファイルのフルパスを返す。ファイルとディレクトリがなければ作成する。"""
  base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
  data_dir = os.path.join(base_dir, 'data')
  if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)
  return os.path.join(data_dir, 'history.json')


def _read_all() -> List[Dict[str, Any]]:
  """履歴ファイルを読み込んでリストを返す。存在しなければ空リストを返す。"""
  path = _history_file_path()
  if not os.path.exists(path):
    return []
  try:
    with open(path, 'r', encoding='utf-8') as f:
      return json.load(f)
  except Exception:
    # 読み取り失敗時は空にフォールバック
    return []


def _write_all(items: List[Dict[str, Any]]) -> None:
  """リストをファイルに書き込む（上書き）。"""
  path = _history_file_path()
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)


def save_result(prompt: str, model: str, temperature: float, result: Dict[str, Any]) -> Dict[str, Any]:
  """新しい履歴エントリを作成して保存し、そのエントリを返す。"""
  entries = _read_all()
  entry = {
    'id': str(uuid4()),
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'prompt': prompt,
    'model': model,
    'temperature': temperature,
    'result': result,
  }
  entries.insert(0, entry)  # 新しいものを先頭に
  _write_all(entries)
  return entry


def list_history() -> List[Dict[str, Any]]:
  """全履歴を取得して返す（新しい順）。"""
  return _read_all()


def get_entry(entry_id: str) -> Optional[Dict[str, Any]]:
  """ID に一致するエントリを返す。見つからなければ None。"""
  for e in _read_all():
    if e.get('id') == entry_id:
      return e
  return None


def delete_entry(entry_id: str) -> bool:
  """ID に一致するエントリを削除する。削除できれば True、存在しなければ False。"""
  entries = _read_all()
  new_entries = [e for e in entries if e.get('id') != entry_id]
  if len(new_entries) == len(entries):
    return False
  _write_all(new_entries)
  return True
