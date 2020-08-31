import requests
from sep1 import fetch_stellar_toml
from sep10 import auth
from utils import urljoin


def _headers(token):
    return {
        'Authorization': 'Bearer ' + (token or auth())
    }


def info():
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0031'], 'info')
    return requests.get(url).json()


def transactions_post(payload: dict, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0031'], 'transactions')
    return requests.post(url, json=payload, headers=_headers(token)).json()


def transactions_get(transaction_id: str, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0031'], 'transactions',
            transaction_id)
    return requests.get(url, headers=_headers(token)).json()


def transactions_patch(transaction_id: str, fields: dict, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0031'], 'transactions',
            transaction_id)
    return requests.patch(url, payload={"fields": fields},
            headers=_headers(token)).json()
