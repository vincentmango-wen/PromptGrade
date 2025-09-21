"""
JSON の履歴（data/history.json）を SQLite に移行するスクリプト
使い方:
  python scripts/migrate_to_sqlite.py
"""
import os
import json
from app import storage
from app import db


def main():
    json_path = storage._history_file_path()
    if not os.path.exists(json_path):
        print('履歴 JSON が見つかりません:', json_path)
        return

    # DB を初期化
    db.init_db()

    entries = storage.list_history()
    for e in entries:
        try:
            db.insert_entry(e)
        except Exception as ex:
            print('挿入失敗', e.get('id'), ex)

    print('移行完了。移行した件数:', len(entries))


if __name__ == '__main__':
    main()
