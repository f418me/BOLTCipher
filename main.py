import binascii
import io
import logging
import secrets
import subprocess
from base64 import b64encode
from fastapi import FastAPI
from Crypto.Cipher import AES
from pydantic import BaseModel, Field
import uuid
from starlette.requests import Request
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from config import Config
from utils.cln import get_invoice
from fastapi.responses import StreamingResponse
import zipfile


config = Config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.LOG_LEVEL))
log = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def encrypt_message_b64(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_content = cipher.encrypt(data)
    return b64encode(encrypted_content).decode()


# Pydantic data model
class ContentItem(BaseModel):
    unique_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    encrypt_mode: str = 'AES.MODE_CFB'
    cost: str = f'{config.CONTENT_PRICE} Sats'
    bolt11: str
    abstract: str
    encrypted_content: str


def get_content():
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
    return content_item


@app.get("/json/", response_model=ContentItem)
async def get_content_json():
    content_item = get_content()
    return content_item


@app.get("/", response_class=HTMLResponse)
async def get_info(request: Request):
    content_item = get_content()

    return templates.TemplateResponse(
        request=request, name="response.html",
        context={"request": request, "item": content_item.dict()}
    )


@app.get("/download-pdf-in-zip")
def download_pdf_in_zip():

    pdf_file_path = "bitcoin.pdf"
    zip_file_path = pdf_file_path + '.zip'
    pwd = 'mypassword'
    path = '.'
    subprocess.run(["zip", "-P", pwd, '-r', zip_file_path, path])

    return FileResponse(zip_file_path, media_type="application/zip", filename=zip_file_path)
