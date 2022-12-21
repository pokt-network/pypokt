from pokt.rpc.models.responses import QueryUnconfirmedTXResponse
from fastapi import APIRouter, Depends

from .conf import ProxySettings, settings

from ..data.async_account import (
    async_get_account,
    async_get_accounts,
    async_get_account_transactions,
    async_get_balance,
    BaseAccountVal,
    QueryPaginatedHeightParams,
    QueryAddressHeight,
    QueryAccountsResponse,
    QueryAccountTXs,
    QueryAccountTXsResponse,
    QueryBalanceResponse,
)
from ..data.async_block import (
    async_get_block,
    async_get_block_transactions,
    QueryBlock,
    QueryBlockResponse,
    QueryBlockTXs,
    QueryBlockTXsResponse,
)
from ..data.async_network import (
    AllParams,
    ParamT,
    QueryHeight,
    QueryHeightAndKey,
    QueryHeightResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    QueryUnconfirmedTXs,
    QueryUnconfirmedTXsResponse,
    StateResponse,
    Upgrade,
    async_get_all_params,
    async_get_height,
    async_get_mempool_txs,
    async_get_param,
    async_get_state,
    async_get_supply,
    async_get_supported_chains,
    async_get_upgrade,
)
from ..data.async_service import (
    async_get_app,
    async_get_apps,
    async_get_node,
    async_get_node_claim,
    async_get_node_claims,
    async_get_nodes,
    async_get_signing_info,
    Application,
    Node,
    QueryAddressHeight,
    QueryAppsResponse,
    QueryNodesResponse,
    QueryHeightAndApplicationsOpts,
    QueryHeightAndValidatorsOpts,
    QueryPaginatedHeightAndAddrParams,
    QuerySigningInfoResponse,
    QueryNodeReceipt,
    QueryNodeClaimResponse,
    QueryNodeClaimsResponse,
)
from ..data.async_transaction import (
    async_get_transaction_by_hash,
    async_get_unconfirmed_transaction_by_hash,
    QueryTX,
    QueryUnconfirmedTX,
    Transaction,
    UnconfirmedTransaction,
)


router = APIRouter(prefix="/v1/query")


@router.post("/account", response_model=BaseAccountVal, tags=["account"])
async def account(
    req: QueryAddressHeight, conf: ProxySettings = Depends(settings)
) -> BaseAccountVal:
    return await async_get_account(conf.url, **req.dict(exclude_unset=True))


@router.post("/accounts", response_model=QueryAccountsResponse, tags=["account"])
async def accounts(
    req: QueryPaginatedHeightParams, conf: ProxySettings = Depends(settings)
) -> QueryAccountsResponse:
    return await async_get_accounts(conf.url, **req.dict(exclude_unset=True))


@router.post("/balance", response_model=QueryBalanceResponse, tags=["account"])
async def balance(
    req: QueryAddressHeight, conf: ProxySettings = Depends(settings)
) -> QueryBalanceResponse:
    return await async_get_balance(conf.url, **req.dict(exclude_unset=True))


@router.post("/accounttxs", response_model=QueryAccountTXsResponse, tags=["account"])
async def account_txs(
    req: QueryAccountTXs, conf: ProxySettings = Depends(settings)
) -> QueryAccountTXsResponse:
    return await async_get_account_transactions(
        conf.url, **req.dict(exclude_unset=True)
    )


@router.post("/block", response_model=QueryBlockResponse, tags=["block"])
async def block(
    req: QueryBlock, conf: ProxySettings = Depends(settings)
) -> QueryBlockResponse:
    return await async_get_block(conf.url, **req.dict(exclude_unset=True))


@router.post("/blocktxs", response_model=QueryBlockTXsResponse, tags=["block"])
async def block_txs(
    req: QueryBlockTXs, conf: ProxySettings = Depends(settings)
) -> QueryBlockTXsResponse:
    return await async_get_block_transactions(conf.url, **req.dict(exclude_unset=True))


@router.post("/height", response_model=QueryHeightResponse, tags=["network"])
async def height(conf: ProxySettings = Depends(settings)) -> QueryHeightResponse:
    return await async_get_height(conf.url)


@router.post("/state", response_model=StateResponse, tags=["network"])
async def state(
    req: QueryHeight, conf: ProxySettings = Depends(settings)
) -> StateResponse:
    return await async_get_state(conf.url, **req.dict(exclude_unset=True))


