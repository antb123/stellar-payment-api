# TEMPO's Stellar API documentation

TEMPO is a Stellar Anchor and provides support for EUR deposits and withdrawals on
the Stellar network.

# Summary
* [1. Domains](#1-domains)  
    - [1.1. Public Network](#11-public-network)  
    - [1.2. Test Network](#12-test-network)  
* [2. SEPs](#2-seps)  
* [3. Integrating with TEMPO](#3-integrating-with-tempo)  
    - [3.1. Fetch stellar.toml](#31-fetch-stellartoml)  
    - [3.2. Get auth token](#32-get-auth-token)  
    - [3.3. Trustline](#33-trustline)  
    - [3.4. Deposit](#34-deposit)  
    - [3.5. Withdrawal](#35-withdrawal)  

## 1. Domains

### 1.1. Public Network

Domain:  
`https://k.tempocrypto.com`

Assets:
* EURT (fiat)

*fiat* assets represent currencies in the real world (EUR, USD) and can be
 deposited/withdrawn directly to bank accounts.

### 1.2. Test Network

Domain:  
`https://ktest.tempocrypto.com`

Assets:
* PURPLE

## 2. SEPs

* [SEP-1](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0001.md): fully compliant
* [SEP-2](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0002.md): not supported
* [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md): fully compliant, requires account to be already verified, see notes below
* [SEP-10](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md): fully compliant
* [SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md): fully compliant

Notes:
* SEP-6 can only be used after user document verification (KYC), either through SEP-24 or manual approval

## 3. Integrating with TEMPO

### 3.1. Fetch stellar.toml
`stellar.toml` provides these variables, which are required for [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md) and [SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md):
  - `TRANSFER_SERVER`
  - `TRANSFER_SERVER_SEP0024`
  - `WEB_AUTH_ENDPOINT`

Python example on how to fetch TEMPO's testnet `stellar.toml`:
```python
import requests
import toml

stellar_toml = toml.loads(requests.get('https://ktest.tempocrypto.com/.well-known/stellar.toml').text)
```

### 3.2. Get auth token

[SEP-10](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md) provides a mechanism to
prove ownership of a Stellar account and obtain a reusable JWT token which carries the ownership information.  
The token is required in many transaction endpoints ([SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md), [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md), etc)
and allow the Wallet to deposit and withdrawal funds on the account through TEMPO.  
The token is usually valid for 1 day after it's generated, and can be used in all HTTP requests while it's valid.

Python example (based on [Django Polaris code](https://github.com/stellar/django-polaris/blob/c2efcf4fc8da630ea76c19df7e9b80be671f90ef/polaris/polaris/tests/helpers.py#L15)) on how to get a new JWT token:
```python
from stellar_sdk.keypair import Keypair
from stellar_sdk.transaction_envelope import TransactionEnvelope

secret_key = 'SBYWIVPVH5PQPB...'

auth_url = stellar_toml['WEB_AUTH_ENDPOINT']

# get challenge transaction and sign it
client_signing_key = Keypair.from_secret(secret_key)
response = client.get(f'{auth_url}?account={client_signing_key.public_key}', follow=True)
content = json.loads(response.content)
envelope_xdr = content['transaction']
envelope_object = TransactionEnvelope.from_xdr(
    envelope_xdr, network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE
)
envelope_object.sign(client_signing_key)
client_signed_envelope_xdr = envelope_object.to_xdr()

# submit the signed transaction to prove ownership of the account
response = client.post(
    f'{auth_url}/auth',
    data={"transaction": client_signed_envelope_xdr},
    content_type='application/json',
)
content = json.loads(response.content)

sep10_token = content['token']
```

### 3.3. Trustline

To deposit assets into a Stellar account, the account must first trust the asset.  
A trustline operation is required only once and the trust will last forever on the account unless removed.  
Python example on how to trust TEMPO's PURPLE asset (used for testnet transactions):
```python
from stellar_sdk.server import Server
from stellar_sdk.network import Network

secret_key = 'SBYWIVPV...'
horizon_testnet = 'https://horizon-testnet.stellar.org/'
asset_info = stellar_toml['CURRENCIES'][0]

server = Server(horizon_url=horizon_testnet)
keypair = Keypair.from_secret(secret_key)
account = server.load_account(keypair.public_key)
builder = TransactionBuilder(source_account=account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE)
builder.append_change_trust_op(asset_code=asset_info['code'],
        asset_issuer=asset_info['issuer'])
envelope = builder.build()
envelope.sign(keypair)
response = server.submit_transaction(envelope)
assert response['successful']
```

### 3.4. Deposit

Deposits are a way for users to deposit real world currencies (ex: USD, EUR) into their Stellar account (usually managed by a Wallet).  
For example, a user can have EUR on a bank account outside Stellar, and deposit that as EURT into a Stellar account.  
To deposit assets, the Wallet must create deposit transactions on TEMPO.  
To create transactions, there are two options:
* [SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md)
  - Interactive - all information needed from the user is collected by TEMPO using web pages
  - Requires opening a popup window or iframe pointing to an URL provided by TEMPO
  - See [example](#sep-24-deposit-python-example) below
* [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md)
  - Non-interactive - Wallet must provide all required information through HTTP requests
  - Does not require opening any external web page
  - **TEMPO requires the account to be already verified (KYC approved) in order to allow SEP-6 operations.
  An account can be verified through SEP-24 or manually approved by TEMPO.**
  - See [example](#sep-6-deposit-python-example) below

#### SEP-24 Deposit Python example:
```python
def sep24_deposit():
    data = {
        'asset_code': 'PURPLE',
        'account': 'GC75JLZ6...',
    }
    headers = {
        'Authorization': 'Bearer ' + sep10_token
    }
    url = stellar_toml['TRANSFER_SERVER_SEP0024'] + '/t1/transactions/deposit/interactive'
    response = requests.post(url, data=data, headers=headers).json()
    return render_sep24_interactive(response['url'])  # popup window on the client
```

#### SEP-6 Deposit Python example:
```python
def sep6_deposit():
    data = {
        'asset_code': 'PURPLE',
        'account': 'GC75JLZ6...',

        # these fields are specific for TEMPO,
        #  they're specified on the SEP-6 /info endpoint
        'type': 'sepa',  # SEPA transfer deposit
        'first_name': 'John',
        'last_name': 'Doe',
        'email_address': 'johndoe@example.com',
        'amount': '11.0',
    }
    headers = {
        'Authorization': 'Bearer ' + sep10_token
    }
    url = stellar_toml['TRANSFER_SERVER'] + '/sep6/deposit'
    response = requests.post(url, data=data, headers=headers).json()
    return render_sep6_instructions(response)  # display instructions to user
```

### 3.5. Withdrawal

Withdrawals are a way for users to obtain assets from their Stellar account as real world currencies (ex: USD, EUR).  
For example, a user can have EURT balance in a Stellar account and withdraw that as EUR, receiving the EUR on a bank account outside Stellar.  
To withdraw assets, the Wallet must create withdrawal transactions on TEMPO.  
To create transactions, there are two options:
* [SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md)
  - Interactive - all information needed from the user is collected by TEMPO using web pages
  - Requires opening a popup window or iframe pointing to an URL provided by TEMPO
  - See [example](#sep-24-withdrawal-python-example) below
* [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md)
  - Non-interactive - Wallet must provide all required information through HTTP requests
  - Does not require opening any external web page
  - **TEMPO requires the account to be already verified (KYC approved) in order to allow SEP-6 operations.
  An account can be verified through SEP-24 or manually approved by TEMPO.**
  - See [example](#sep-6-withdrawal-python-example) below

#### SEP-24 Withdrawal Python example:
```python
def sep24_withdrawal():
    data = {
        'asset_code': 'PURPLE',
    }
    headers = {
        'Authorization': 'Bearer ' + sep10_token
    }
    url = stellar_toml['TRANSFER_SERVER_SEP0024'] + '/t1/transactions/withdraw/interactive'
    response = requests.post(url, data=data, headers=headers).json()
    return render_sep24_interactive(response['url'])  # popup window on the client
```

#### SEP-6 Withdrawal Python example:
```python
def sep6_withdrawal():
    data = {
        'asset_code': 'PURPLE',

        # these fields are specific for TEMPO,
        #  they're specified on the SEP-6 /info endpoint
        'amount': '12.5',
        'type': 'cash',
        'dest_country': 'fr',
        'benef_first_name': 'John',
        'benef_last_name': 'Doe',
        'benef_email': 'johndoe@example.com',
    }
    headers = {
        'Authorization': 'Bearer ' + sep10_token
    }
    url = stellar_toml['TRANSFER_SERVER'] + '/sep6/withdraw'
    response = requests.post(url, data=data, headers=headers).json()
    return render_sep6_instructions(response)  # display instructions to user
```
