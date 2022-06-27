# The MIT License (MIT)
# Copyright (c) 2022 Gamejam.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json

from solanaetl.domain.account import Account


class AccountMapper(object):
    def json_dict_to_account(self, json_dict: dict, accountKey: str = None):
        account = Account()
        account.pubkey = accountKey
        account.executable = json_dict.get('executable')
        account.lamports = json_dict.get('lamports')
        account.owner = json_dict.get('owner')
        account.rent_epoch = json_dict.get('rentEpoch')

        data = json_dict.get('data')
        if isinstance(data, dict):
            account.space = data.get('space')
            account.program = data.get('program')
            if 'parsed' in data:
                parsed_data: dict = data.get('parsed')
                account.account_type = parsed_data.get('type')
                account_info: dict = parsed_data.get('info')
                if account_info is not None:
                    if account.account_type == 'program':
                        account.program_data = account_info.get('programData')
                    elif account.account_type == 'account':
                        account.is_native = account_info.get('isNative')
                        account.mint = account_info.get('mint')
                        account.owner = account_info.get('owner')
                        account.state = account_info.get('state')

                        token_amount: dict = account_info.get('tokenAmount')
                        if token_amount is not None:
                            account.token_amount = token_amount.get('amount')
                            account.token_amount_decimals = token_amount.get(
                                'decimals')
                    elif account.account_type == 'vote':
                        account.authorized_voters = json.dumps(
                            account_info.get('authorizedVoters'))
                        account.authorized_withdrawer = account_info.get(
                            'authorizedWithdrawer')
                        account.commission = account_info.get('commission')
                        account.epoch_credits = json.dumps(
                            account_info.get('epochCredits'))
                        account.last_timestamp = json.dumps(
                            account_info.get('lastTimestamp'))
                        account.node_pubkey = account_info.get('nodePubkey')
                        account.prior_voters = json.dumps(
                            account_info.get('priorVoters'))
                        account.root_slot = account_info.get('rootSlot')
                        account.votes = json.dumps(account_info.get('votes'))

        if account.account_type is None:
            # save raw data for unclassified account type
            account.data = json.dumps(json_dict.get('data'))

        return account

    def account_to_dict(self, account: Account):
        return {
            'type': 'account',
            'pubkey': account.pubkey,
            'executable': account.executable,
            'lamports': account.lamports,
            'owner': account.owner,
            'rent_epoch': account.rent_epoch,
            'program': account.program,
            'space': account.space,
            'account_type': account.account_type,
            'is_native': account.is_native,
            'mint': account.mint,
            'owner': account.owner,
            'state': account.state,
            'token_amount': account.token_amount,
            'token_amount_decimals': account.token_amount_decimals,
            'program_data': account.program_data,
            'authorized_voters': account.authorized_voters,
            'authorized_withdrawer': account.authorized_withdrawer,
            'prior_voters': account.prior_voters,
            'node_pubkey': account.node_pubkey,
            'commission': account.commission,
            'epoch_credits': account.epoch_credits,
            'votes': account.votes,
            'root_slot': account.root_slot,
            'last_timestamp': account.last_timestamp,
            'data': account.data,
        }
