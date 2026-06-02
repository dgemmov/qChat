import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import InvalidToken
from src.crypto import key_generation

def generateRoomKey():
    room_key = Fernet.generate_key()
    key_generation.key = room_key.decode()
    key_generation.cipher = Fernet(room_key)

def setRoomKey(room_key_bytes: bytes):
    key_generation.key = room_key_bytes.decode()
    key_generation.cipher = Fernet(room_key_bytes)

def generateDHKeys() -> tuple:
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_bytes, private_key  # send these bytes over the network

def deriveTemporaryKey(peer_public_bytes: bytes, private_key) -> Fernet:
    """Creates a TEMPORARY cipher used only to securely transfer the room key."""
    try:
        peer_public_key = serialization.load_pem_public_key(peer_public_bytes)
        shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
        
        # derive clean 32 bytes for fernet via hkdf
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'chat-crypto-key',
        ).derive(shared_secret)
        
        temp_fernet_key = base64.urlsafe_b64encode(derived_key)
        return Fernet(temp_fernet_key)
    except Exception as e:
        print(f"[Crypto] Failed to generate temporary key: {e}")
        return None

def returnEncrypted(data: str):
    if key_generation.cipher is None: return None
    return key_generation.cipher.encrypt(data.encode())

def returnDecrypted(data: bytes):
    if key_generation.cipher is None: return data.decode(errors='ignore')
    try:
        return key_generation.cipher.decrypt(data).decode()
    except (InvalidToken, ValueError):
        return data.decode(errors='ignore')