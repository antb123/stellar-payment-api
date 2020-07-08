import os
from pathlib import Path
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server

DATABASE_NAME = 'database.bin'
DATABASE_PATH = os.path.join(Path(__file__).parent.absolute(), DATABASE_NAME)

TEMPO_DOMAINS = {
    'TESTNET': 'https://ktest.tempocrypto.com',
    'PUBLIC': 'https://k.tempocrypto.com',
}

ASSETS = {
    'PURPLE': {
        'code': 'PURPLE',
        'issuer': 'GBT4VVTDPCNA45MNWX5G6LUTLIEENSTUHDVXO2AQHAZ24KUZUPLPGJZH',
    },
    'EURT': {
        'code': 'EURT',
        'issuer': 'GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S',
    },
}

def init(stellar_network, secret):
    globals()['STELLAR_NETWORK'] = stellar_network
    globals()['TEMPO_DOMAIN'] = TEMPO_DOMAINS[stellar_network]
    globals()['NETWORK_PASSPHRASE'] = Network.TESTNET_NETWORK_PASSPHRASE if stellar_network == 'TESTNET' else Network.PUBLIC_NETWORK_PASSPHRASE
    globals()['HORIZON_SERVER'] = Server(horizon_url='https://horizon-testnet.stellar.org/') if stellar_network == 'TESTNET' else Server(horizon_url='https://horizon.stellar.org/')
    globals()['ASSET'] = ASSETS['PURPLE'] if stellar_network == 'TESTNET' else ASSETS['EURT']

    globals()['SECRET'] = secret
    globals()['PUBKEY'] = Keypair.from_secret(secret).public_key
