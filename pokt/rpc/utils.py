from urllib.parse import urljoin
from typing import Optional
import requests

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS


def make_api_url(provider_url: str, route: str, version: str = "v1") -> str:
    return urljoin(provider_url, urljoin(version, route))


def get(route: str, session: Optional[requests.Session] = None, **params) -> str:
    if session is None:
        resp = requests.get(route, headers=DEFAULT_GET_HEADERS, params=params)
    else:
        resp = session.get(route, params=params, headers=DEFAULT_GET_HEADERS)
    return resp.text


def post(route: str, session: Optional[requests.Session] = None, **payload) -> dict:
    if session is None:
        resp = requests.post(route, headers=DEFAULT_POST_HEADERS, data=payload)
    else:
        resp = session.post(route, data=payload, headers=DEFAULT_POST_HEADERS)
    return resp.json()
