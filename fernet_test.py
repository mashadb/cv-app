from cryptography.fernet import Fernet

# 🔑 Fernet key (store this securely, e.g., in Azure App Settings)
key = b'7XnZJvYhP0L3g_JhzUARJjJJ0KpPMIx0lRGejQQ0S8Y='

# 🔧 Initialize Fernet
fernet = Fernet(key)

# ✅ STEP 1: Encrypt a plaintext string
plaintext = "MySuperSecretToken123"
encrypted = fernet.encrypt(plaintext.encode())
print("🔒 Encrypted:", encrypted.decode())

# ✅ STEP 2: Decrypt the encrypted string
try:
    decrypted = fernet.decrypt(encrypted).decode()
    print("🔓 Decrypted:", decrypted)
except Exception as e:
    print("❌ Decryption failed:", e)