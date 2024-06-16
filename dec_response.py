from base64 import b64decode

from Crypto.Cipher import AES
import binascii

hex_key = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
key = binascii.unhexlify(hex_key)

iv_hex="d8a3c76cb529c291a57e826008dbb9e9"
iv = binascii.unhexlify(iv_hex)

encrypted_content_b64 = "PahdlRxsYm7frzNqpaSrDTk="
encrypted_text = b64decode(encrypted_content_b64)

cipher = AES.new(key, AES.MODE_CFB, iv)
decrypted_text = cipher.decrypt(encrypted_text).decode()
print(f"decrypted content: {decrypted_text}")

