import os
from cryptography.fernet import Fernet

try:
    from constants.gitignore import data
    ENCRYPTION_KEY = data["ENCRYPTION_KEY"]
except:
    ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY']
    

def get_key():
    return Fernet.generate_key()

def encrypt(str, key=ENCRYPTION_KEY):
    fernet = Fernet(key.encode())
    return fernet.encrypt(str.encode())

def decrypt(encrypt_str, key=ENCRYPTION_KEY):
    fernet = Fernet(key.encode())
    return fernet.decrypt(encrypt_str).decode()


if __name__ == "__main__":
    key = Fernet.generate_key()
    print(key)