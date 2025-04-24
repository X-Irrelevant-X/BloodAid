import sqlite3
from werkzeug.security import *

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


def user_exists_by_contact(contact):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT contact FROM user_list WHERE contact = ?", (contact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def submit_report(reported_by, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO report_box (reported_by, donor_contact, report_box) VALUES (?, ?, ?)",
        (reported_by, contact, reason)
    )
    conn.commit()
    conn.close()

def get_user_password(username):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("SELECT pass FROM user_list WHERE username=?", (username,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else None

def update_user_password(username, new_password_hash):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("UPDATE user_list SET pass=? WHERE username=?", (new_password_hash, username))
    db.commit()
    db.close()

def delete_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_list WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_trusted_hospitals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trusted_hospitals")
    hospitals = cursor.fetchall()
    conn.close()
    return hospitals

def is_trusted_hospital(hospital_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT hospital_name FROM trusted_hospitals WHERE hospital_name = ?", (hospital_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def is_already_donor(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donor_list WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_donor(username, donation_date, approver_hospital):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donor_list (username, previous_donation, approver_hospital) VALUES (?, ?, ?)",
                   (username, donation_date, approver_hospital))
    conn.commit()
    conn.close()
    

def insert_blood_request(request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO blood_requests 
                      (request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason))
    conn.commit()
    conn.close()

def get_all_blood_requests():
    conn = sqlite3.connect(DB_PATH)
    requests = conn.execute('SELECT * FROM blood_requests').fetchall()
    conn.close()
    return requests

def get_donor_list():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT u.name, u.age, u.blood_group, u.contact, u.police_station, u.city
        FROM donor_list d
        INNER JOIN user_list u ON d.username = u.username
    """
    cursor.execute(query)
    donors = cursor.fetchall()
    conn.close()
    return donors