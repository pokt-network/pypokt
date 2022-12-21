from typing import Any, List, Optional

from pydantic import Field

from .base import Base
from .core import ABCIMessageLog, Application, Block, BlockMeta, Node, Session
from .msgs import Transaction, MsgClaimVal, UnconfirmedTransaction
from .state import AppState, BaseAccountVal, ConsensusParams, SigningInfo


class QueryBlockResponse(Base):
    block: Optional[Block] = None
    block_meta: Optional[BlockMeta] = None


class QueryHeightResponse(Base):
    height: int


class QueryBlockTXsResponse(Base):
    txs: Optional[List[Transaction]] = None
    total_txs: Optional[str] = None
    page_total: Optional[str] = None
    total_count: Optional[int] = None


class QueryAccountTXsResponse(Base):
    txs: Optional[List[Transaction]] = None
    total_txs: Optional[str] = None
    page_total: Optional[str] = None
    total_count: Optional[str] = None


class QueryUnconfirmedTXResponse(Base):
    transaction: Optional[UnconfirmedTransaction] = None


class QueryUnconfirmedTXsResponse(Base):
    txs: Optional[List[UnconfirmedTransaction]] = None
    page_count: int
    total_txs: int


class QueryTXResponse(Base):
    transaction: Optional[Transaction] = None


class QueryNodeClaimsResponse(Base):
    result: Optional[List[MsgClaimVal]] = None
    page: int
    total_pages: int


class QueryNodeClaimResponse(Base):

    type_: str = Field(..., alias="type")
    value: MsgClaimVal


class QueryAppsResponse(Base):
    result: Optional[List[Application]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class StateResponse(Base):
    app_hash: str
    app_state: AppState
    chain_id: str
    consensus_params: ConsensusParams
    genesis_time: str


class QueryBalanceResponse(Base):
    balance: Optional[int] = None


class QuerySupplyResponse(Base):
    node_staked: Optional[int] = Field(
        None, description="Amount staked by the node in uPOKT"
    )
    app_staked: Optional[int] = Field(
        None, description="Amount staked by the app in uPOKT"
    )
    dao: Optional[int] = Field(None, description="DAO amount in uPOKT")
    total_staked: Optional[int] = Field(
        None, description="Total amount staked in uPOKT"
    )
    total_unstaked: Optional[int] = Field(
        None, description="Total amount unstaked in uPOKT"
    )
    total: Optional[int] = Field(None, description="Total amount in uPOKT")


class QuerySupportedChainsResponse(Base):
    supported_chains: List[str] = Field(None, description="Supported blockchains")


class QueryNodesResponse(Base):
    result: Optional[List[Node]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class QuerySigningInfoResponse(Base):
    result: Optional[List[SigningInfo]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class QueryAccountsResponse(Base):
    result: Optional[List[BaseAccountVal]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class QueryDispatchResponse(Base):
    session: Session
    block_height: int


class QueryRelayResponse(Base):
    signature: str = Field(..., description="Signature from the node in hex")
    payload: str = Field(..., description="String response to the relay")


class QueryErrorRelayResponse(Base):
    error: str = Field(..., description="Encoded as an Amino JSON Error String")
    dispatch: QueryDispatchResponse


class QueryRawTXResponse(Base):
    height: int = Field(..., description="Blockheight of the transaction")
    txhash: str = Field(..., description="hash of the transaction")
    codespace: str
    code: int = Field(..., description="Result code, 0 is OK; else error.")
    data: str = Field(..., description="Raw transaction data")
    raw_log: str = Field(..., description="Raw transaction log")
    logs: list[ABCIMessageLog] = Field(..., description="ABCI Tendermint Logs")
    info: str
    gas_wanted: int
    gas_used: int
    Tx: dict[str, Any]
    timestamp: str = Field(..., description="Timestamp of the transaction")


class QueryChallengeResponse(Base):
    response: str
