"""
app.db - SQLite ラッパー

簡易的なラッパーを提供します:
- init_db(path)
- insert_entry(entry_dict)
- list_entries()
- get_entry(id)
- delete_entry(id)

初心者向けにコメントを多めにしています。
"""

import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'history.db'))


def init_db(db_path: Optional[str] = None) -> None:
    """データベースとテーブルを初期化する。"""
    path = db_path or DB_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                prompt TEXT,
                model TEXT,
                temperature REAL,
                result_json TEXT
            )
        ''')
        conn.commit()
    finally:
        conn.close()


def insert_entry(entry: Dict[str, Any], db_path: Optional[str] = None) -> None:
    """エントリを挿入する。entry の result は JSON 文字列として保存する。"""
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO history (id, timestamp, prompt, model, temperature, result_json)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (entry['id'], entry['timestamp'], entry['prompt'], entry.get('model'), entry.get('temperature'), json.dumps(entry.get('result', {}), ensure_ascii=False)))
        conn.commit()
    finally:
        conn.close()


def list_entries(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, timestamp, prompt, model, temperature, result_json FROM history ORDER BY timestamp DESC')
        rows = cur.fetchall()
        result = []
        for r in rows:
            result.append({
                'id': r[0],
                'timestamp': r[1],
                'prompt': r[2],
                'model': r[3],
                'temperature': r[4],
                'result': json.loads(r[5]) if r[5] else {}
            })
        return result
    finally:
        conn.close()


def get_entry(entry_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, timestamp, prompt, model, temperature, result_json FROM history WHERE id = ?', (entry_id,))
        r = cur.fetchone()
        if not r:
            return None
        return {
            'id': r[0],
            'timestamp': r[1],
            'prompt': r[2],
            'model': r[3],
            'temperature': r[4],
            'result': json.loads(r[5]) if r[5] else {}
        }
    finally:
        conn.close()


def delete_entry(entry_id: str, db_path: Optional[str] = None) -> bool:
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM history WHERE id = ?', (entry_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
