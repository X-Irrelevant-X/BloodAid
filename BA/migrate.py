import sqlite3
from encryption import encrypt_data
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'zDB.sqlite3'

def migrate_admin_data_to_encrypted():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all admins from the database
    cursor.execute("SELECT admin_name, admin_email, pass FROM admin")
    admins = cursor.fetchall()
    print(f"Number of admins: {len(admins)}")

    for admin in admins:
        admin_name, admin_email, password = admin

        print(f"Admin: {admin_name}\n Admin Email: {admin_email}\n Password: {password}")

        # Encrypt admin name and email
        encrypted_name = encrypt_data(admin_name)
        encrypted_email = encrypt_data(admin_email)
        hashed_password = generate_password_hash(password)

        print(f"Encrypted Name: {encrypted_name}\n Encrypted Email: {encrypted_email}\n Hashed Password: {hashed_password}")

    

        # Update the admin record with the encrypted name, email, and hashed password
        cursor.execute("""
            UPDATE admin
            SET admin_name = ?, admin_email = ?, pass = ?
            WHERE admin_name = ?
        """, (encrypted_name, encrypted_email, hashed_password, admin_name))

    conn.commit()

    # Verify migration
    cursor.execute("SELECT * FROM admin")
    rows = cursor.fetchall()

    print(f"Found {len(rows)} admin(s) in the database.")
    for row in rows:
        print(row)

    conn.close()
    print("Migration complete. Admins are now encrypted and passwords hashed.")

# Run the migration
migrate_admin_data_to_encrypted()
