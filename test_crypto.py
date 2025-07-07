from utils.security import encrypt_password, decrypt_password

test_pw = "my-secret"
enc = encrypt_password(test_pw)
dec = decrypt_password(enc)

print(f"Encrypted: {enc}")
print(f"Decrypted: {dec}")
