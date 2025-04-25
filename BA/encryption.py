from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

ENV_FILE = ".env"


if not os.path.exists(ENV_FILE):
    with open(ENV_FILE, "w") as f:
        f.write("#Generated Fernet KEY:\n")


load_dotenv()


FERNET_KEY = os.getenv("FERNET_KEY")


if not FERNET_KEY:
    new_key = Fernet.generate_key().decode()
    
    with open(ENV_FILE, "a") as f:
        f.write(f"\nFERNET_KEY={new_key}\n")
    
    FERNET_KEY = new_key

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data):
    if data is None:
        return None
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data):
    if data is None:
        return None
    try:
        return fernet.decrypt(data.encode()).decode()
    except:
        data = None
        return data
