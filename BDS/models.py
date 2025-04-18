import sqlite3

DB_PATH = 'zDB.sqlite3'

def get_user_count():
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute('SELECT COUNT(*) FROM user_list').fetchone()[0]
    conn.close()
    return count

def get_donor_count():
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute('SELECT COUNT(*) FROM donor_list').fetchone()[0]
    conn.close()
    return count

def get_hospital_count():
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute('SELECT COUNT(*) FROM trusted_hospitals').fetchone()[0]
    conn.close()
    return count
