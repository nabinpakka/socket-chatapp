import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cryptograher:
    def __init__(self, password, salt):
        self.password = password
        self.salt = salt

    def derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=self.salt,
            length=32,
            backend=default_backend()
        )
        return kdf.derive(self.password)
    def encrypt(self, message, key):
        iv = b'0123456789abcdef'  # IV (Initialization Vector) should be random and unique for each message
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
        return (iv + ciphertext)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:16]  # Extract IV from the first 16 bytes
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
        return plaintext.decode()