from typing import Optional
import requests
from .errors import RelayRepsonseError, PortalRPCError, PoktRPCError
from .models import (
    RelayMetadata,
    RelayPayload,
    RelayProofVal,
    QueryChallengeRequest,
    QueryChallengeResponse,
    QueryDispatchResponse,
    QueryErrorRelayResponse,
    QueryRawTXRequest,
    QueryRawTXResponse,
    QueryRelayRequest,
    QueryRelayResponse,
    QuerySimRequest,
    SessionHeader,
)
from .utils import make_api_url, post, raw_post


def get_session(
    provider_url: str,
    app_public_key: str,
    chain: str,
    session_height: int = 0,
    session: Optional[requests.Session] = None,
) -> QueryDispatchResponse:
    request = SessionHeader(
        app_public_key=app_public_key, chain=chain, session_height=session_height
    )
    route = make_api_url(provider_url, "/client/dispatch")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryDispatchResponse(**resp_data)


def sim_relay(
    provider_url: str,
    payload: RelayPayload,
    relay_network_id: str,
    height: Optional[int] = None,
    proof: Optional[RelayProofVal] = None,
    session: Optional[requests.Session] = None,
) -> str:
    metadata = None if height is None else RelayMetadata(block_height=height)
    request = QuerySimRequest(
        payload=payload, relay_network_id=relay_network_id, meta=metadata, proof=proof
    )
    route = make_api_url(provider_url, "/client/sim")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return str(resp_data)


def send_raw_tx(
    provider_url: str,
    address: str,
    raw_hex_bytes: str,
    session: Optional[requests.Session] = None,
) -> QueryRawTXResponse:
    request = QueryRawTXRequest(address=address, raw_hex_bytes=raw_hex_bytes)
    route = make_api_url(provider_url, "/client/rawtx")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryRawTXResponse(**resp_data)


def send_challenge(
    provider_url: str,
    majority_responses: list[QueryRelayResponse],
    minority_response: QueryRelayResponse,
    address: str,
    session: Optional[requests.Session] = None,
) -> QueryChallengeResponse:
    request = QueryChallengeRequest(
        majority_responses=majority_responses,
        minority_response=minority_response,
        address=address,
    )
    route = make_api_url(provider_url, "/client/challenge")
    resp_data = post(route, session, **request.dict(by_alias=True))
    return QueryChallengeResponse(**resp_data)


def send_relay(
    provider_url: str,
    payload: RelayPayload,
    height: int,
    proof: RelayProofVal,
    session: Optional[requests.Session] = None,
) -> QueryRelayResponse:
    request = QueryRelayRequest(
        payload=payload, meta=RelayMetadata(block_height=height), proof=proof
    )
    route = make_api_url(provider_url, "/client/relay")
    resp = raw_post(route, session, **request.dict(by_alias=True))
    data = resp.json()
    error_obj = data.get("error")
    error_code = data.get("code")
    if resp.status_code == 400:
        error = QueryErrorRelayResponse(**data)
        raise RelayRepsonseError(error.error, error.dispatch)
    elif error_obj:
        raise PortalRPCError(error_obj.get("code"), error_obj.get("message"))
    elif error_code:
        raise PoktRPCError(error_code, data.get("message"))
    return QueryRelayResponse(**data)
