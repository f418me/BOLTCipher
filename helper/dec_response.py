from base64 import b64decode

from Crypto.Cipher import AES
import binascii

hex_key = '53eb8b9b168aa90a2c6fcc6ac0ef0dce358226934c5f02244b7d9ba413be67f0'
key = binascii.unhexlify(hex_key)

iv_hex="f658aa06e45b03d9a933caa5cad9d7e9"
iv = binascii.unhexlify(iv_hex)

encrypted_content_b64 = "Q9ZJeVZfTzeeNPNduOSS1TjAK3n7Vq7E+ZFQYBV9E/Qv"
encrypted_text = b64decode(encrypted_content_b64)

cipher = AES.new(key, AES.MODE_CFB, iv)
decrypted_text = cipher.decrypt(encrypted_text).decode()
print(f"decrypted content: {decrypted_text}")

