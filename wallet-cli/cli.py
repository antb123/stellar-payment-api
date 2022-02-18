"""
Wallet CLI

1) Installation

python3 -m pip install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

2) Running

python cli.py --help

"""
import argparse
from getpass import getpass
import json
from json.decoder import JSONDecodeError
import os
import os.path
import sys

from requests.exceptions import RequestException
from stellar_sdk.exceptions import Ed25519SecretSeedInvalidError
from stellar_sdk.keypair import Keypair
from termcolor import colored, cprint

import database
import sep1
import trust
import sep6
import sep10
import sep12
import sep24
import sep31
import settings


PARSERS = {}


def argparser():
    parser = argparse.ArgumentParser(description='Wallet CLI')
    parser.add_argument('-e', '--env', action='store_true',
            help='get database password from WALLET_CLI_PASSWORD environment variable')
    option_subparsers = parser.add_subparsers(help='option', dest='_option')

    def add_database_parser():
        database_parser = option_subparsers.add_parser('database')
        PARSERS['database'] = {}
        PARSERS['database']['_'] = database_parser
        database_subparsers = database_parser.add_subparsers(description='operations', dest='_operation')

        create_parser = database_subparsers.add_parser('create')
        PARSERS['database']['create'] = create_parser

        delete_parser = database_subparsers.add_parser('delete')
        PARSERS['database']['delete'] = delete_parser

        list_parser = database_subparsers.add_parser('list')
        PARSERS['database']['list'] = list_parser

    def add_sep1_parser():
        sep1_parser = option_subparsers.add_parser('sep1')
        PARSERS['sep1'] = {}
        PARSERS['sep1']['_'] = sep1_parser
        sep1_subparsers = sep1_parser.add_subparsers(description='operations', dest='_operation')
        fetch_stellar_toml_parser = sep1_subparsers.add_parser('fetch_stellar_toml')
        PARSERS['sep1']['fetch_stellar_toml'] = fetch_stellar_toml_parser

    def add_trust_parser():
        trust_parser = option_subparsers.add_parser('trust')
        PARSERS['trust'] = {}
        PARSERS['trust']['_'] = trust_parser
        trust_subparsers = trust_parser.add_subparsers(description='operations', dest='_operation')
        change_trust_parser = trust_subparsers.add_parser('change_trust')
        change_trust_parser.add_argument('--asset-code', required=True)
        change_trust_parser.add_argument('--issuer', required=True)
        change_trust_parser.add_argument('--limit')
        PARSERS['trust']['change_trust'] = change_trust_parser

    def add_sep6_parser():
        sep6_parser = option_subparsers.add_parser('sep6')
        PARSERS['sep6'] = {}
        PARSERS['sep6']['_'] = sep6_parser
        sep6_subparsers = sep6_parser.add_subparsers(description='operations', dest='_operation')

        info_parser = sep6_subparsers.add_parser('info')
        PARSERS['sep6']['info'] = info_parser

        fee_parser = sep6_subparsers.add_parser('fee')
        fee_parser.add_argument('--operation', required=True)
        fee_parser.add_argument('--amount', required=True)
        fee_parser.add_argument('--asset-code', required=True)
        fee_parser.add_argument('--type')
        PARSERS['sep6']['fee'] = fee_parser

        deposit_parser = sep6_subparsers.add_parser('deposit')
        deposit_parser.add_argument('--first-name', required=True)
        deposit_parser.add_argument('--last-name', required=True)
        deposit_parser.add_argument('--email-address', required=True)
        deposit_parser.add_argument('--amount', required=True)
        deposit_parser.add_argument('--asset-code', required=True)
        deposit_parser.add_argument('--account')
        deposit_parser.add_argument('--memo-type')
        deposit_parser.add_argument('--memo')
        deposit_parser.add_argument('--type', choices=['sepa', 'cash'])
        deposit_parser.add_argument('--wallet-name')
        deposit_parser.add_argument('--wallet-url')
        deposit_parser.add_argument('--lang')
        deposit_parser.add_argument('--partner-ref')
        deposit_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep6']['deposit'] = deposit_parser

        withdraw_parser = sep6_subparsers.add_parser('withdraw')
        withdraw_parser.add_argument('--amount', required=True)
        withdraw_parser.add_argument('--type', required=True, choices=['sepa', 'cash'])
        withdraw_parser.add_argument('--asset-code', required=True)
        withdraw_parser.add_argument('--dest-country', required=True)
        withdraw_parser.add_argument('--benef-first-name', required=True)
        withdraw_parser.add_argument('--benef-last-name', required=True)
        withdraw_parser.add_argument('--benef-email', required=True)
        withdraw_parser.add_argument('--benef-address', required=True)
        withdraw_parser.add_argument('--benef-city', required=True)
        withdraw_parser.add_argument('--bank-bic', help='required if type is sepa')
        withdraw_parser.add_argument('--dest', help='required if type is sepa')
        withdraw_parser.add_argument('--memo')
        withdraw_parser.add_argument('--memo-type')
        withdraw_parser.add_argument('--wallet-name')
        withdraw_parser.add_argument('--wallet-url')
        withdraw_parser.add_argument('--lang')
        withdraw_parser.add_argument('--benef-phone-number')
        withdraw_parser.add_argument('--external-memo')
        withdraw_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep6']['withdraw'] = withdraw_parser

        transaction_parser = sep6_subparsers.add_parser('transaction')
        transaction_parser.add_argument('--id')
        transaction_parser.add_argument('--stellar-transaction-id')
        transaction_parser.add_argument('--external-transaction-id')
        transaction_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep6']['transaction'] = transaction_parser

        transactions_parser = sep6_subparsers.add_parser('transactions')
        transactions_parser.add_argument('--asset-code', required=True)
        transactions_parser.add_argument('--no-older-than')
        transactions_parser.add_argument('--limit')
        transactions_parser.add_argument('--kind')
        transactions_parser.add_argument('--paging-id')
        transactions_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep6']['transactions'] = transactions_parser

    def add_sep10_parser():
        sep10_parser = option_subparsers.add_parser('sep10')
        PARSERS['sep10'] = {}
        PARSERS['sep10']['_'] = sep10_parser
        sep10_subparsers = sep10_parser.add_subparsers(description='operations', dest='_operation')
        auth_parser = sep10_subparsers.add_parser('auth')
        PARSERS['sep10']['auth'] = auth_parser

    def add_sep12_parser():
        sep12_parser = option_subparsers.add_parser('sep12')
        PARSERS['sep12'] = {}
        PARSERS['sep12']['_'] = sep12_parser
        sep12_subparsers = sep12_parser.add_subparsers(description='operations', dest='_operation')

        get_parser = sep12_subparsers.add_parser('get')
        get_parser.add_argument('--id')
        get_parser.add_argument('--account')
        get_parser.add_argument('--memo')
        get_parser.add_argument('--memo_type')
        get_parser.add_argument('--type')
        get_parser.add_argument('--lang')
        get_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep12']['get'] = get_parser

        put_parser = sep12_subparsers.add_parser('put')
        put_parser.add_argument(
            '--data',
            required=True,
            help='Parameters as a JSON string. Ex: {"memo": "MEMO1234"}'
        )
        put_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep12']['put'] = put_parser

    def add_sep24_parser():
        sep24_parser = option_subparsers.add_parser('sep24')
        PARSERS['sep24'] = {}
        PARSERS['sep24']['_'] = sep24_parser
        sep24_subparsers = sep24_parser.add_subparsers(description='operations', dest='_operation')

        info_parser = sep24_subparsers.add_parser('info')
        PARSERS['sep24']['info'] = info_parser

        fee_parser = sep24_subparsers.add_parser('fee')
        fee_parser.add_argument('--operation', required=True)
        fee_parser.add_argument('--amount', required=True)
        fee_parser.add_argument('--asset-code', required=True)
        fee_parser.add_argument('--type')
        PARSERS['sep24']['fee'] = fee_parser

        deposit_parser = sep24_subparsers.add_parser('deposit')
        deposit_parser.add_argument(
            '--data',
            required=True,
            help='Parameters as a JSON string. Ex: {"memo": "MEMO1234"}'
        )
        deposit_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep24']['deposit'] = deposit_parser

        withdraw_parser = sep24_subparsers.add_parser('withdraw')
        withdraw_parser.add_argument(
            '--data',
            required=True,
            help='Parameters as a JSON string. Ex: {"memo": "MEMO1234"}'
        )
        withdraw_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep24']['withdraw'] = withdraw_parser

        transaction_parser = sep24_subparsers.add_parser('transaction')
        transaction_parser.add_argument('--id')
        transaction_parser.add_argument('--stellar-transaction-id')
        transaction_parser.add_argument('--external-transaction-id')
        transaction_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep24']['transaction'] = transaction_parser

        transactions_parser = sep24_subparsers.add_parser('transactions')
        transactions_parser.add_argument('--asset-code', required=True)
        transactions_parser.add_argument('--no-older-than')
        transactions_parser.add_argument('--limit')
        transactions_parser.add_argument('--kind')
        transactions_parser.add_argument('--paging-id')
        transactions_parser.add_argument('--token', help='SEP10 auth token')
        PARSERS['sep24']['transactions'] = transactions_parser

    def add_sep31_parser():
        sep31_parser = option_subparsers.add_parser('sep31')
        PARSERS['sep31'] = {}
        PARSERS['sep31']['_'] = sep31_parser
        sep31_subparsers = sep31_parser.add_subparsers(description='operations', dest='_operation')

        info_parser = sep31_subparsers.add_parser('info')
        PARSERS['sep31']['info'] = info_parser

        create_transaction_parser = sep31_subparsers.add_parser('create_transaction')
        create_transaction_parser.add_argument('--amount', required=True)
        create_transaction_parser.add_argument('--asset-code', required=True)
        create_transaction_parser.add_argument('--fields', help='fields as a JSON string')
        PARSERS['sep31']['create_transaction'] = create_transaction_parser

        get_transaction_parser = sep31_subparsers.add_parser('get_transaction')
        get_transaction_parser.add_argument('--transaction-id', required=True)
        PARSERS['sep31']['get_transaction'] = get_transaction_parser

        patch_transaction_parser = sep31_subparsers.add_parser('patch_transaction')
        patch_transaction_parser.add_argument('--transaction-id', required=True)
        patch_transaction_parser.add_argument('--fields', help='fields as a JSON string', required=True)
        PARSERS['sep31']['patch_transaction'] = patch_transaction_parser


    add_database_parser()
    add_sep1_parser()
    add_trust_parser()
    add_sep6_parser()
    add_sep10_parser()
    add_sep12_parser()
    add_sep24_parser()
    add_sep31_parser()

    return parser


