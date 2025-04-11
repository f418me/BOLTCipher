from base64 import b64decode
from Crypto.Cipher import ChaCha20
import binascii

# --- Inputs as Strings ---
# Replace these values with your actual data!

# 256-bit key (32 bytes) as hex string
key_hex_string = '0cfebc3a24f47fb635ab19f55c0c4c9d32a5ef4c859b83d3b7ac4fb96143e1ba'

# 64-bit nonce (8 bytes) as hex string
# Example: Must be the nonce used during encryption!
nonce_hex_string = '1cfa1980a0e84b3520422766' # <--- REPLACE THIS VALUE

# Encrypted text as Base64 string
# Example: Must be the encrypted text!
encrypted_text_b64_string = '8z6yCrKNQ5ShcKRoc9y2xp6STsTngYYh0T8eZ6tQstuQ' # <--- REPLACE THIS VALUE


# --- Conversion from Strings to Bytes ---
try:
    key_bytes = binascii.unhexlify(key_hex_string)
    nonce_bytes = binascii.unhexlify(nonce_hex_string)
    # Assumption: Ciphertext is Base64 encoded
    encrypted_text_bytes = b64decode(encrypted_text_b64_string)
    # If your ciphertext is Hex-encoded, use this instead:
    # encrypted_text_bytes = binascii.unhexlify(encrypted_text_hex_string) # (You would need to define encrypted_text_hex_string)

except binascii.Error as e:
    print(f"Error decoding hex string (key or nonce): {e}")
    print("Make sure the hex strings are correct and complete.")
    exit()
except Exception as e: # Also catches Base64 Decode errors
    print(f"Error decoding Base64 string (encrypted text): {e}")
    print("Make sure the Base64 string is correct and complete.")
    exit()

# --- Decryption with ChaCha20 ---
try:
    # Create the ChaCha20 cipher object with the key and nonce
    cipher = ChaCha20.new(key=key_bytes, nonce=nonce_bytes)

    # Decrypt the data
    decrypted_bytes = cipher.decrypt(encrypted_text_bytes)

    # Convert the decrypted bytes back into a string (assuming UTF-8 encoding)
    decrypted_text = decrypted_bytes.decode('utf-8')

    # --- Output ---
    print(f"Used Key (Hex): {key_hex_string}")
    print(f"Used Nonce (Hex):   {nonce_hex_string}")
    print(f"Encrypted Text (B64): {encrypted_text_b64_string}")
    print("-" * 30)
    print(f"Decrypted Text: {decrypted_text}")

except ValueError as e:
    print(f"Error during decryption: {e}")
    print("Possible causes: Incorrect key, incorrect nonce, or corrupted encrypted text.")
except UnicodeDecodeError as e:
    print(f"Error decoding the decrypted text to UTF-8: {e}")
    print("The original text might not have been UTF-8 encoded.")
    print(f"Decrypted Bytes (raw): {decrypted_bytes}")