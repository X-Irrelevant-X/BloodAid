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


def get_user_list():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT username, name, age, blood_group, contact, police_station, city
        FROM user_list
    """
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()

    decrypted_users = []
    for user in users:
        try:
            decrypted_user = {
                'username': user[0],
                'name': decrypt_data(user[1]),
                'age': decrypt_data(user[2]),
                'blood_group': decrypt_data(user[3]),
                'contact': decrypt_data(user[4]),
                'police_station': decrypt_data(user[5]),
                'city': decrypt_data(user[6]),
            }
            decrypted_users.append(decrypted_user)
        except Exception as e:
            print(f"Skipping user due to decryption error: {e}")
            continue

    return decrypted_users


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
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM user_list WHERE username = ?', (username,)).fetchone()
    conn.close()

    if not user:
        return None

    return {
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
        'city': decrypt_data(user[10]),
    }


def get_admin_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT admin_name, admin_email, pass FROM admin")
    admins = cursor.fetchall()

    for admin in admins:
        admin_name, admin_email, password = admin
        decrypted_admin_name = decrypt_data(admin_name)

        if decrypted_admin_name == username:
            admin_email = decrypt_data(admin_email)
            return {
                'admin_name': decrypted_admin_name,
                'admin_email': admin_email,
                'pass': password
            }

    conn.close()
    return None


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


def get_username_by_contact(donor_contact):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT username, contact FROM user_list")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        decrypted_contact = decrypt_data(user['contact'])
        if decrypted_contact == donor_contact:
            return user['username']
    
    return None 


def submit_report(reported_by, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    encrypted_contact = encrypt_data(contact)
    encrypted_reason = encrypt_data(reason)
    cursor.execute(
        "INSERT INTO reports (reported_by, donor_contact, report_box) VALUES (?, ?, ?)",
        (reported_by, encrypted_contact, encrypted_reason)
    )
    conn.commit()
    conn.close()


def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT reported_by, donor_contact, report_box FROM reports")
    reports = cursor.fetchall()
    conn.close()

    decrypted_reports = []
    for report in reports:
        reported_by = report['reported_by']
        donor_contact = decrypt_data(report['donor_contact'])
        report_box = decrypt_data(report['report_box'])
        
        report_username = get_username_by_contact(donor_contact)
        
        decrypted_reports.append({
            'reported_by': reported_by,
            'username': report_username,
            'report_box': report_box
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


def remove_donor(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM donor_list WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def get_donor_list():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT u.username, u.name, u.age, u.blood_group, u.contact, u.police_station, u.city
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
                'username': donor[0],
                'name': decrypt_data(donor[1]),
                'age': decrypt_data(donor[2]),
                'blood_group': decrypt_data(donor[3]),
                'contact': decrypt_data(donor[4]),
                'police_station': decrypt_data(donor[5]),
                'city': decrypt_data(donor[6]),
            }
            decrypted_donors.append(decrypted_donor)
        except Exception as e:
            print(f"Skipping donor due to decryption error: {e}")
            continue
    
    return decrypted_donors


def delete_donor(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM donor_list WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    
    
def insert_blood_request(request_by, name, age, blood_group, quantity, hospital_unit, hospital_name, date_needed, contact, reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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


def is_user_donor(username):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM donor_list WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


def add_trusted_hospital(name, email, hotline, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trusted_hospitals (hospital_name, hospital_mail, hotline, location)
        VALUES (?, ?, ?, ?)
    """, (name, email, hotline, location))

    conn.commit()
    conn.close()


def get_trusted_hospitals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hospital_name, hospital_mail, hotline, location
        FROM trusted_hospitals
        ORDER BY hospital_name ASC
    """)
    
    hospitals = cursor.fetchall()
    conn.close()
    
    return [{'name': row[0], 'email': row[1], 'hotline': row[2], 'location': row[3]} for row in hospitals]


def delete_trusted_hospital_by_email(hospital_mail):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trusted_hospitals WHERE hospital_mail = ?", (hospital_mail,))
    conn.commit()
    conn.close()


def add_campaign(venue, start_date, end_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO campaigns (venue, start_date, end_date) VALUES (?, ?, ?)",
        (venue, start_date, end_date)
    )
    conn.commit()
    conn.close()


def get_campaigns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        SELECT 
            c.venue, 
            c.start_date, 
            c.end_date, 
            h.location 
        FROM campaigns c
        JOIN trusted_hospitals h ON c.venue = h.hospital_name
        WHERE c.end_date >= ?
    ''', (current_date,))
    campaigns = cursor.fetchall()
    conn.close()
    return [{
        'venue': row[0],
        'start_date': row[1],
        'end_date': row[2],
        'location': row[3]
    } for row in campaigns]
    
    
def delete_campaign(venue, start_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM campaigns WHERE venue = ? AND start_date = ?",
        (venue, start_date)
    )
    conn.commit()
    conn.close()
