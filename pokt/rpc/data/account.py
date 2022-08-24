from typing import Optional
import requests
from ..models import (
    BaseAccountVal,
    QueryAccountTXs,
    QueryAccountTXsResponse,
    QueryAddressHeight,
    QueryBalanceResponse,
    QueryPaginatedHeightParams,
    QueryAccountsResponse,
    SortOrder,
)
from ..utils import make_api_url, post


def get_account(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> BaseAccountVal:
    """
    Get the account with the given address at a specified height.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the account
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    BaseAccountVal
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/account")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return BaseAccountVal(**resp_data)


def get_accounts(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    session: Optional[requests.Session] = None,
) -> QueryAccountsResponse:
    request = QueryPaginatedHeightParams(height=height, page=page, per_page=per_page)
    route = make_api_url(provider_url, "/query/accounts")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryAccountsResponse(**resp_data)


def get_balance(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> QueryBalanceResponse:
    """
    Get the balance of the account at the given address at a specified height.


    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the account
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryBalanceResponse
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/balance")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryBalanceResponse(**resp_data)


def get_account_transactions(
    provider_url: str,
    address: str,
    page: int = 0,
    per_page: int = 100,
    received: bool = True,
    prove: bool = False,
    order: str = "desc",
    session: Optional[requests.Session] = None,
) -> QueryAccountTXsResponse:
    """
    Get a list of transactions for a given account at a specified height.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the account
    page: optional
        The index of the page, defaults to the first page.
    per_page: optional
        The amount of results to return for each page, defaults to 100.
    received: optional
        Whether to include only received transactions, defaults to True.
    prove: optional
        Whether to include only proof transactions, defaults to False.
    order: optional
        The order that the results should be sorted in, either 'desc' or 'asc', defaults to 'desc'
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryAccountTXsResponse
    """
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
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryAccountTXsResponse(**resp_data)
