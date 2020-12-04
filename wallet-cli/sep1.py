import requests
import toml
import settings
from utils import urljoin

def fetch_stellar_toml(anchor_domain=None):
    anchor_domain = anchor_domain if anchor_domain is not None else settings.ANCHOR_DOMAIN
    url = urljoin(f'https://{anchor_domain}', '.well-known/stellar.toml')
    return toml.loads(requests.get(url).text)
