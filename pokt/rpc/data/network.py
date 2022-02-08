from typing import Optional
import requests
from ..models import QueryHeightResponse
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
