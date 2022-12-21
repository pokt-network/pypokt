from typing import Optional
import requests
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
from ..utils import make_api_url, post


def get_app(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
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
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    Application
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/app")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return Application(**resp_data)


def get_apps(
    provider_url: str,
    height: int = 0,
    page: int = 1,
    per_page: int = 100,
    staking_status: Optional[int] = None,
    blockchain: str = "",
    session: Optional[requests.Session] = None,
) -> QueryAppsResponse:
    """
    Get a paginated list of apps on the network by search criteria

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
    staking_status: optional
        Whether or not the app is staked (2) or unstaking (1); defaults to neither.
    blockchain: optional
        The relay chain the apps are staked for.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryAppsResponse
    """
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
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryAppsResponse(**resp_data)


def get_node(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
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
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    Node
    """
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/node")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return Node(**resp_data)


def get_nodes(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 10,
    staking_status: Optional[int] = None,
    jailed_status: Optional[int] = None,
    blockchain: str = "",
    session: Optional[requests.Session] = None,
) -> QueryNodesResponse:
    """
    Get a paginated list of apps on the network by search criteria

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
    staking_status: optional
        Whether or not the node is staked (2) or unstaking (1); defaults to neither.
    jailed_status: optional
        Whether or not the node is jailed (1) or unjailed (1); defaults to neither
    blockchain: optional
        The relay chain the nodes are staked for.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryNodesResponse
    """
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
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryNodesResponse(**resp_data)


def get_signing_info(
    provider_url: str,
    address: Optional[str] = None,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    session: Optional[requests.Session] = None,
) -> QuerySigningInfoResponse:
    """
    Get either the signing info of a particular address, or a paginated list for all accounts

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address: optional
        The address of the account
    height: optional
        The height to look after
    page: optional
        The index of the page, defaults to the first page.
    per_page: optional
        The amount of results to return for each page, defaults to 100.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QuerySigningInfoResponse
    """
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/signinginfo")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QuerySigningInfoResponse(**resp_data)


def get_node_claim(
    provider_url: str,
    address: str,
    blockchain: str,
    app_pubkey: str,
    height: int,
    session_block_height: int,
    receipt_type: ReceiptType = "relay",
    session: Optional[requests.Session] = None,
) -> QueryNodeClaimResponse:
    """
    Get the specific outstanding claim for a node

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the node
    blockchain: str
        The chain the node claimed service on
    app_pubkey:
        The public key of the app the node claimed to service
    height:
        The height the claim was made
    session_block_height:
        The height of the session the node is claiming for
    receipt_type: optional
        The kind of claim; defaults to Relay
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryNodeClaimResponse
    """
    request = QueryNodeReceipt(
        address=address,
        blockchain=blockchain,
        app_pubkey=app_pubkey,
        height=height,
        session_block_height=session_block_height,
        receipt_type=receipt_type,
    )
    route = make_api_url(provider_url, "/query/nodeclaim")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryNodeClaimResponse(**resp_data)


def get_node_claims(
    provider_url: str,
    address: str = "",
    height: int = 0,
    page: int = 1,
    per_page: int = 1000,
    session: Optional[requests.Session] = None,
) -> QueryNodeClaimsResponse:
    """
    Get a paginated list of claims made by a given node

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    address
        The address of the node
    height: optional
        The height the claims were made after
    page: optional
        The index of the page, defaults to the first page.
    per_page: optional
        The amount of results to return for each page, defaults to 100.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryNodeClaimsResponse
    """
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/nodeclaims")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryNodeClaimsResponse(**resp_data)
