from cryptography.fernet import Fernet
from werkzeug.security import *
import os


FERNET_KEY = b'tjDmLEm-WwF5nPJuoTDIp9vyyv9AKp6_iY_t_KFAa7Q='
fernet = Fernet(FERNET_KEY)

def encrypt_data(data):
    """Encrypt sensitive data before storage"""
    if data is None:
        return None
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt data for display/use"""
    if data is None:
        return None
    try:
        return fernet.decrypt(data.encode()).decode()
    except:
        return data  # Return original if decryption fails

def hash_password(password):
    """Generate a secure password hash"""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Verify a password against its hash"""
    return check_password_hash(hashed_password, password)