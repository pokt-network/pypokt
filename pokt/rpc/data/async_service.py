from typing import Optional
import aiohttp
from ..models import (
    Application,
    ApplicationOpts,
    JailedStatus,
    Node,
    QueryAddressHeight,
    QueryAppsResponse,
    QueryHeightAndApplicationsOpts,
    QueryHeightAndValidatorsOpts,
    QueryNodeClaimResponse,
    QueryNodeClaimsResponse,
    QueryNodeReceipt,
    QueryNodesResponse,
    QueryPaginatedHeightAndAddrParams,
    QuerySigningInfoResponse,
    ReceiptType,
    StakingStatus,
    ValidatorOpts,
)
from ..utils import make_api_url
from ..async_utils import post_async


async def async_get_app(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[aiohttp.ClientSession] = None,
) -> Application:
    """
    Get the application by address at a specified height

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the app
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional aiohttp client session, if none is provided, the request will be handled by creating a new aiohttp client session just for this request.

    Returns
    -------
    Application
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/app")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return Application(**resp_data)


async def async_get_apps(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    staking_status: int = 2,
    blockchain: str = "",
    session: Optional[aiohttp.ClientSession] = None,
) -> QueryAppsResponse:
    if staking_status:
        staking_status = StakingStatus(staking_status)
    opts = ApplicationOpts(
        page=page,
        per_page=per_page,
        staking_status=staking_status,
        blockchain=blockchain,
    )
    request = QueryHeightAndApplicationsOpts(height=height, opts=opts)
    route = make_api_url(provider_url, "/query/apps")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryAppsResponse(**resp_data)


async def async_get_node(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[aiohttp.ClientSession] = None,
) -> Node:
    """
    Get the node by address at a specified height

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the node
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional aiohttp client session, if none is provided, the request will be handled by creating a new aiohttp client session just for this request.

    Returns
    -------
    Node
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/node")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return Node(**resp_data)


async def async_get_nodes(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 10,
    staking_status: int = 2,
    jailed_status: int = 2,
    blockchain: str = "",
    session: Optional[aiohttp.ClientSession] = None,
) -> QueryNodesResponse:
    if staking_status:
        staking_status = StakingStatus(staking_status)
    if jailed_status:
        jailed_status = JailedStatus(jailed_status)
    opts = ValidatorOpts(
        page=page,
        per_page=per_page,
        staking_status=staking_status,
        jailed_status=jailed_status,
        blockchain=blockchain,
    )
    request = QueryHeightAndValidatorsOpts(height=height, opts=opts)
    route = make_api_url(provider_url, "/query/nodes")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryNodesResponse(**resp_data)


async def async_get_signing_info(
    provider_url: str,
    address: Optional[str] = None,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    session: Optional[aiohttp.ClientSession] = None,
) -> QuerySigningInfoResponse:
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/signinginfo")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QuerySigningInfoResponse(**resp_data)


async def async_get_node_claim(
    provider_url: str,
    address: str,
    blockchain: str,
    app_pubkey: str,
    height: int,
    session_block_height: int,
    receipt_type: str,
    session: Optional[aiohttp.ClientSession] = None,
) -> QueryNodeClaimResponse:
    receipt_type = ReceiptType(receipt_type)
    request = QueryNodeReceipt(
        address=address,
        blockchain=blockchain,
        app_pubkey=app_pubkey,
        height=height,
        session_block_height=session_block_height,
        receipt_type=receipt_type,
    )
    route = make_api_url(provider_url, "/query/nodeclaim")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryNodeClaimResponse(**resp_data)


async def async_get_node_claims(
    provider_url: str,
    address: str = "",
    height: int = 0,
    page: int = 1,
    per_page: int = 1000,
    session: Optional[aiohttp.ClientSession] = None,
) -> QueryNodeClaimsResponse:
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/nodeclaims")
    resp_data = await post_async(route, session, **request.dict(by_alias=True))
    return QueryNodeClaimsResponse(**resp_data)
