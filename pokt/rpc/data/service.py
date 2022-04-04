from typing import Optional
import requests
from ..models import (
    Application,
    Node,
    QueryAddressHeight,
    QueryAppsResponse,
    QueryNodesResponse,
    QueryNodeReceipt,
    QueryNodeClaimsResponse,
    StoredReceipt,
    ValidatorOpts,
    ApplicationOpts,
    QuerySigningInfoResponse,
    QueryPaginatedHeightAndAddrParams,
    QueryHeightAndApplicationsOpts,
    QueryHeightAndValidatorsOpts,
    StakingStatus,
    JailedStatus,
)
from ..utils import make_api_url, post


def get_app(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> Application:
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/app")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return Application(**resp_data)


def get_apps(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 100,
    staking_status: int = 2,
    blockchain: str = "",
    session: Optional[requests.Session] = None,
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
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryAppsResponse(**resp_data)


def get_node(
    provider_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> Node:
    request = QueryAddressHeight(height=height, address=address)
    route = make_api_url(provider_url, "/query/node")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return Node(**resp_data)


def get_nodes(
    provider_url: str,
    height: int = 0,
    page: int = 0,
    per_page: int = 10,
    staking_status: int = 2,
    jailed_status: int = 2,
    blockchain: str = "",
    session: Optional[requests.Session] = None,
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
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryNodesResponse(**resp_data)


def get_signing_info(
    provider_url: str,
    height: int = 0,
    address: Optional[str] = None,
    page: int = 0,
    per_page: int = 100,
    session: Optional[requests.Session] = None,
) -> QuerySigningInfoResponse:
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/signinginfo")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QuerySigningInfoResponse(**resp_data)


def get_node_claim(
    provider_url: str,
    address: str = "",
    blockchain: Optional[str] = None,
    app_pubkey: Optional[str] = None,
    height: int = 0,
    session_block_height: int = 0,
    session: Optional[requests.Session] = None,
) -> StoredReceipt:
    request = QueryNodeReceipt(
        address=address,
        blockchain=blockchain,
        app_pubkey=app_pubkey,
        height=height,
        session_block_height=session_block_height,
    )
    route = make_api_url(provider_url, "/query/nodeclaim")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return StoredReceipt(**resp_data)


def get_node_claims(
    provider_url: str,
    address: str = "",
    height: int = 0,
    page: int = 1,
    per_page: int = 1000,
    session: Optional[requests.Session] = None,
) -> QueryNodeClaimsResponse:
    request = QueryPaginatedHeightAndAddrParams(
        height=height, address=address, page=page, per_page=per_page
    )
    route = make_api_url(provider_url, "/query/nodeclaims")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryNodeClaimsResponse(**resp_data)