@router.post("/supply", response_model=QuerySupplyResponse, tags=["network"])
async def supply(
    req: QueryHeight, conf: ProxySettings = Depends(settings)
) -> QuerySupplyResponse:
    return await async_get_supply(conf.url, **req.dict(exclude_unset=True))


@router.post(
    "/supportedchains", response_model=QuerySupportedChainsResponse, tags=["network"]
)
async def supported_chains(
    req: QueryHeight,
    conf: ProxySettings = Depends(settings),
) -> QuerySupportedChainsResponse:
    return await async_get_supported_chains(conf.url, **req.dict(exclude_unset=True))


@router.post("/upgrade", response_model=Upgrade, tags=["network"])
async def upgrade(req: QueryHeight, conf: ProxySettings = Depends(settings)) -> Upgrade:
    return await async_get_upgrade(conf.url, **req.dict(exclude_unset=True))


@router.post("/param", response_model=ParamT, tags=["network"])
async def param(
    req: QueryHeightAndKey, conf: ProxySettings = Depends(settings)
) -> ParamT:
    h = req.height if req.height else 0
    return await async_get_param(conf.url, req.key, h)


@router.post("/allParams", response_model=AllParams, tags=["network"])
async def all_params(
    req: QueryHeight,
    conf: ProxySettings = Depends(settings),
) -> AllParams:
    return await async_get_all_params(conf.url, **req.dict(exclude_unset=True))


@router.post("/app", response_model=Application, tags=["service"])
async def single_app(
    req: QueryAddressHeight, conf: ProxySettings = Depends(settings)
) -> Application:
    return await async_get_app(conf.url, **req.dict(exclude_unset=True))


@router.post("/apps", response_model=QueryAppsResponse, tags=["service"])
async def apps(
    req: QueryHeightAndApplicationsOpts, conf: ProxySettings = Depends(settings)
) -> QueryAppsResponse:
    return await async_get_apps(conf.url, **req.dict(exclude_unset=True))


@router.post("/node", response_model=Node, tags=["service"])
async def node(
    req: QueryAddressHeight, conf: ProxySettings = Depends(settings)
) -> Node:
    return await async_get_node(conf.url, **req.dict(exclude_unset=True))


@router.post("/nodes", response_model=QueryNodesResponse, tags=["service"])
async def nodes(
    req: QueryHeightAndValidatorsOpts, conf: ProxySettings = Depends(settings)
) -> QueryNodesResponse:
    return await async_get_nodes(conf.url, **req.dict(exclude_unset=True))


@router.post("/signinginfo", response_model=QuerySigningInfoResponse, tags=["service"])
async def signing_info(
    req: QueryPaginatedHeightAndAddrParams, conf: ProxySettings = Depends(settings)
) -> QuerySigningInfoResponse:
    return await async_get_signing_info(conf.url, **req.dict(exclude_unset=True))


@router.post("/nodeclaim", response_model=QueryNodeClaimResponse, tags=["service"])
async def node_claim(
    req: QueryNodeReceipt, conf: ProxySettings = Depends(settings)
) -> QueryNodeClaimResponse:
    return await async_get_node_claim(conf.url, **req.dict(exclude_unset=True))


@router.post("/nodeclaims", response_model=QueryNodeClaimsResponse, tags=["service"])
async def node_claims(
    req: QueryPaginatedHeightAndAddrParams, conf: ProxySettings = Depends(settings)
) -> QueryNodeClaimsResponse:
    return await async_get_node_claims(conf.url, **req.dict(exclude_unset=True))


@router.post("/tx", response_model=Transaction, tags=["transaction"])
async def tx(req: QueryTX, conf: ProxySettings = Depends(settings)) -> Transaction:
    return await async_get_transaction_by_hash(conf.url, req.hash_, bool(req.prove))


@router.post("/unsupportedtx", response_model=UnconfirmedTransaction, tags=["mempool"])
async def unconfirmedtx(
    req: QueryUnconfirmedTX, conf: ProxySettings = Depends(settings)
) -> UnconfirmedTransaction:
    return await async_get_unconfirmed_transaction_by_hash(
        conf.url, **req.dict(exclude_unset=True)
    )


@router.post(
    "/unsupportedtxs", response_model=QueryUnconfirmedTXResponse, tags=["mempool"]
)
async def unconfirmedtxs(
    req: QueryUnconfirmedTXs, conf: ProxySettings = Depends(settings)
) -> QueryUnconfirmedTXsResponse:
    return await async_get_mempool_txs(conf.url, **req.dict(exclude_unset=True))
