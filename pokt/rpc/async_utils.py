from typing import Optional

try:
    import aiohttp
except ImportError:
    raise RuntimeError(
        "The optional dependencies for async RPC requests don't appear to be installed. These can be installed via 'pip install pypocket[async]'."
    )

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS


async def _get_ad_hoc(route: str, **params) -> str:
    async with aiohttp.ClientSession(headers=DEFAULT_GET_HEADERS) as session:
        async with session.get(route, params=params) as resp:
            return await resp.text()


async def get_async(
    route: str, session: Optional[aiohttp.ClientSession], **params
) -> str:
    if session is None:
        return await _get_ad_hoc(route, **params)
    async with session.get(route, params=params, headers=DEFAULT_GET_HEADERS) as resp:
        return await resp.test()


async def _post_ad_hoc(route: str, **data) -> dict:
    async with aiohttp.ClientSession(headers=DEFAULT_POST_HEADERS) as session:
        async with session.post(route, data=data) as resp:
            return await resp.json()


async def post_async(
    route: str, session: Optional[aiohttp.ClientSession], **data
) -> dict:
    if session is None:
        return await _post_ad_hoc(route, **data)
    async with session.post(route, data=data, headers=DEFAULT_POST_HEADERS) as resp:
        return await resp.json()
