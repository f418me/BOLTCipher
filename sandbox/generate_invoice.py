"""
Generate invoice for test payment
"""
from pyln.client import LightningRpc
from config import Config
import random

config = Config()

node = LightningRpc(config.LIGHTNING_RPC_FILE)

node_info = node.getinfo()
print(node_info)

# Create invoice for test payment
invoice = node.invoice(18000, "lbl{}".format(random.random()), "testpayment")
print(invoice)
print("")
print(f"bolt11: {invoice['bolt11']}")

