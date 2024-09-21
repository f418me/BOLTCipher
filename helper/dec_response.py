from base64 import b64encode, b64decode

from Crypto.Cipher import AES
import binascii

hex_key = '6b382c0396df9847fed8695b6fbdfe237881020ea34a30c261466a4f03e84849'
encrypted_content_b64 = 'j1iFCcQb0AEKGdiyy4bBsXylZA0d6YpmlSQCQ7R/21q5'

# we us the first 16 bytes of the key as the iv
iv_hex = hex_key[:32]

key = binascii.unhexlify(hex_key)
iv = binascii.unhexlify(iv_hex)
encrypted_text = b64decode(encrypted_content_b64)


print(f"DECRYPTING")
print(f"encrypted text: {encrypted_text}")

cipher = AES.new(key, AES.MODE_CFB, iv)
decrypted_text = cipher.decrypt(encrypted_text).decode()
print(f"decrypted content: {decrypted_text}")


