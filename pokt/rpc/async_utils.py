import json
from typing import Optional

try:
    import aiohttp
except ImportError:
    raise RuntimeError(
        "The optional dependencies for async RPC requests don't appear to be installed. These can be installed via 'pip install pypokt[async]'."
    )

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS, PortalRPCError, PoktRPCError


async def _get_ad_hoc(route: str, **params) -> str:
    async with aiohttp.ClientSession(headers=DEFAULT_GET_HEADERS) as session:
        async with session.get(route, params=params) as resp:
            try:
                data = await resp.json()
            except:
                pass
            else:
                if isinstance(data, dict):
                    error_obj = data.get("error")
                    if error_obj:
                        error_code = error_obj.get("code", None)
                        if error_code is None:
                            error_code = error_obj.get("statusCode", None)
                        raise PortalRPCError(error_code, error_obj.get("message"))

                    error_code = data.get("code", None)
                    if error_code:
                        raise PoktRPCError(error_code, data.get("message"))
            return await resp.text()


async def get_async(
    route: str, session: Optional[aiohttp.ClientSession], **params
) -> str:
    if session is None:
        return await _get_ad_hoc(route, **params)
    async with session.get(route, params=params, headers=DEFAULT_GET_HEADERS) as resp:
        try:
            data = await resp.json()
        except:
            pass
        else:
            if isinstance(data, dict):
                error_obj = data.get("error")
                if error_obj:
                    error_code = error_obj.get("code", None)
                    if error_code is None:
                        error_code = error_obj.get("statusCode", None)
                    raise PortalRPCError(error_code, error_obj.get("message"))

                error_code = data.get("code", None)
                if error_code:
                    raise PoktRPCError(error_code, data.get("message"))
        return await resp.text()


async def _post_ad_hoc(route: str, **data) -> dict:
    async with aiohttp.ClientSession(headers=DEFAULT_POST_HEADERS) as session:
        async with session.post(route, data=json.dumps(data)) as resp:
            data = await resp.json()
            if isinstance(data, dict):
                error_obj = data.get("error")
                if error_obj:
                    raise PortalRPCError(
                        error_obj.get("code"), error_obj.get("message")
                    )

                error_code = data.get("code", None)
                if error_code:
                    raise PoktRPCError(error_code, data.get("message"))
            return data


async def post_async(
    route: str, session: Optional[aiohttp.ClientSession], **data
) -> dict:
    if session is None:
        return await _post_ad_hoc(route, **data)
    async with session.post(
        route, data=json.dumps(data), headers=DEFAULT_POST_HEADERS
    ) as resp:
        data = await resp.json()
        if isinstance(data, dict):
            error_obj = data.get("error")
            if error_obj:
                raise PortalRPCError(error_obj.get("code"), error_obj.get("message"))

            error_code = data.get("code", None)
            if error_code:
                raise PoktRPCError(error_code, data.get("message"))
        return data
