import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
API_KEY_FILE = "api_key.enc"


def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    generate_key()
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    return key


def save_api_key_prompt(api_key):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_api_key = cipher_suite.encrypt(api_key.encode())
    with open(API_KEY_FILE, "wb") as f:
        f.write(encrypted_api_key)


def get_api_key():
    if not os.path.exists(API_KEY_FILE):
        return None
    key = load_key()
    cipher_suite = Fernet(key)
    try:
        with open(API_KEY_FILE, "rb") as f:
            encrypted_api_key = f.read()
        decrypted_api_key = cipher_suite.decrypt(encrypted_api_key).decode()
        return decrypted_api_key
    except:
        return None
