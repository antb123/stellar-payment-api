import requests
import toml
from urllib.parse import urljoin
import settings

def fetch_stellar_toml():
    url = urljoin(settings.TEMPO_DOMAIN, '.well-known/stellar.toml')
    return toml.loads(requests.get(url).text)
