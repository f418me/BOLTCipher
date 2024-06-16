import binascii
import random
from base64 import b64encode

from fastapi import FastAPI
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from pydantic import BaseModel
import uuid

app = FastAPI()
from pyln.client import LightningRpc


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

    node = LightningRpc("/root/.lightning/lnd-rpc-file")

    invoice = node.invoice(18000, "lbl{}".format(random.random()), "testpayment")
    print(invoice)
    print("")
    print(f"bolt11: {invoice['bolt11']}")
    print(f"payment_secret: {invoice['payment_secret']}")
    bolt11 = invoice['bolt11']

    # Generierung einer UUID im RFC 4122 Format
    unique_id = str(uuid.uuid4())
    hex_key = invoice['payment_secret']
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypt_content = encrypt_message_b64(encoded_content, key, iv)
    return contentItem(id=unique_id, encrypt_mode="AES.MODE_CFB", initialize_vector_hex=iv_hex, invoice=bolt11,
                       abstract=abstract, content=encrypt_content)
