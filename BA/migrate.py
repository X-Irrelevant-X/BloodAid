import sqlite3
from encryption import encrypt_data

DB_PATH = 'zDB.sqlite3'

def migrate_user_data_to_encrypted():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute("SELECT username, name, contact, email, pass, age, blood_group, NID, gender, police_station, city FROM user_list")
    users = cursor.fetchall()

    for user in users:
        username, name, contact, email, password, age, blood_group, nid, gender, police_station, city = user

        # Check if fields are already encrypted by trying to decrypt them
        try:
            # Attempt to decrypt a field, if it succeeds, it's already encrypted
            decrypted_name = decrypt_data(name)
            decrypted_contact = decrypt_data(contact)
            decrypted_email = decrypt_data(email)
            decrypted_age = decrypt_data(age)
            decrypted_blood_group = decrypt_data(blood_group)
            decrypted_nid = decrypt_data(nid)
            decrypted_gender = decrypt_data(gender)
            decrypted_police_station = decrypt_data(police_station)
            decrypted_city = decrypt_data(city)

            # Skip already encrypted user
            continue  # Skip to the next user if decryption succeeds
        except:
            pass  # Continue if any decryption fails, which means the data is not encrypted yet

        # Encrypt fields
        encrypted_name = encrypt_data(name)
        encrypted_contact = encrypt_data(contact)
        encrypted_email = encrypt_data(email)
        encrypted_age = encrypt_data(age)
        encrypted_blood_group = encrypt_data(blood_group)
        encrypted_nid = encrypt_data(nid)
        encrypted_gender = encrypt_data(gender)
        encrypted_police_station = encrypt_data(police_station)
        encrypted_city = encrypt_data(city)

        # Update user record with encrypted values
        cursor.execute("""
            UPDATE user_list SET 
                name = ?, 
                contact = ?, 
                email = ?, 
                age = ?, 
                blood_group = ?, 
                NID = ?, 
                gender = ?, 
                police_station = ?, 
                city = ?
            WHERE username = ?
        """, (
            encrypted_name, encrypted_contact, encrypted_email,
            encrypted_age, encrypted_blood_group, encrypted_nid,
            encrypted_gender, encrypted_police_station, encrypted_city,
            username
        ))

        print(f"Encrypting user: {username}")

    conn.commit()
    conn.close()
    print("Migration complete. All unencrypted users are now encrypted.")


    
    
migrate_user_data_to_encrypted()

