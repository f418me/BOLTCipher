"""
Generate invoice for test payment
"""
from pyln.client import LightningRpc
import random

# Create an instances of the LightningRpc object
node = LightningRpc("/root/.lightning/lnd-rpc-file")

info_A = node.getinfo()
print(info_A)

# Create invoice for test payment
invoice = node.invoice(18000, "lbl{}".format(random.random()), "testpayment")
print(invoice)
print("")
print(f"bolt11: {invoice['bolt11']}")

