import binascii
import logging
import secrets
import subprocess
from base64 import b64encode
from fastapi import FastAPI
from Crypto.Cipher import ChaCha20
from pydantic import BaseModel, Field
import uuid
from starlette.requests import Request
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from config import Config
from utils.cln import get_invoice



config = Config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.LOG_LEVEL))
log = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def encrypt_message_chacha20_b64(data: bytes, key: bytes, nonce: bytes) -> str:
    """Encrypts data using ChaCha20 and returns Base64 encoded string."""
    cipher = ChaCha20.new(key=key, nonce=nonce)
    encrypted_content = cipher.encrypt(data)
    return b64encode(encrypted_content).decode('utf-8')


class ContentItem(BaseModel):
    unique_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    encrypt_mode: str = 'ChaCha20' # Aktualisiert
    cost: str = f'{config.CONTENT_PRICE} Sats'
    bolt11: str
    abstract: str
    nonce_hex: str # Nonce statt IV
    encrypted_content: str


def get_content():
    with open('content.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        encoded_content = content.encode('utf-8')

    with open('abstract_planB.txt', 'r', encoding='utf-8') as file:
        abstract = file.read()

    invoice_amount_msats = int(config.CONTENT_PRICE) * 1000

    # Preimage wird als Key verwendet (32 Bytes = 256 Bits)
    preimage_hex = secrets.token_hex(32)
    key_bytes = binascii.unhexlify(preimage_hex)

    # Generiere einen zufälligen 8-Byte Nonce (wie in dec_response.py)
    # WICHTIG: Für jede Verschlüsselung mit demselben Key MUSS ein neuer Nonce generiert werden!
    # Standardmäßig verwendet ChaCha20 oft 12 Bytes, aber wir halten uns an das Beispiel.
    nonce_bytes = secrets.token_bytes(12)
    nonce_hex = binascii.hexlify(nonce_bytes).decode('utf-8')

    # Invoice mit dem Preimage generieren (wie vorher)
    invoice = get_invoice(invoice_amount_msats, preimage_hex)
    bolt11 = invoice['bolt11']

    log.info(f"Generated Key (Hex): {preimage_hex}")
    log.info(f"Generated Nonce (Hex):  {nonce_hex}")
    log.info(f"Generated Bolt11: {bolt11}")

    encrypted_content_b64 = encrypt_message_chacha20_b64(encoded_content, key_bytes, nonce_bytes)

    content_item = ContentItem(
        abstract=abstract,
        bolt11=bolt11,
        nonce_hex=nonce_hex, # Nonce statt IV
        encrypted_content=encrypted_content_b64
    )
    return content_item


@app.get("/json/", response_model=ContentItem)
async def get_content_json():
    content_item = get_content()
    return content_item


@app.get("/", response_class=HTMLResponse)
async def get_info(request: Request):
    content_item = get_content()

    # Stelle sicher, dass das Template 'response.html' die neuen Felder
    # (key_hex, nonce_hex) anstelle der alten (initialize_vector_hex) verwendet,
    # wenn es diese anzeigt.
    return templates.TemplateResponse(
        request=request, name="response.html",
        context={"request": request, "item": content_item.dict()}
    )


@app.get("/download-pdf-in-zip")
def download_pdf_in_zip():

    pdf_file_path = "bitcoin.pdf"
    zip_file_path = pdf_file_path + '.zip'
    pwd = 'mypassword' # Vorsicht: Passwort ist hardcoded
    # Es wird empfohlen, Passwörter sicherer zu handhaben (z.B. Konfiguration, Umgebungsvariable)
    subprocess.run(["zip", "-P", pwd, '-r', zip_file_path, pdf_file_path])

    return FileResponse(zip_file_path, media_type="application/zip", filename=zip_file_path)

