import binascii
from base64 import b64encode

from fastapi import FastAPI
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from pydantic import BaseModel
import uuid

app = FastAPI()


def encrypt_message_b64(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_content = cipher.encrypt(data)
    return b64encode(encrypted_content).decode()

# Pyd
# antic-Modell für die Daten
class contentItem(BaseModel):
    id: str  # UUID als String
    encrypt_mode: str
    initialize_vector_hex: str
    invoice: str
    abstract: str
    content: str


class abstractItem(BaseModel):
    encrypt_mode: str
    cost: str
    abstract: str


@app.get("/abstract", response_model=abstractItem)
async def get_abstract():
    with open('abstract.txt', 'r', encoding='utf-8') as file:
        abstract = file.read()
    return abstractItem(encrypt_mode="AES.MODE_CFB", cost="Invoice123",
                       abstract=abstract)


# Route, die das JSON-Objekt zurückgibt
@app.get("/content/", response_model=contentItem)
async def get_whitepaper():
    with open('content.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    # Generierung einer UUID im RFC 4122 Format
    unique_id = str(uuid.uuid4())
    hex_key = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypt_content = encrypt_message_b64(encoded_content, key, iv)
    return contentItem(id=unique_id, encrypt_mode="AES.MODE_CFB", initialize_vector_hex=iv_hex, invoice="Invoice123",
                       abstract=abstract, content=encrypt_content)
