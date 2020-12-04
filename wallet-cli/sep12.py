import requests
from sep10 import auth
from sep1 import fetch_stellar_toml
from utils import urljoin


def _headers(token):
    return {
        'Authorization': 'Bearer ' + (token or auth())
    }


def customer_get(params: dict, token=None):
    stellar_toml = fetch_stellar_toml()
    server = stellar_toml.get('KYC_SERVER')
    if server is None:
        server = stellar_toml['TRANSFER_SERVER']
    url = urljoin(server, 'customer')
    return requests.get(url, params=params, headers=_headers(token)).json()


def customer_put(params: dict, token=None):
    stellar_toml = fetch_stellar_toml()
    server = stellar_toml.get('KYC_SERVER')
    if server is None:
        server = stellar_toml['TRANSFER_SERVER']
    url = urljoin(server, 'customer')
    return requests.put(url, data=params, headers=_headers(token)).json()
