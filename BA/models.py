import sqlite3
from werkzeug.security import *
from encryption import *
from datetime import *

DB_PATH = 'zDB.sqlite3'


def insert_user(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO user_list (username, name, contact, email, pass, age, blood_group, NID, gender, police_station, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            data['username'],
            encrypt_data(data['name']),
            encrypt_data(data['contact']),
            encrypt_data(data['email']),
            data['password'],  
            encrypt_data(data['age']),
            encrypt_data(data['blood_group']),
            encrypt_data(data['nid']),
            encrypt_data(data['gender']),
            encrypt_data(data['police_station']),
            encrypt_data(data['city'])
        )
    )

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

    user_data = {
        'username': user[0],
        'name': decrypt_data(user[1]),
        'contact': decrypt_data(user[2]),
        'email': decrypt_data(user[3]),
        'password': user[4],
        'age': decrypt_data(user[5]),
        'blood_group': decrypt_data(user[6]),
        'nid': decrypt_data(user[7]),
        'gender': decrypt_data(user[8]),
        'police_station': decrypt_data(user[9]),
        'city': decrypt_data(user[10])
    }

    conn.close()
    return user_data


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
    cursor.execute("SELECT contact FROM user_list")
    all_contacts = cursor.fetchall()
    conn.close()

    for (stored_contact,) in all_contacts:
        try:
            decrypted = decrypt_data(stored_contact)
        except:
            decrypted = stored_contact

        if decrypted == contact:
            return True
    return False



def submit_report(reported_by, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    encrypted_contact = encrypt_data(contact)
    encrypted_reason = encrypt_data(reason)
    cursor.execute(
        "INSERT INTO report_box (reported_by, donor_contact, report_box) VALUES (?, ?, ?)",
        (reported_by, encrypted_contact, encrypted_reason)
    )
    conn.commit()
    conn.close()


def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM report_box")
    reports = cursor.fetchall()
    conn.close()

    decrypted_reports = []
    for report in reports:
        decrypted_reports.append({
            'reported_by': decrypt_data(report['reported_by']),
            'donor_contact': decrypt_data(report['donor_contact']),
            'report_box': decrypt_data(report['report_box'])
        })

    return decrypted_reports


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
    
    encrypted_donation_date = encrypt_data(donation_date)
    encrypted_approver_hospital = encrypt_data(approver_hospital)

    cursor.execute("INSERT INTO donor_list (username, previous_donation, approver_hospital) VALUES (?, ?, ?)",
                   (username, encrypted_donation_date, encrypted_approver_hospital))
    conn.commit()
    conn.close()


def get_donor_list():
    import sqlite3
    from encryption import decrypt_data

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

    decrypted_donors = []
    for donor in donors:
        try:
            decrypted_donor = {
                'name': decrypt_data(donor[0]),
                'age': decrypt_data(donor[1]),
                'blood_group': decrypt_data(donor[2]),
                'contact': decrypt_data(donor[3]),
                'police_station': decrypt_data(donor[4]),
                'city': decrypt_data(donor[5]),
            }
            decrypted_donors.append(decrypted_donor)
        except Exception as e:
            print(f"Skipping donor due to decryption error: {e}")
            continue
    
    return decrypted_donors


def insert_blood_request(request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Encrypt sensitive fields
    name_enc = encrypt_data(name)
    age_enc = encrypt_data(age)
    blood_group_enc = encrypt_data(blood_group)
    quantity_enc = encrypt_data(quantity)
    hospital_unit_enc = encrypt_data(hospital_unit)
    hospital_name_enc = encrypt_data(hospital_name)
    date_needed_enc = encrypt_data(date_needed)
    contact_enc = encrypt_data(contact)
    reason_enc = encrypt_data(reason)

    cursor.execute('''INSERT INTO blood_requests 
                      (request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (request_by, name_enc, age_enc, blood_group_enc, quantity_enc,
                    hospital_unit_enc, hospital_name_enc, date_needed_enc,
                    contact_enc, reason_enc))
    
    conn.commit()
    conn.close()


def get_all_blood_requests():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    rows = cursor.execute('SELECT * FROM blood_requests').fetchall()
    conn.close()

    decrypted_requests = []
    for blood in rows:
        decrypted = {
            'id': blood[0],
            'request_by': blood[1],
            'name': decrypt_data(blood[2]),
            'age': decrypt_data(blood[3]),
            'blood_group': decrypt_data(blood[4]),
            'quantity': decrypt_data(blood[5]),
            'hospital_unit': decrypt_data(blood[6]),
            'hospital_name': decrypt_data(blood[7]),
            'date_needed': decrypt_data(blood[8]),
            'contact': decrypt_data(blood[9]),
            'reason': decrypt_data(blood[10]),
            'location': "Contact for Location"
        }
        decrypted_requests.append(decrypted)
    
    return decrypted_requests


def get_campaigns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    query = '''
        SELECT c.venue, c.start_date, c.end_date, h.location
        FROM campaigns c
        JOIN trusted_hospitals h ON c.venue = h.hospital_name
        WHERE c.end_date >= ?
    '''
    cursor.execute(query, (current_date,))
    campaigns = cursor.fetchall()
    conn.close()
    
    return [{
        'venue': row[0],
        'start_date': row[1],
        'end_date': row[2],
        'location': row[3]
    } for row in campaigns]