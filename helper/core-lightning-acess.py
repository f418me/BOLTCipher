from pyln.client import LightningRpc

node = LightningRpc("/Users/fre/.lightning/bitcoin/lightning-rpc")

print(node.getinfo())
