from typing import Optional
import aiohttp
from ..models import (
    BaseAccountVal,
    QueryAccountsResponse,
    QueryAccountTXs,
    QueryAccountTXsResponse,
    QueryAddressHeight,
    QueryBalanceResponse,
    QueryPaginatedHeightParams,
    SortOrder,
)
from ..utils import make_api_url
from ..async_utils import post_async


async def async_get_account(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[aiohttp.ClientSession] = None,
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
        The optional aiohttp client session, if none is provided, the request will be handled by creating a new aiohttp client session just for this request.

    Returns
    -------
    Account
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/account")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return Account(**resp_data)


async def async_get_accounts(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    session: Optional[aiohttp.ClientSession] = None,
) -> QueryAccountsResponse:
    request = QueryPaginatedHeightParams(height=height, page=page, per_page=per_page)
    route = make_api_url(provider_url, "/query/accounts")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryAccountsResponse(**resp_data)


async def async_get_balance(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[aiohttp.ClientSession] = None,
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
        The optional aiohttp client session, if none is provided, the request will be handled by creating a new aiohttp client session just for this request.

    Returns
    -------
    QueryBalanceResponse
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/balance")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryBalanceResponse(**resp_data)


async def async_get_account_transactions(
    provider_url: str,
    address: str,
    page: int = 0,
    per_page: int = 100,
    received: bool = True,
    prove: bool = False,
    order: SortOrder = "desc",
    session: Optional[aiohttp.ClientSession] = None,
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
        The optional aiohttp client session, if none is provided, the request will be handled by creating a new aiohttp client session just for this request.

    Returns
    -------
    QueryAccountTXsResponse
    """
    request = QueryAccountTXs(
        address=address,
        page=page,
        per_page=per_page,
        received=received,
        prove=prove,
        order=order,
    )
    route = make_api_url(provider_url, "/query/accounttxs")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryAccountTXsResponse(**resp_data)
