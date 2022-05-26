from pokt.rpc.data import get_block, get_block_transactions

from pokt.rpc.models import QueryBlockResponse, QueryBlockTXsResponse


def test_get_block(rpc_url, session, height):
    block = get_block(rpc_url, height=height, session=session)
    assert isinstance(block, QueryBlockResponse)


def test_get_block_transactions(rpc_url, session, height):
    block_txs = get_block_transactions(rpc_url, height=height, session=session)
    assert isinstance(block_txs, QueryBlockTXsResponse)
