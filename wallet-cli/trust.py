from stellar_sdk.keypair import Keypair
from stellar_sdk.transaction_builder import TransactionBuilder
from settings import SECRET, HORIZON_SERVER, NETWORK_PASSPHRASE


def change_trust(asset_code, asset_issuer, limit=None):
    keypair = Keypair.from_secret(SECRET)
    account = HORIZON_SERVER.load_account(keypair.public_key)

    builder = TransactionBuilder(source_account=account,
            network_passphrase=NETWORK_PASSPHRASE)
    builder.append_change_trust_op(asset_code, asset_issuer, limit)

    envelope = builder.build()
    envelope.sign(keypair)
    return HORIZON_SERVER.submit_transaction(envelope)
