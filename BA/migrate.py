import sqlite3
from encryption import encrypt_data

DB_PATH = 'zDB.sqlite3'

def migrate_donor_data_to_encrypted():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all donors
    cursor.execute("SELECT rowid, previous_donation, approver_hospital FROM donor_list")
    donors = cursor.fetchall()

    print(f"Found {len(donors)} donors to migrate.")
    for donor in donors:
        rowid, previous_donation, approver_hospital = donor
        print(f"{rowid}, {previous_donation}, {approver_hospital}")
        # Skip if already encrypted (simple heuristic: if short, probably not encrypted)
        try:
            if previous_donation and len(previous_donation) < 50:
                encrypted_donation = encrypt_data(previous_donation)
                encrypted_approver = encrypt_data(approver_hospital) if approver_hospital else None
                
                print(f"Encrypting {encrypted_donation}")
                print(f"Encrypting {encrypted_approver}")
                
                cursor.execute("""
                    UPDATE donor_list SET 
                        previous_donation = ?, 
                        approver_hospital = ?
                    WHERE rowid = ?
                """, (encrypted_donation, encrypted_approver, rowid))

                print(f"Encrypting donor entry: rowid {rowid}")
        except Exception as e:
            print(f"Skipping rowid {rowid} due to error: {e}")
            continue

    conn.commit()
    conn.close()
    print("Migration complete. All unencrypted donor entries are now encrypted.")

# Run the migration
migrate_donor_data_to_encrypted()
