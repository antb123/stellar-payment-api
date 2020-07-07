import argparse
import json
import sys
import sep1
import trust
import sep6
import sep10
import sep24
from settings import ASSET, PUBKEY


SECRET = None
TOML = None

parsers = {}


def argparser():
    parser = argparse.ArgumentParser(description='TEMPO Stellar CLI Example')
    option_subparsers = parser.add_subparsers(help='option', dest='_option')

    def add_sep1_parser():
        sep1_parser = option_subparsers.add_parser('sep1')
        parsers['sep1'] = {}
        parsers['sep1']['_'] = sep1_parser
        sep1_subparsers = sep1_parser.add_subparsers(description='operations', dest='_operation')
        fetch_stellar_toml_parser = sep1_subparsers.add_parser('fetch_stellar_toml')
        parsers['sep1']['fetch_stellar_toml'] = fetch_stellar_toml_parser

    def add_trust_parser():
        trust_parser = option_subparsers.add_parser('trust')
        parsers['trust'] = {}
        parsers['trust']['_'] = trust_parser
        trust_subparsers = trust_parser.add_subparsers(description='operations', dest='_operation')
        change_trust_parser = trust_subparsers.add_parser('change_trust')
        change_trust_parser.add_argument('--asset-code')
        change_trust_parser.add_argument('--issuer')
        change_trust_parser.add_argument('--limit')
        parsers['trust']['change_trust'] = change_trust_parser

    def add_sep6_parser():
        sep6_parser = option_subparsers.add_parser('sep6')
        parsers['sep6'] = {}
        parsers['sep6']['_'] = sep6_parser
        sep6_subparsers = sep6_parser.add_subparsers(description='operations', dest='_operation')

        info_parser = sep6_subparsers.add_parser('info')
        parsers['sep6']['info'] = info_parser

        fee_parser = sep6_subparsers.add_parser('fee')
        fee_parser.add_argument('--operation', required=True)
        fee_parser.add_argument('--amount', required=True)
        fee_parser.add_argument('--asset-code')
        fee_parser.add_argument('--type')
        parsers['sep6']['fee'] = fee_parser

        deposit_parser = sep6_subparsers.add_parser('deposit')
        deposit_parser.add_argument('--first-name', required=True)
        deposit_parser.add_argument('--last-name', required=True)
        deposit_parser.add_argument('--email-address', required=True)
        deposit_parser.add_argument('--amount', required=True)
        deposit_parser.add_argument('--account')
        deposit_parser.add_argument('--asset-code')
        deposit_parser.add_argument('--memo-type')
        deposit_parser.add_argument('--memo')
        deposit_parser.add_argument('--type', choices=['sepa', 'cash'])
        deposit_parser.add_argument('--wallet-name')
        deposit_parser.add_argument('--wallet-url')
        deposit_parser.add_argument('--lang')
        deposit_parser.add_argument('--partner-ref')
        deposit_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep6']['deposit'] = deposit_parser

        withdraw_parser = sep6_subparsers.add_parser('withdraw')
        withdraw_parser.add_argument('--amount', required=True)
        withdraw_parser.add_argument('--type', required=True, choices=['sepa', 'cash'])
        withdraw_parser.add_argument('--dest-country', required=True)
        withdraw_parser.add_argument('--benef-first-name', required=True)
        withdraw_parser.add_argument('--benef-last-name', required=True)
        withdraw_parser.add_argument('--benef-email', required=True)
        withdraw_parser.add_argument('--benef-address', required=True)
        withdraw_parser.add_argument('--benef-city', required=True)
        withdraw_parser.add_argument('--bank-bic', help='required if type is sepa')
        withdraw_parser.add_argument('--dest', help='required if type is sepa')
        withdraw_parser.add_argument('--asset-code')
        withdraw_parser.add_argument('--memo')
        withdraw_parser.add_argument('--memo-type')
        withdraw_parser.add_argument('--wallet-name')
        withdraw_parser.add_argument('--wallet-url')
        withdraw_parser.add_argument('--lang')
        withdraw_parser.add_argument('--benef-phone-number')
        withdraw_parser.add_argument('--external-memo')
        withdraw_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep6']['withdraw'] = withdraw_parser

        transaction_parser = sep6_subparsers.add_parser('transaction')
        transaction_parser.add_argument('--id')
        transaction_parser.add_argument('--stellar-transaction-id')
        transaction_parser.add_argument('--external-transaction-id')
        transaction_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep6']['transaction'] = transaction_parser

        transactions_parser = sep6_subparsers.add_parser('transactions')
        transactions_parser.add_argument('--asset-code')
        transactions_parser.add_argument('--no-older-than')
        transactions_parser.add_argument('--limit')
        transactions_parser.add_argument('--kind')
        transactions_parser.add_argument('--paging-id')
        transactions_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep6']['transactions'] = transactions_parser

    def add_sep10_parser():
        sep10_parser = option_subparsers.add_parser('sep10')
        parsers['sep10'] = {}
        parsers['sep10']['_'] = sep10_parser
        sep10_subparsers = sep10_parser.add_subparsers(description='operations', dest='_operation')
        auth_parser = sep10_subparsers.add_parser('auth')
        parsers['sep10']['auth'] = auth_parser

    def add_sep24_parser():
        sep24_parser = option_subparsers.add_parser('sep24')
        parsers['sep24'] = {}
        parsers['sep24']['_'] = sep24_parser
        sep24_subparsers = sep24_parser.add_subparsers(description='operations', dest='_operation')

        info_parser = sep24_subparsers.add_parser('info')
        parsers['sep24']['info'] = info_parser

        fee_parser = sep24_subparsers.add_parser('fee')
        fee_parser.add_argument('--operation', required=True)
        fee_parser.add_argument('--amount', required=True)
        fee_parser.add_argument('--asset-code')
        fee_parser.add_argument('--type')
        parsers['sep24']['fee'] = fee_parser

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
        parsers['sep24']['deposit'] = deposit_parser

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
        parsers['sep24']['withdraw'] = withdraw_parser

        transaction_parser = sep24_subparsers.add_parser('transaction')
        transaction_parser.add_argument('--id')
        transaction_parser.add_argument('--stellar-transaction-id')
        transaction_parser.add_argument('--external-transaction-id')
        transaction_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep24']['transaction'] = transaction_parser

        transactions_parser = sep24_subparsers.add_parser('transactions')
        transactions_parser.add_argument('--asset-code')
        transactions_parser.add_argument('--no-older-than')
        transactions_parser.add_argument('--limit')
        transactions_parser.add_argument('--kind')
        transactions_parser.add_argument('--paging-id')
        transactions_parser.add_argument('--token', help='SEP10 auth token')
        parsers['sep24']['transactions'] = transactions_parser

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
        print(parser.format_help())
        sys.exit(1)
    if not args._operation:
        print('No operation provided')
        print(parsers[args._option]['_'].format_help())
        sys.exit(1)

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
        if args._operation == 'info':
            pp(sep6.info())

        elif args._operation == 'fee':
            params = {
                'operation': args.operation,
                'asset_code': args.asset_code or ASSET['code'],
                'amount': args.amount,
            }
            if args.type:
                params['type'] = args.type
            pp(sep6.fee(params))

        elif args._operation == 'deposit':
            params = {
                'asset_code': args.asset_code or ASSET['code'],
                'account': args.account or PUBKEY,
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
                'asset_code': args.asset_code or ASSET['code'],
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
                    print('Missing required argument --bank-bic')
                    print(parsers['sep6']['withdraw'].format_help())
                    sys.exit(1)
                if not args.dest:
                    print('Missing required argument --dest')
                    print(parsers['sep6']['withdraw'].format_help())
                    sys.exit(1)
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
                print('An argument is required')
                print(parsers['sep6']['transaction'].format_help())
                sys.exit(1)

            pp(sep6.transaction(params, args.token))

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

            pp(sep6.transactions(params, args.token))

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
            if not params:
                print('An argument is required')
                print(parsers['sep24']['transaction'].format_help())
                sys.exit(1)

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
