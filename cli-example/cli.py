import argparse
import json
import sep1
import trust
import sep6
import sep10
import sep24
from settings import ASSET, PUBKEY


SECRET = None
TOML = None


def argparser():
    parser = argparse.ArgumentParser(description='TEMPO Stellar CLI Example')
    option_subparsers = parser.add_subparsers(help='option', dest='_option')

    def add_sep1_parser():
        sep1_parser = option_subparsers.add_parser('sep1')
        sep1_subparsers = sep1_parser.add_subparsers(help='operation', dest='_operation')
        fetch_stellar_toml = sep1_subparsers.add_parser('fetch_stellar_toml')

    def add_trust_parser():
        trust_parser = option_subparsers.add_parser('trust')
        trust_subparsers = trust_parser.add_subparsers(help='operation', dest='_operation')
        change_trust = trust_subparsers.add_parser('change_trust')
        change_trust.add_argument('--asset-code')
        change_trust.add_argument('--issuer')
        change_trust.add_argument('--limit')

    def add_sep6_parser():
        pass

    def add_sep10_parser():
        sep10_parser = option_subparsers.add_parser('sep10')
        sep10_subparsers = sep10_parser.add_subparsers(help='operation', dest='_operation')
        auth_parser = sep10_subparsers.add_parser('auth')

    def add_sep24_parser():
        sep24_parser = option_subparsers.add_parser('sep24')
        sep24_subparsers = sep24_parser.add_subparsers(help='operation', dest='_operation')

        info_parser = sep24_subparsers.add_parser('info')

        fee_parser = sep24_subparsers.add_parser('fee')
        fee_parser.add_argument('--operation', required=True)
        fee_parser.add_argument('--amount', required=True)
        fee_parser.add_argument('--asset-code')
        fee_parser.add_argument('--type')

        deposit_parser = sep24_subparsers.add_parser('deposit')
        deposit_parser.add_argument('--account')
        deposit_parser.add_argument('--asset-code')
        deposit_parser.add_argument('--asset-issuer')
        deposit_parser.add_argument('--amount')
        deposit_parser.add_argument('--memo-type')
        deposit_parser.add_argument('--memo')
        deposit_parser.add_argument('--wallet-name')
        deposit_parser.add_argument('--wallet-url')
        deposit_parser.add_argument('--lang')
        deposit_parser.add_argument('--token', help='SEP10 auth token')

        withdraw_parser = sep24_subparsers.add_parser('withdraw')
        withdraw_parser.add_argument('--asset-code')
        withdraw_parser.add_argument('--asset-issuer')
        withdraw_parser.add_argument('--amount')
        withdraw_parser.add_argument('--account')
        withdraw_parser.add_argument('--memo')
        withdraw_parser.add_argument('--memo-type')
        withdraw_parser.add_argument('--wallet-name')
        withdraw_parser.add_argument('--wallet-url')
        withdraw_parser.add_argument('--lang')
        withdraw_parser.add_argument('--token', help='SEP10 auth token')

        transaction_parser = sep24_subparsers.add_parser('transaction')
        transaction_parser.add_argument('--id')
        transaction_parser.add_argument('--stellar-transaction-id')
        transaction_parser.add_argument('--external-transaction-id')
        transaction_parser.add_argument('--token', help='SEP10 auth token')

        transactions_parser = sep24_subparsers.add_parser('transactions')
        transactions_parser.add_argument('--asset-code')
        transactions_parser.add_argument('--no-older-than')
        transactions_parser.add_argument('--limit')
        transactions_parser.add_argument('--kind')
        transactions_parser.add_argument('--paging-id')
        transactions_parser.add_argument('--token', help='SEP10 auth token')

    add_sep1_parser()
    add_trust_parser()
    add_sep6_parser()
    add_sep10_parser()
    add_sep24_parser()

    return parser


def pp(obj):
    print(json.dumps(obj, indent=2))


def main():
    parser = argparser()
    args = parser.parse_args()

    if not args._option:
        print('No option provided')
    if not args._operation:
        print('No operation provided')

    if args._option == 'sep1':
        if args._operation == 'fetch_stellar_toml':
            pp(sep1.fetch_stellar_toml())

    elif args._option == 'trust':
        if args._operation == 'change_trust':
            pp(trust.change_trust(args.asset_code or ASSET['code'],
                                  args.issuer or ASSET['issuer'],
                                  args.limit))

    elif args._option == 'sep10':
        if args._operation == 'auth':
            print(sep10.auth())

    elif args._option == 'sep6':
        pass

    elif args._option == 'sep24':
        if args._operation == 'info':
            pp(sep24.info())

        elif args._operation == 'fee':
            params = {
                'operation': args.operation,
                'asset_code': args.asset_code or ASSET['code'],
                'amount': args.amount,
            }
            if args.type:
                params['type'] = args.type
            pp(sep24.fee(params))

        elif args._operation == 'deposit':
            params = {
                'asset_code': args.asset_code or ASSET['code'],
                'account': args.account or PUBKEY,
            }
            if args.asset_issuer:
                params['asset_issuer'] = args.asser_issuer
            if args.amount:
                params['amount'] = args.amount
            if args.memo_type:
                params['memo_type'] = args.memo_type
            if args.memo:
                params['memo'] = args.memo
            if args.wallet_name:
                params['wallet_name'] = args.wallet_name
            if args.wallet_url:
                params['wallet_url'] = args.wallet_url
            if args.lang:
                params['lang'] = args.lang

            pp(sep24.deposit(params, args.token))

        elif args._operation == 'withdraw':
            params = {
                'asset_code': args.asset_code or ASSET['code']
            }
            if args.asset_issuer:
                params['asset_issuer'] = args.asset_issuer
            if args.amount:
                params['amount'] = args.amount
            if args.account:
                params['account'] = args.account
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

            pp(sep24.withdraw(params, args.token))

        elif args._operation == 'transaction':
            params = {}
            if args.id:
                params['id'] = args.id
            if args.stellar_transaction_id:
                params['stellar_transaction_id'] = args.stellar_transaction_id
            if args.external_transaction_id:
                params['external_transaction_id'] = args.external_transaction_id

            pp(sep24.transaction(params, args.token))

        elif args._operation == 'transactions':
            params = {
                'asset_code': args.asset_code or ASSET['code'],
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


if __name__ == '__main__':
    main()
