from typing import Any, Dict, AnyStr, Optional
import requests
from ..models import (
    AllParams,
    QueryHeight,
    QueryHeightAndKey,
    QueryHeightResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    SingleParam,
    UpgradeResponse,
)
from ..utils import make_api_url, get, post


def get_version(provider_url: str, session: Optional[requests.Session] = None) -> str:
    route = make_api_url(provider_url, "/")
    return get(route, session)


def get_height(
    provider_url: str, session: Optional[requests.Session] = None
) -> QueryHeightResponse:
    route = make_api_url(provider_url, "/query/height")
    resp_data = post(route, session)
    return QueryHeightResponse(**resp_data)


def get_state(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> Dict[AnyStr, Any]:
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/state")
    resp_data = post(route, session, **request.dict())
    return resp_data


def get_supply(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> QuerySupplyResponse:
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/supply")
    resp_data = post(route, session, **request.dict())
    return QuerySupplyResponse(**resp_data)


def get_supported_chains(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> QuerySupportedChainsResponse:
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/supportedchains")
    resp_data = post(route, session, **request.dict())
    return QuerySupportedChainsResponse(**resp_data)


def get_upgrade(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> UpgradeResponse:
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/upgrade")
    resp_data = post(route, session, **request.dict())
    return UpgradeResponse(**resp_data)


def get_param(
    provider_url: str,
    param_key: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> SingleParam:
    request = QueryHeightAndKey(height=height, key=param_key)
    route = make_api_url(provider_url, "/query/param")
    resp_data = post(route, session, **request.dict())
    return SingleParam(**resp_data)


def get_all_params(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> AllParams:
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/allParams")
    resp_data = post(route, session, **request.dict())
    return AllParams(**resp_data)
