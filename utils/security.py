import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# 🌍 Load environment variables (only affects local dev)
load_dotenv()

# 🔐 Retrieve FERNET_KEY from environment
fernet_key = os.getenv("FERNET_KEY")

# 🧪 Optional debug print
print(f"Loaded FERNET_KEY: {fernet_key}")

# 🧠 Validate that key exists
if not fernet_key:
    raise ValueError("FERNET_KEY is not set in the environment.")

# 🔒 Create Fernet instance
fernet = Fernet(fernet_key)


# 🔐 Encrypt plain-text password (returns encrypted string)
def encrypt_password(plain_text: str) -> str:
    return fernet.encrypt(plain_text.encode()).decode()


# 🔓 Decrypt encrypted password (returns original string)
def decrypt_password(encrypted_text: str) -> str:
    return fernet.decrypt(encrypted_text.encode()).decode()


# 🧪 Run this file directly to test encryption/decryption
if __name__ == "__main__":
    test_pw = "my-secret-password"
    encrypted = encrypt_password(test_pw)
    decrypted = decrypt_password(encrypted)

    print("\n🧪 Password Encryption Test")
    print(f"🔐 Encrypted: {encrypted}")
    print(f"🔓 Decrypted: {decrypted}")
