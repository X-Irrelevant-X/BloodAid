import sqlite3
import bcrypt
from encryption import encrypt_data  # Assuming this is for encrypting the name and email

DB_PATH = 'zDB.sqlite3'

def migrate_admin_data_to_encrypted():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Select all admins
    cursor.execute("SELECT admin_name, admin_email, pass FROM admin")
    admins = cursor.fetchall()

    print(f"Number of admins: {len(admins)}")

    for admin in admins:
        admin_name, admin_email, password = admin

        print(f"Admin: {admin_name}\n Admin Email: {admin_email}\n Password: {password}")

        # Encrypt name and email (assuming encrypt_data handles this)
        encrypted_name = encrypt_data(admin_name)
        encrypted_email = encrypt_data(admin_email)

        print(f"Encrypted Name: {encrypted_name}\n Encrypted Email: {encrypted_email}")

        # Hash the password using bcrypt if it's plain text
        if not password.startswith('$2y$'):  # Check if it's not bcrypt hashed
            print(f"Password for {admin_name} is not hashed. Hashing now...")
            # Hashing with bcrypt (default cost factor is 12, but we want 10)
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))  # cost factor 10
        else:
            hashed_password = password  # Already bcrypt hashed, no change
            print(f"Password for {admin_name} is already bcrypt hashed.")

        # Update the admin data with encrypted name, email, and bcrypt hashed password
        cursor.execute("""
            UPDATE admin
            SET admin_name = ?, admin_email = ?, pass = ?
            WHERE admin_name = ?
        """, (encrypted_name, encrypted_email, hashed_password.decode('utf-8'), admin_name))

    # Commit changes and close the connection
    conn.commit()

    # Check the updated data
    cursor.execute("SELECT * FROM admin")
    rows = cursor.fetchall()

    print(f"Found {len(rows)} admin(s) in the database.")
    for row in rows:
        print(row)

    conn.close()

    print("Migration complete. Admins are now encrypted and passwords hashed with bcrypt.")

# Run the migration
migrate_admin_data_to_encrypted()
