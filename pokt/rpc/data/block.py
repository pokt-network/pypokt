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
    request = QueryBlock(height=height)
    route = make_api_url(provider_url, "/query/block")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryBlockResponse(**resp_data)


def get_block_transactions(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    prove: bool = False,
    order: str = "desc",
    session: Optional[requests.Session] = None,
) -> QueryBlockTXsResponse:
    order = SortOrder(order)
    request = QueryBlockTXs(
        height=height, page=page, per_page=per_page, prove=prove, order=order
    )
    route = make_api_url(provider_url, "/query/blocktxs")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryBlockTXsResponse(**resp_data)
