from pyln.client import LightningRpc
from config import Config

config = Config()

node = LightningRpc(config.LIGHTNING_RPC_FILE)

print(node.getinfo())
