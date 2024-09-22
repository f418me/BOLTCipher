import secrets
from pyln.client import LightningRpc

from config import Config

config = Config()

def get_invoice(amount_msats: int, preimage: hex):
    node = LightningRpc(config.LIGHTNING_RPC_FILE)

    random_string = secrets.token_hex(16)
    invoice_label = f'{config.INVOICE_LABEL_PREFIX}' + random_string
    description = config.INVOICE_DESCRIPTION

    invoice = node.invoice(
        amount_msat=amount_msats,
        label=invoice_label,
        description=description,
        preimage=preimage
    )
    return invoice
