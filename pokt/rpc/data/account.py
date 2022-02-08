from typing import Optional
import requests
from ..models import (
    Account,
    QueryAccountTXs,
    QueryAccountTXsResponse,
    QueryAddressHeight,
    QueryBalanceResponse,
    SortOrder,
)
from ..utils import make_api_url, post


def get_account(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> Account:
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/account")
    resp_data = post(route, session, **request.dict())
    return Account(**resp_data)


def get_balance(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> QueryBalanceResponse:
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/balance")
    resp_data = post(route, session, **request.dict())
    return QueryBalanceResponse(**resp_data)


def get_account_transactions(
    provider_url: str,
    address: str,
    page: int = 1,
    per_page: int = 100,
    received: bool = True,
    prove: bool = False,
    order: str = "desc",
    session: Optional[requests.Session] = None,
) -> QueryAccountTXsResponse:
    order = SortOrder(order)
    request = QueryAccountTXs(
        address=address,
        page=page,
        per_page=per_page,
        received=received,
        prove=prove,
        order=order,
    )
    route = make_api_url(provider_url, "/query/accounttxs")
    resp_data = post(route, session, **request.dict())
    return QueryAccountTXsResponse(**resp_data)
