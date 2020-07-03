# SEP-10: Obtain token

The JWT token obtained via SEP-10 is required for many operations, including deposits
and withdrawals in SEP-24 and SEP-6.

A reference Python implementation on how to obtain the token is available in
Django Polaris test helpers:  
https://github.com/stellar/django-polaris/blob/c2efcf4fc8da630ea76c19df7e9b80be671f90ef/polaris/polaris/tests/helpers.py#L15
```
def sep10(client, address, seed):
    response = client.get(f"/auth?account={address}", follow=True)
    content = json.loads(response.content)
    envelope_xdr = content["transaction"]
    envelope_object = TransactionEnvelope.from_xdr(
        envelope_xdr, network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE
    )
    client_signing_key = Keypair.from_secret(seed)
    envelope_object.sign(client_signing_key)
    client_signed_envelope_xdr = envelope_object.to_xdr()

    response = client.post(
        "/auth",
        data={"transaction": client_signed_envelope_xdr},
        content_type="application/json",
    )
    content = json.loads(response.content)
    encoded_jwt = content["token"]
    assert encoded_jwt
    return encoded_jwt
```
