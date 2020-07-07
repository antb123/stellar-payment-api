import requests
import toml
from urllib.parse import urljoin
from settings import TEMPO_DOMAIN

def fetch_stellar_toml():
    url = urljoin(TEMPO_DOMAIN, '.well-known/stellar.toml')
    return toml.loads(requests.get(url).text)
