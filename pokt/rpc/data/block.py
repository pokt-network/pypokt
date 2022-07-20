from typing import Optional
import requests
from ..models import (
    SortOrder,
    QueryBlock,
    QueryBlockResponse,
    QueryBlockTXs,
    QueryBlockTXsResponse,
)
from ..utils import make_api_url, post


def get_block(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> QueryBlockResponse:
    """
    Get the block at a specified height.


    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryBlockResponse
    """
    request = QueryBlock(height=height)
    route = make_api_url(provider_url, "/query/block")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryBlockResponse(**resp_data)


def get_block_transactions(
    provider_url: str,
    height: int = 0,
    page: int = 1,
    per_page: int = 100,
    prove: bool = False,
    order: str = "desc",
    session: Optional[requests.Session] = None,
) -> QueryBlockTXsResponse:
    """
    Get a list of transactions from the block at the specfified height.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    page: optional
        The index of the page, defaults to the first page.
    per_page: optional
        The amount of results to return for each page, defaults to 100.
    received: optional
        Whether to include only received transactions, defaults to True.
    prove: optional
        If you want to be certain that the transaction is from the block, it's inherited from TM.
        If this is true, txs.proof = null.
    order: optional
        The order that the results should be sorted in, either 'desc' or 'asc', defaults to 'desc'
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryBlockTXsResponse
    """
    order = SortOrder(order)
    request = QueryBlockTXs(
        height=height, page=page, per_page=per_page, prove=prove, order=order
    )
    route = make_api_url(provider_url, "/query/blocktxs")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryBlockTXsResponse(**resp_data)
