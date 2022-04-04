from typing import Optional
import requests
from ..models import QueryTX, Transaction
from ..utils import make_api_url, post


def get_transaction_by_hash(
    provider_url: str,
    tx_hash: str,
    prove: bool = False,
    session: Optional[requests.Session] = None,
) -> Transaction:
    request = QueryTX(hash=tx_hash, prove=prove)
    route = make_api_url(provider_url, "/query/tx")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return Transaction(**resp_data)
