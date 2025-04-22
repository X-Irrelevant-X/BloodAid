import sqlite3

DB_PATH = 'zDB.sqlite3'

def insert_user(data):
    conn = sqlite3.connect(DB_PATH)
    query = '''
        INSERT INTO user_list 
        (username, name, contact, email, pass, age, blood_group, NID, gender, police_station, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn.execute(query, (
        data['username'], data['name'], data['contact'], data['email'],
        data['password'], data['age'], data['blood_group'], data['nid'],
        data['gender'], data['police_station'], data['city']
    ))
    conn.commit()
    conn.close()

def check_duplicate_fields(username, email, nid, contact):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    errors = {}
    if cursor.execute("SELECT 1 FROM user_list WHERE username = ?", (username,)).fetchone():
        errors['u'] = "  *User Name Exists! Create another one."
    if cursor.execute("SELECT 1 FROM user_list WHERE email = ?", (email,)).fetchone():
        errors['e'] = "  *Email Exists! Use another one."
    if cursor.execute("SELECT 1 FROM user_list WHERE NID = ?", (nid,)).fetchone():
        errors['n'] = "  *NID Exists!"
    if cursor.execute("SELECT 1 FROM user_list WHERE contact = ?", (contact,)).fetchone():
        errors['c'] = "  *Contact Exists! Use another one."

    conn.close()
    return errors


def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_list WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user


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

