import json
from typing import Optional
import requests
from pydantic import parse_obj_as
from ..models import (
    AllParams,
    ParamT,
    SingleParam,
    QueryHeight,
    QueryHeightAndKey,
    QueryHeightResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    StateResponse,
    Upgrade,
)
from ..utils import make_api_url, get, post


def get_version(provider_url: str, session: Optional[requests.Session] = None) -> str:
    """
     Get the current version.

    Parameters
     ----------
     provider_url
         The URL to make the RPC call to.
     session: optional
         The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

     Returns
     -------
     str
    """
    route = make_api_url(provider_url, "/")
    return get(route, session)


def get_height(
    provider_url: str, session: Optional[requests.Session] = None
) -> QueryHeightResponse:
    """
    Get the current height of the network.

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    QueryHeightResponse
    """
    route = make_api_url(provider_url, "/query/height")
    resp_data = post(route, session)
    return QueryHeightResponse(**resp_data)


def get_state(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> StateResponse:  # Dict[AnyStr, Any]:
    """
    Get the network state at a specified height.

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
    StateResponse
    """
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/state")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return StateResponse(**resp_data)


def get_supply(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> QuerySupplyResponse:
    """
    Get the supply infomration at a specified height.

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
    QuerySupplyResponse
    """
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/supply")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QuerySupplyResponse(**resp_data)


def get_supported_chains(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> QuerySupportedChainsResponse:
    """
    Get the list of supported chain ids at a specified height.


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
    QuerySupportedChainsResponse
    """
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/supportedchains")
    resp_data = post(route, session, **request.dict(by_alias=True))
    if isinstance(resp_data, str):
        resp_data = json.loads(resp_data)
    return QuerySupportedChainsResponse(supported_chains=resp_data)


def get_upgrade(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> Upgrade:
    """
    Get the upgrade information at a specified height.


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
    Upgrade
    """
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/upgrade")
    resp_data = post(route, session, **request.dict(by_alias=True))
    if isinstance(resp_data, str):
        resp_data = json.loads(resp_data)
    return Upgrade(**resp_data)


def get_param(
    provider_url: str,
    param_key: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> ParamT:
    """
    Get the value of the desired protocol parameter at a specified height

    Parameters
    ----------
    provider_url
        The URL to make the RPC call to.
    param_key
        The key to the desired parameter
    height: optional
        The height to get the state at, if none is provided, defaults to the latest height.
    session: optional
        The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

    Returns
    -------
    Any
    """
    request = QueryHeightAndKey(height=height, key=param_key)
    route = make_api_url(provider_url, "/query/param")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return parse_obj_as(SingleParam, resp_data).__root__


def get_all_params(
    provider_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> AllParams:
    """
    Get the values of all protocol parameters at a specified height.


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
    AllParams
    """
    request = QueryHeight(height=height)
    route = make_api_url(provider_url, "/query/allParams")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return AllParams(**resp_data)
