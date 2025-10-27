import sqlite3
import json

def main():
    import os
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'zDB.sqlite3'))
    print('db_path:', db_path, 'exists:', os.path.exists(db_path))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA database_list")
    print('db_list:', cur.fetchall())
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print('tables:', json.dumps(tables))
    for name in tables:
        cur.execute(f"PRAGMA table_info({name})")
        cols = cur.fetchall()
        print(name, json.dumps([f"{c[1]}:{c[2]}" for c in cols]))
    conn.close()

if __name__ == '__main__':
    main()
