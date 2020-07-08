import json
import requests
from stellar_sdk.keypair import Keypair
from stellar_sdk.transaction_envelope import TransactionEnvelope
from sep1 import fetch_stellar_toml
import settings


def auth():
    stellar_toml = fetch_stellar_toml()
    auth_url = stellar_toml['WEB_AUTH_ENDPOINT']

    # get challenge transaction and sign it
    client_signing_key = Keypair.from_secret(settings.SECRET)
    response = requests.get(f'{auth_url}?account={client_signing_key.public_key}')
    content = json.loads(response.content)
    envelope_xdr = content['transaction']
    envelope_object = TransactionEnvelope.from_xdr(
        envelope_xdr, network_passphrase=settings.NETWORK_PASSPHRASE
    )
    envelope_object.sign(client_signing_key)
    client_signed_envelope_xdr = envelope_object.to_xdr()

    # submit the signed transaction to prove ownership of the account
    response = requests.post(
        auth_url,
        json={"transaction": client_signed_envelope_xdr},
    )
    content = json.loads(response.content)
    return content['token']
