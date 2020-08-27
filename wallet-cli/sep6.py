import requests
from sep1 import fetch_stellar_toml
from sep10 import auth
from utils import urljoin


def _headers(token):
    return {
        'Authorization': 'Bearer ' + (token or auth())
    }


def deposit(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'deposit')
    return requests.get(url, params=params, headers=_headers(token)).json()


def withdraw(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'withdraw')
    return requests.get(url, params=params, headers=_headers(token)).json()


def info():
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'info')
    return requests.get(url).json()


def fee(params):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'fee')
    return requests.get(url, params=params).json()


def transaction(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'transaction')
    return requests.get(url, params=params, headers=_headers(token)).json()


def transactions(params, token=None):
    stellar_toml = fetch_stellar_toml()
    url = urljoin(stellar_toml['TRANSFER_SERVER'], 'transactions')
    return requests.get(url, params=params, headers=_headers(token)).json()
