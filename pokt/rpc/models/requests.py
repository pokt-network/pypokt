from typing import Optional

from pydantic import Field, conint

from .base import Base
from .core import (
    ApplicationOpts,
    ValidatorOpts,
    SortOrder,
    ReceiptType,
    RelayMetadata,
    RelayPayload,
    RelayProofVal,
)
from .gov_params import ParamKeys
from .responses import QueryRelayResponse


class QueryHeightAndValidatorsOpts(Base):
    opts: ValidatorOpts
    height: int


class QueryHeightAndApplicationsOpts(Base):
    opts: ApplicationOpts
    height: int


class QueryPaginatedHeightAndAddrParams(Base):
    height: int
    address: Optional[str] = None
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 10000"
    )


class QueryUnconfirmedTX(Base):
    hash_: str = Field(..., alias="hash")


class QueryUnconfirmedTXs(Base):
    page: int
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 10000"
    )


class QueryBlockTXs(Base):

    height: int
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 10000"
    )
    prove: Optional[bool] = None
    order: SortOrder = Field(
        "desc", description="The sort order, either 'asc' or 'desc'"
    )


class QueryAddressHeight(Base):
    height: Optional[int] = None
    address: str


class QueryAccountTXs(Base):

    address: str
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 10000"
    )
    received: Optional[bool] = None
    prove: Optional[bool] = None
    order: SortOrder = Field(
        "desc", description="The sort order, either 'asc' or 'desc'"
    )


class QueryHeightAndKey(Base):
    height: Optional[int] = None
    key: ParamKeys


class QueryTX(Base):
    hash_: str = Field(..., alias="hash")
    prove: Optional[bool] = None


class QueryNodeReceipt(Base):

    address: str
    blockchain: str
    app_pubkey: str
    session_block_height: int
    height: int
    receipt_type: ReceiptType


class QueryBlock(Base):
    height: Optional[int] = None


class QueryHeight(Base):
    height: Optional[int] = None


class QueryPaginatedHeightParams(Base):
    height: Optional[int] = None
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 10000"
    )


class QueryRelayRequest(Base):
    payload: RelayPayload
    meta: RelayMetadata
    proof: RelayProofVal


class QuerySimRequest(Base):
    payload: RelayPayload
    relay_network_id: str
    meta: Optional[RelayMetadata] = None
    proof: Optional[RelayProofVal] = None


class QueryRawTXRequest(Base):
    address: str
    raw_hex_bytes: str


class QueryChallengeRequest(Base):
    majority_responses: list[QueryRelayResponse]
    minority_response: QueryRelayResponse
    address: str = Field(..., description="reporter address")
