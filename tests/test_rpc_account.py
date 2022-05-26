from pokt.rpc.data import get_account, get_account_transactions
from pokt.rpc.models import Account, QueryAccountTXsResponse


def test_get_account(rpc_url, session, height, account_address):
    account = get_account(rpc_url, account_address, height=height, session=session)
    assert isinstance(account, Account)


def test_get_account_transactions(rpc_url, session, account_address):
    account_txs = get_account_transactions(rpc_url, account_address, session=session)
    assert isinstance(account_txs, QueryAccountTXsResponse)
