import os
from pathlib import Path
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server

DATABASE_NAME = 'database.bin'
DATABASE_PATH = os.path.join(Path(__file__).parent.absolute(), DATABASE_NAME)

def init(anchor_domain, stellar_network, secret):
    globals()['STELLAR_NETWORK'] = stellar_network
    globals()['ANCHOR_DOMAIN'] = anchor_domain
    globals()['NETWORK_PASSPHRASE'] = Network.TESTNET_NETWORK_PASSPHRASE if stellar_network == 'TESTNET' else Network.PUBLIC_NETWORK_PASSPHRASE
    globals()['HORIZON_SERVER'] = Server(horizon_url='https://horizon-testnet.stellar.org/') if stellar_network == 'TESTNET' else Server(horizon_url='https://horizon.stellar.org/')

    globals()['SECRET'] = secret
    globals()['PUBKEY'] = Keypair.from_secret(secret).public_key
