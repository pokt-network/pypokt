import json
from typing import Optional
import requests

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS


class PortalRPCError(RuntimeError):
    def __init__(self, code, message):
        msg = "The following error was returned from the Portal:\n Code: {} – Message: {}".format(
            code, message
        )
        super().__init__(msg)


class PoktRPCError(RuntimeError):
    def __init__(self, code, message):
        msg = (
            "The following RPC error was encountered:\n Code: {} – Message: {}".format(
                code, message
            )
        )
        super().__init__(msg)


def make_api_url(provider_url: str, route: str, version: str = "v1") -> str:
    if not provider_url.endswith("/"):
        provider_url += "/"
    if not route.startswith("/"):
        route = "/" + route
    return provider_url + version + route


def get(route: str, session: Optional[requests.Session] = None, **params) -> str:
    if session is None:
        resp = requests.get(route, headers=DEFAULT_GET_HEADERS, params=params)
    else:
        resp = session.get(route, params=params, headers=DEFAULT_GET_HEADERS)
    return resp.text


def post(route: str, session: Optional[requests.Session] = None, **payload) -> dict:
    if session is None:
        resp = requests.post(
            route, headers=DEFAULT_POST_HEADERS, data=json.dumps(payload)
        )
    else:
        resp = session.post(
            route, data=json.dumps(payload), headers=DEFAULT_POST_HEADERS
        )
    data = resp.json()
    if isinstance(data, dict):
        error_obj = data.get("error")
        if error_obj:
            raise PortalRPCError(error_obj.get("code"), error_obj.get("message"))

        error_code = data.get("code", None)
        if error_code:
            raise PoktRPCError(error_code, data.get("message"))
    return data
