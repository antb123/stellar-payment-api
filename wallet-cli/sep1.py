import requests
import toml
import settings
from utils import urljoin

def fetch_stellar_toml():
    url = urljoin(settings.TEMPO_DOMAIN, '.well-known/stellar.toml')
    return toml.loads(requests.get(url).text)
