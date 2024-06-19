import binascii
from base64 import b64encode
from random import random

from pyln.client import LightningRpc
from fastapi import FastAPI
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from pydantic import BaseModel
import uuid

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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


@app.get("/content", response_class=HTMLResponse)
async def get_content(request: Request):
    with open('content_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        abstract = file.read()

    node = LightningRpc("/root/.lightning/lnd-rpc-file")

    invoice = node.invoice(18000, "lbl{}".format(random.random()), "BOLTCipher")
    bolt11 = invoice['bolt11']

    unique_id = str(uuid.uuid4())
    hex_key = invoice['payment_secret']
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)
    iv_hex = iv.hex()
    encrypt_content = encrypt_message_b64(encoded_content, key, iv)
    return templates.TemplateResponse(
        request=request, name="response.html", context={"unique_id":unique_id, "encrypt_mode": encrypt_mode, "cost": cost, "abstract": abstract, "bolt11": bolt11, "iv_hex": iv_hex, "encrypted_content": encrypted_content}
    )




@app.get("/content-json", response_model=contentItem)
async def get_content_json():
    with open('content_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    node = LightningRpc("/root/.lightning/lnd-rpc-file")

    invoice = node.invoice(18000, "lbl{}".format(random.random()), "BOLTCipher")
    bolt11 = invoice['bolt11']

    unique_id = str(uuid.uuid4())
    hex_key = invoice['payment_secret']
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)
    iv_hex = iv.hex()
    encrypt_content = encrypt_message_b64(encoded_content, key, iv)
    return contentItem(id=unique_id, encrypt_mode="AES.MODE_CFB", initialize_vector_hex=iv_hex, invoice=bolt11,
                       abstract=abstract, content=encrypt_content)


@app.get("/test-content", response_class=HTMLResponse)
async def get_test_content(request: Request):
    with open('content_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    # Generierung einer UUID im RFC 4122 Format
    unique_id = str(uuid.uuid4())
    encrypt_mode = "AES.MODE_CFB"
    cost = "18 Sats"
    hex_key = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
    bolt11 = "lnbc1800n1"
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypted_content = encrypt_message_b64(encoded_content, key, iv)
    return templates.TemplateResponse(
        request=request, name="response.html", context={"unique_id":unique_id, "encrypt_mode": encrypt_mode, "cost": cost, "abstract": abstract, "bolt11": bolt11, "iv_hex": iv_hex, "encrypted_content": encrypted_content}
    )

@app.get("/test-content-json/", response_model=contentItem)
async def get_content_json():
    with open('content_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
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


@app.get("/", response_class=HTMLResponse)
async def get_info(request: Request):
    encrypt_mode = "AES.MODE_CFB"
    cost = "18 Sats"

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    return templates.TemplateResponse(
        request=request, name="info.html", context={"encrypt_mode": encrypt_mode, "cost": cost, "abstract": abstract}
    )

