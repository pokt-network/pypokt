from typing import Optional, TYPE_CHECKING

from .response_models import (
    AccountTxResponse,
    BalanceResponse,
    HeightResponse,
    SupplyResponse,
    SupportedChainsResponse,
)
from .request_models import AccountTxRequest, BalanceRequest, HeightRequest

import requests

if TYPE_CHECKING:
    from pydantic import BaseModel


def _post(
    req: BaseModel, rpc_url: str, session: Optional[requests.Session] = None
) -> dict:
    if session is not None:
        resp = session.post(rpc_url, json=req.dict())
    else:
        resp = requests.post(rpc_url, json=req.dict())
    return resp.json()


def get_account_txs(
    rpc_url: str,
    address: str,
    height: int = 0,
    page: int = 1,
    per_page: int = 1000,
    sort: str = "desc",
    session: Optional[requests.Session] = None,
) -> AccountTxResponse:
    req = AccountTxRequest(
        address=address, height=height, page=page, per_page=per_page, sort=sort
    )
    resp = _post(req, rpc_url, session)
    return AccountTxResponse(**resp)


def get_balance(
    rpc_url: str,
    address: str,
    height: int = 0,
    session: Optional[requests.Session] = None,
) -> BalanceResponse:
    req = BalanceRequest(address=address, height=height)
    resp = _post(req, rpc_url, session)
    return BalanceResponse(**resp)


def get_height(
    rpc_url: str, session: Optional[requests.Session] = None
) -> HeightResponse:
    if session is not None:
        resp = session.post(rpc_url, json={}).json()
    else:
        resp = requests.post(rpc_url, json={}).json()
    return HeightResponse(**resp)


def get_supply(
    rpc_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> SupplyResponse:
    req = HeightRequest(height=height)
    resp = _post(req, rpc_url, session)
    return SupplyResponse(**resp)


def get_supported_chains(
    rpc_url: str, height: int = 0, session: Optional[requests.Session] = None
) -> SupportedChainsResponse:
    req = HeightRequest(height=height)
    resp = _post(req, rpc_url, session)
    return SupportedChainsResponse(**resp)


def _get_current_params(height=0):
    req = HeightRequest(height=height)
