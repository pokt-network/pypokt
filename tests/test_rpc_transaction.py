import pytest
from pokt.rpc.data import get_transaction_by_hash

from pokt.rpc.models import Transaction

# TODO: Find hashes of the rest of the Transaction types
@pytest.mark.parametrize(
    "tx_hash",
    ("0485137A23D1D7ED188AF23F47C7A089253E582F241338094B18249371D5FFD5",),
    ids=("send",),
)
def test_get_transatcion(rpc_url, session, tx_hash):
    tx = get_transaction_by_hash(rpc_url, tx_hash, session=session)
    assert isinstance(tx, Transaction)
