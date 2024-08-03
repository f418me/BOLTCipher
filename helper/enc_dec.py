from base64 import b64encode, b64decode

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import binascii

hex_key = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
key = binascii.unhexlify(hex_key)

iv = get_random_bytes(16)
iv_hex = iv.hex()



print(f"initialice vector: {iv_hex}")
original_text = "this is the original text"
data = original_text.encode()

# Verschlüssele den Original-Text im CFB-Modus
cipher = AES.new(key, AES.MODE_CFB, iv)
encrypted_text = cipher.encrypt(data)
print(f"encrypted text: {encrypted_text}")
encrypted_text_hex = binascii.hexlify(encrypted_text).decode()
print(f"encrypted Text HEX: {encrypted_text_hex}")
encrypted_text_b64 = b64encode(encrypted_text).decode()
print(f"encrypted Text Base64: {encrypted_text_b64}")

encrypted_text = b64decode(encrypted_text_b64)

# Entschlüssele den verschlüsselten Text im CFB-Modus
cipher = AES.new(key, AES.MODE_CFB, iv)
decrypted_text = cipher.decrypt(encrypted_text).decode()
print(f"decrypted text: {decrypted_text}")

