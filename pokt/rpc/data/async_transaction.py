from typing import Optional
import aiohttp
from ..models import QueryTX, QueryUnconfirmedTX, Transaction, UnconfirmedTransaction
from ..utils import make_api_url
from ..async_utils import post_async


async def async_get_unconfirmed_transaction_by_hash(
    provider_url: str,
    tx_hash: str,
    session: Optional[aiohttp.ClientSession] = None,
) -> UnconfirmedTransaction:
    """
    Get a specific transaction by hash.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    tx_hash
        The hash of the transaction
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    UnconfirmedTransaction
    """
    request = QueryUnconfirmedTX(hash=tx_hash)
    route = make_api_url(provider_url, "/query/tx")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return UnconfirmedTransaction(**resp_data)


async def async_get_transaction_by_hash(
    provider_url: str,
    tx_hash: str,
    prove: bool = False,
    session: Optional[aiohttp.ClientSession] = None,
) -> Transaction:
    """
    Get a specific transaction by hash.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    tx_hash
        The hash of the transaction
    prove: optional
        Whether or not to inclue to proof of the transaction, defaults to False.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    Transaction
    """
    request = QueryTX(hash=tx_hash, prove=prove)
    route = make_api_url(provider_url, "/query/tx")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return Transaction(**resp_data)
