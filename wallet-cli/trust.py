from stellar_sdk.keypair import Keypair
from stellar_sdk.transaction_builder import TransactionBuilder
import settings


def change_trust(asset_code, asset_issuer, limit=None):
    keypair = Keypair.from_secret(settings.SECRET)
    account = settings.HORIZON_SERVER.load_account(keypair.public_key)

    builder = TransactionBuilder(source_account=account,
            network_passphrase=settings.NETWORK_PASSPHRASE)
    builder.append_change_trust_op(asset_code, asset_issuer, limit)

    envelope = builder.build()
    envelope.sign(keypair)
    return settings.HORIZON_SERVER.submit_transaction(envelope)
