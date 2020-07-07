from stellar_sdk.network import Network
from stellar_sdk.server import Server


STELLAR_NETWORK = 'TESTNET'

PUBKEY = ''
SECRET = ''

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

try:
    from local_settings import *
except ImportError as e:
    pass

TEMPO_DOMAIN = TEMPO_DOMAINS[STELLAR_NETWORK]
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE if STELLAR_NETWORK == 'TESTNET' else Network.PUBLIC_NETWORK_PASSPHRASE
HORIZON_SERVER = Server(horizon_url='https://horizon-testnet.stellar.org/') if STELLAR_NETWORK == 'TESTNET' else Server(horizon_url='https://horizon.stellar.org/')
ASSET = ASSETS['PURPLE'] if STELLAR_NETWORK == 'TESTNET' else ASSETS['EURT']
