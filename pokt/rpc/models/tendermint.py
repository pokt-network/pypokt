from typing import Any, List
from pydantic import Field

from .base import Base

class JsonRpcBase(Base):
    jsonrpc: str
    id_: int = Field(..., alias="id")
    result: Any

class HeightVote(Base):
    round_: int = Field(..., alias="round")
    prevotes: List[str]
    precommits_bit_array: str

class RoundState(Base):
    height_round_step: str = Field(..., alias="height/round/step")
    start_time: str
    proposal_block_hash: str
    locked_block_hash: str
    valid_block_hash: str
    height_vote_set: List[HeightVote]

class ConsesnsusStateResult(Base):
    round_state: RoundState

class ConsesnsusStateResponse(JsonRpcBase):
    result: ConsesnsusStateResult

class PubKey(Base):
    type_: str =  Field(..., alias="type")
    value: str

class Validator(Base):
    address: str
    pub_key: PubKey
    voting_power: int
    proposer_priority: int

class ValidatorsResult(Base):
    block_height: int
    validators: List[Validator]

class ValidatorsResponse(JsonRpcBase):
    result: ValidatorsResult
