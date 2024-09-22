import binascii
import csv
import logging
import secrets
from base64 import b64encode
from pyln.client import LightningRpc
from fastapi import FastAPI
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from pydantic import BaseModel, Field
import uuid

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from config import Config
from utils.cln import get_invoice

#todo put all strings into config


config = Config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.LOG_LEVEL))
log = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#todo remove or move to different class
def read_bolt11(file_path):
    updated_rows = []
    result_dict = None
    found_unread = False  # Zustand, um zu überprüfen, ob eine ungelesene Zeile gefunden wurde

    # CSV-Datei öffnen und Zeilen lesen
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        for row in reader:
            if not found_unread:  # Prüfen, ob bereits eine ungelesene Zeile gefunden wurde
                if len(row) == 2 and not row[0].startswith(
                        'used'):  # Überprüfen, ob die Zeile zwei Elemente hat und nicht markiert ist
                    result_dict = {'payment_secret': row[0], 'bolt11': row[1]}
                    row = ['used'] + row  # Markieren der Zeile als "used" am Anfang der Zeile
                    found_unread = True  # Setzen des Flags, dass eine ungelesene Zeile gefunden wurde
            updated_rows.append(row)  # Füge die gelesenen Zeilen zur Aktualisierungsliste hinzu

    # CSV-Datei mit den aktualisierten Zeilen zurückschreiben
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    return result_dict


def encrypt_message_b64(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_content = cipher.encrypt(data)
    return b64encode(encrypted_content).decode()


# Pydantic data model
class ContentItem(BaseModel):
    unique_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    encrypt_mode: str = 'AES.MODE_CFB'
    cost: str = f'{config.CONTENT_PRICE} Sats'
    initialize_vector_hex: str
    bolt11: str
    abstract: str
    encrypted_content: str


class AbstractItem(BaseModel):
    encrypt_mode: str
    cost: str
    abstract: str


@app.get("/content", response_class=HTMLResponse)
async def get_content(request: Request):
    with open('content.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        abstract = file.read()

    invoice_amount_msats = int(config.CONTENT_PRICE) * 1000
    preimage = secrets.token_hex(32)

    # We use the first 16 bytes of the key as the iv
    iv_hex = preimage[:32]
    iv = binascii.unhexlify(iv_hex)

    invoice = get_invoice(invoice_amount_msats, preimage)
    bolt11 = invoice['bolt11']

    key = binascii.unhexlify(preimage)

    log.info(f"iv_hex: {iv_hex}")
    log.info(f"preimage: {preimage}")
    log.info(f"bolt11: {bolt11}")



    encrypted_content = encrypt_message_b64(encoded_content, key, iv)

    content_item = ContentItem(
        abstract=abstract,
        bolt11=bolt11,
        initialize_vector_hex=iv_hex,
        encrypted_content=encrypted_content
    )

    return templates.TemplateResponse(
        request=request, name="response.html",
        context={"request": request, "item": content_item.dict()}
    )


#todo update json response according to the content route
@app.get("/content-json", response_model=ContentItem)
async def get_content_json():
    with open('content.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode()

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    node = LightningRpc("/root/.lightning/lnd-rpc-file")

    preimage = secrets.token_hex(32)

    invoice = node.invoice(
        amount_msat=18000,
        #label="lbl{}".format(random.random()),
        description="BOLTCipher",
        preimage=preimage
    )
    bolt11 = invoice['bolt11']

    #invoice = read_bolt11('bolt11.csv')
    #bolt11 = invoice['bolt11']
    key = binascii.unhexlify(preimage)
    iv = get_random_bytes(16)
    iv_hex = iv.hex()
    encrypted_content = encrypt_message_b64(encoded_content, key, iv)

    preimage = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
    key = binascii.unhexlify(preimage)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypted_content = encrypt_message_b64(encoded_content, key, iv)

    return ContentItem(
        initialize_vector_hex=iv_hex,
        abstract=abstract,
        bolt11=bolt11,
        encrypted_content=encrypted_content
    )


@app.get("/test-content", response_class=HTMLResponse)
async def get_test_content(request: Request):
    with open('content.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        abstract = file.read()

    preimage = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
    bolt11 = "lnbc1800n1"
    key = binascii.unhexlify(preimage)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypted_content = encrypt_message_b64(encoded_content, key, iv)
    content_item = ContentItem(
        abstract=abstract,
        bolt11=bolt11,
        initialize_vector_hex=iv_hex,
        encrypted_content=encrypted_content
    )
    return templates.TemplateResponse(
        request=request, name="response.html",
        context={"request": request, "item": content_item.dict()}
    )


@app.get("/test-content-json/", response_model=ContentItem)
async def get_content_json():
    with open('content.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        # Lesen aller Zeilen der Datei
        abstract = file.read()

    # Generierung einer UUID im RFC 4122 Format
    unique_id = str(uuid.uuid4())
    hex_key = '016ede0e62833ff4088a60f8b7823943ba641b0da11555997f434734e860738d'
    cost = "18 Sats"
    ecrypt_mode = "AES.MODE_CFB"
    key = binascii.unhexlify(hex_key)
    iv = get_random_bytes(16)  # Zufälliger Initialisierungsvektor
    iv_hex = iv.hex()
    encrypt_content = encrypt_message_b64(encoded_content, key, iv)
    return ContentItem(id=unique_id, encrypt_mode="AES.MODE_CFB", initialize_vector_hex=iv_hex, invoice="Invoice123",
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