def load_database(env=False):
    if not os.path.isfile(settings.DATABASE_PATH):
        print(colored('Database file does not exist. Use the "python cli.py database create" to create it.', 'yellow'))
        sys.exit(1)
    elif env:
        pw = os.getenv('WALLET_CLI_PASSWORD')
        if pw is None:
            error('Environment variable WALLET_CLI_PASSWORD is required '
                    'when using the -e/--env option')
    else:
        pw = None

    try:
        if pw is None:
            pw = getpass(magenta('Database password: '))
        data = database.read(pw)
        settings.init(data['anchor_domain'], data['stellar_network'], data['secret'])
    except ValueError:
        error('Password is incorrect or database is corrupted')


def pp(obj):
    print(json.dumps(obj, indent=2))


def print_red(message):
    cprint(message, 'red', attrs=['bold'])


def magenta(message):
    return colored(message, 'magenta', attrs=['bold'])


def error(message, parser=None):
    if parser is not None:
        print(parser.format_help())
    print_red(message)
    sys.exit(1)


def main():
    parser = argparser()
    args = parser.parse_args()

    if not args._option:
        error('No option provided')
    if not args._operation:
        error('No operation provided', PARSERS[args._option]['_'])

    if args._option == 'database':
        if args._operation == 'create':
            print('The database is an encrypted file named '
                  + colored(settings.DATABASE_NAME, 'yellow', attrs=['bold']) + ', and it\'s'
                  ' used to store these values:')
            print('- Anchor domain')
            print('- Stellar network')
            print('- Stellar account secret key')
            print('The database password and Stellar secret key will not be displayed'
                  ' on the screen while you type them.')

            if os.path.isfile(settings.DATABASE_PATH):
                cprint(
                    'Database file {} already exists, do you want to override '
                    'it? (y/N) '.format(settings.DATABASE_NAME),
                    'yellow',
                    attrs=['bold'],
                    end='',
                )
                answer = input().strip()
                if answer not in ['y', 'Y']:
                    error('')

            while True:
                pw = getpass(magenta('New database password: '))
                confirm_pw = getpass(magenta('Repeat new database password: '))
                if pw != confirm_pw:
                    print_red('Passwords mismatch')
                    continue
                break
            while True:
                secret = getpass(colored('Stellar account secret key: ', 'magenta', attrs=['bold']))
                try:
                    Keypair.from_secret(secret)
                except Ed25519SecretSeedInvalidError:
                    print_red('Invalid secret key')
                    continue
                break
            while True:
                print('Stellar network options:')
                print(' 1 - TESTNET')
                print(' 2 - PUBLIC')
                answer = input('Stellar network: ').strip()
                if answer == '1':
                    stellar_network = 'TESTNET'
                elif answer == '2':
                    stellar_network = 'PUBLIC'
                else:
                    print_red('Invalid option')
                    continue
                break
            while True:
                anchor_domain = input('Anchor domain (ex: testanchor.stellar.org): ').strip()
                try:
                    sep1.fetch_stellar_toml(anchor_domain)
                    break
                except RequestException:
                    print_red('Invalid or unreachable Anchor domain')
                    continue

            data = {
                'anchor_domain': anchor_domain,
                'secret': secret,
                'stellar_network': stellar_network,
            }
            database.write(pw, data)
            print()
            cprint('Successfully created database.bin', 'green', attrs=['bold'])


        elif args._operation == 'delete':
            try:
                os.remove(settings.DATABASE_PATH)
            except FileNotFoundError:
                error('Database file does not exist')

        elif args._operation == 'list':
            load_database(args.env)
            cprint('Database:', 'white', attrs=['bold'])
            print(' Anchor domain: ' + settings.ANCHOR_DOMAIN)
            print(' Stellar Network: ' + settings.STELLAR_NETWORK)
            print(' Account: ' + settings.PUBKEY)
    else:
        load_database(args.env)

    if args._option == 'sep1':
        if args._operation == 'fetch_stellar_toml':
            pp(sep1.fetch_stellar_toml())

    elif args._option == 'trust':
        if args._operation == 'change_trust':
            pp(trust.change_trust(args.asset_code, args.issuer, args.limit))

    elif args._option == 'sep6':
        if args._operation == 'info':
            pp(sep6.info())

        elif args._operation == 'fee':
            params = {
                'operation': args.operation,
                'asset_code': args.asset_code,
                'amount': args.amount,
            }
            if args.type:
                params['type'] = args.type
            pp(sep6.fee(params))

        elif args._operation == 'deposit':
            params = {
                'asset_code': args.asset_code,
                'account': args.account or settings.PUBKEY,
                'first_name': args.first_name,
                'last_name': args.last_name,
                'email_address': args.email_address,
                'amount': args.amount,
            }
            if args.memo_type:
                params['memo_type'] = args.memo_type
            if args.memo:
                params['memo'] = args.memo
            if args.type:
                params['type'] = args.type
            if args.wallet_name:
                params['wallet_name'] = args.wallet_name
            if args.wallet_url:
                params['wallet_url'] = args.wallet_url
            if args.lang:
                params['lang'] = args.lang
            if args.partner_ref:
                params['partner_ref'] = args.partner_ref

            pp(sep6.deposit(params, args.token))

        elif args._operation == 'withdraw':
            params = {
                'asset_code': args.asset_code,
                'amount': args.amount,
                'type': args.type,
                'dest_country': args.dest_country,
                'benef_first_name': args.benef_first_name,
                'benef_last_name': args.benef_last_name,
                'benef_email': args.benef_email,
                'benef_address': args.benef_address,
                'benef_city': args.benef_city,
            }
            if params['type'] == 'sepa':
                if not args.bank_bic:
                    error('Missing required argument --bank-bic', PARSERS['sep6']['withdraw'])
                if not args.dest:
                    error('Missing required argument --dest', PARSERS['sep6']['withdraw'])
            if args.bank_bic:
                params['bank_bic'] = args.bank_bic
            if args.dest:
                params['dest'] = args.dest
            if args.memo:
                params['memo'] = args.memo
            if args.memo_type:
                params['memo_type'] = args.memo_type
            if args.wallet_name:
                params['wallet_name'] = args.wallet_name
            if args.wallet_url:
                params['wallet_url'] = args.wallet_url
            if args.lang:
                params['lang'] = args.lang
            if args.benef_phone_number:
                params['benef_phone_number'] = args.benef_phone_number
            if args.external_memo:
                params['external_memo'] = args.external_memo

            pp(sep6.withdraw(params, args.token))

        elif args._operation == 'transaction':
            params = {}
            if args.id:
                params['id'] = args.id
            if args.stellar_transaction_id:
                params['stellar_transaction_id'] = args.stellar_transaction_id
            if args.external_transaction_id:
                params['external_transaction_id'] = args.external_transaction_id
            if not params:
                error('An argument is required', PARSERS['sep6']['transaction'])

            pp(sep6.transaction(params, args.token))

        elif args._operation == 'transactions':
            params = {
                'asset_code': args.asset_code,
            }
            if args.no_older_than:
                params['no_older_than'] = args.no_older_than
            if args.limit:
                params['limit'] = args.limit
            if args.kind:
                params['kind'] = args.kind
            if args.paging_id:
                params['paging_id'] = args.paging_id

            pp(sep6.transactions(params, args.token))

    elif args._option == 'sep10':
        if args._operation == 'auth':
            print(sep10.auth())

    elif args._option == 'sep12':
        if args._operation == 'get':
            params = {}
            if args.id:
                params['id'] = args.id
            if args.account:
                params['account'] = args.account
            if args.memo:
                params['memo'] = args.memo
            if args.memo_type:
                params['memo_type'] = args.memo_type
            if args.type:
                params['type'] = args.type
            if args.lang:
                params['lang'] = args.lang
            pp(sep12.customer_get(params, args.token))

        if args._operation == 'put':
            try:
                params = json.loads(args.data)
            except (JSONDecodeError, TypeError):
                error('data must be a JSON string', PARSERS['sep12']['put'])

            pp(sep12.customer_put(params, args.token))

    elif args._option == 'sep24':
        if args._operation == 'info':
            pp(sep24.info())

        elif args._operation == 'fee':
            params = {
                'operation': args.operation,
                'asset_code': args.asset_code,
                'amount': args.amount,
            }
            if args.type:
                params['type'] = args.type
            pp(sep24.fee(params))

        elif args._operation == 'deposit':
            try:
                params = json.loads(args.data)
            except (JSONDecodeError, TypeError):
                error('data must be a JSON string', PARSERS['sep24']['deposit'])

            pp(sep24.deposit(params, args.token))

        elif args._operation == 'withdraw':
            try:
                params = json.loads(args.data)
            except (JSONDecodeError, TypeError):
                error('data must be a JSON string', PARSERS['sep24']['withdraw'])

            pp(sep24.withdraw(params, args.token))

        elif args._operation == 'transaction':
            params = {}
            if args.id:
                params['id'] = args.id
            if args.stellar_transaction_id:
                params['stellar_transaction_id'] = args.stellar_transaction_id
            if args.external_transaction_id:
                params['external_transaction_id'] = args.external_transaction_id
            if not params:
                error('An argument is required', PARSERS['sep24']['transaction'])

            pp(sep24.transaction(params, args.token))

        elif args._operation == 'transactions':
            params = {
                'asset_code': args.asset_code,
            }
            if args.no_older_than:
                params['no_older_than'] = args.no_older_than
            if args.limit:
                params['limit'] = args.limit
            if args.kind:
                params['kind'] = args.kind
            if args.paging_id:
                params['paging_id'] = args.paging_id

            pp(sep24.transactions(params, args.token))

    elif args._option == 'sep31':
        if args._operation == 'info':
            pp(sep31.info())

        elif args._operation == 'create_transaction':
            payload = {
                'amount': args.amount,
                'asset_code': args.asset_code,
            }
            if args.fields:
                try:
                    payload['fields'] = json.loads(args.fields)
                except (JSONDecodeError, TypeError):
                    error('fields must be a JSON string', PARSERS['sep31']['create_transaction'])
            pp(sep31.transactions_post(payload))

        elif args._operation == 'get_transaction':
            pp(sep31.transactions_get(args.transaction_id))

        elif args._operation == 'patch_transaction':
            try:
                payload = {
                    'fields': json.loads(args.fields)
                }
            except (JSONDecodeError, TypeError):
                error('fields must be a JSON string', PARSERS['sep31']['patch_transaction'])
            pp(sep31.transactions_patch(args.transaction_id, payload))


if __name__ == '__main__':
    main()
