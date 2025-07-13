from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20
import binascii
import os

# 256-Bit-Schlüssel (32 Byte)
hex_key = 'd6d1ad27df5bace05d9fd48216dd2b5ddc03b8d537058f8343b8b9e47afe551d'
key = binascii.unhexlify(hex_key)

# 64-Bit-Nonce (8 Byte) – zufällig generiert
nonce = os.urandom(8)

print(f"Nonce: {binascii.hexlify(nonce).decode()}")

original_text = "This is the content of the Plan B"
data = original_text.encode()

# Verschlüsseln mit ChaCha20
cipher = ChaCha20.new(key=key, nonce=nonce)
encrypted_text = cipher.encrypt(data)

# Ausgabe in Hex und Base64
encrypted_text_hex = binascii.hexlify(encrypted_text).decode()
encrypted_text_b64 = b64encode(encrypted_text).decode()

print(f"Encrypted Text HEX: {encrypted_text_hex}")
print(f"Encrypted Text Base64: {encrypted_text_b64}")

# Entschlüsseln mit ChaCha20
cipher = ChaCha20.new(key=key, nonce=nonce)  # Gleiche Nonce für Entschlüsselung
decrypted_text = cipher.decrypt(encrypted_text).decode()

print(f"Decrypted Text: {decrypted_text}")
