import requests
from sep10 import auth
from sep1 import fetch_stellar_toml
from utils import urljoin


def _headers(token):
    return {
        'Authorization': 'Bearer ' + (token or auth())
    }


def deposit(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'transactions/deposit/interactive')
    return requests.post(url, data=params, headers=_headers(token)).json()


def withdraw(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'transactions/withdraw/interactive')
    return requests.post(url, data=params, headers=_headers(token)).json()


def info():
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'info')
    return requests.get(url).json()


def fee(params):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'fee')
    return requests.get(url, params=params).json()


def transaction(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'transaction')
    return requests.get(url, params=params, headers=_headers(token)).json()


def transactions(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER_SEP0024'], 'transactions')
    return requests.get(url, params=params, headers=_headers(token)).json()
