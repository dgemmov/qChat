from cryptography.fernet import Fernet
from src.crypto import key_generation
# Main code of encryption and decryption will be soon ( now 10:00 PM 05.27.2026 )

cipher = None

def generateKey():
     global cipher
     key = Fernet.generate_key().decode()
     cipher = Fernet(key.encode())
     return key

def returnEncrypted(data: str):
    if cipher is None:
        print("Cipher is not created!")
        return None

    encrypted_bytes = cipher.encrypt(data.encode())
    return encrypted_bytes

def returnDecrypted(data: bytes):
    if cipher is None:
        print("Cipher is not created!")
        return None

    decrypted_bytes = cipher.decrypt(data)
    return decrypted_bytes.decode()