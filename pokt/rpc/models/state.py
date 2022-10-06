import json
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import Field, validator

from .base import Base
from .core import Application, ACLKey, FeeMultiplier, Upgrade
from .msgs import Coin

class ApplicationParams(Base):
    unstaking_time: Optional[str] = Field(None, description="duration of unstaking")
    max_applications: Optional[int] = Field(
        None, description="maximum number of applications"
    )
    app_stake_minimum: Optional[int] = Field(
        None, description="minimum amount needed to stake as an application"
    )
    base_relays_per_pokt: Optional[int] = Field(
        None, description="base relays per POKT coin staked"
    )
    stability_adjustment: Optional[int] = Field(
        None, description="the stability adjustment from the governance"
    )
    participation_rate_on: Optional[bool] = Field(
        None,
        description="the participation rate affects the amount minted based on staked ratio",
    )


class ApplicationState(Base):
    applications: List[Application]
    exported: bool
    params: ApplicationParams

class PubKey(Base):

    type_: str = Field(..., alias="type")
    value: str

class BaseAccountVal(Base):
    address: str
    coins: List[Coin]

class ModuleAccountVal(Base):
    base_account: Optional[BaseAccountVal] = Field(None, alias="BaseAccount")
    name: Optional[str]
    permissions: Optional[List[str]]  #

    public_key: Optional[Union[str, PubKey]] = Field(None)

class BaseAccount(Base):

    type_: Literal["posmint/Account"] = Field(..., alias="type")
    value: BaseAccountVal

    @validator("value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class ModuleAccount(Base):

    type_: Literal["posmint/ModuleAccount"] = Field(..., alias="type")
    value: ModuleAccountVal

    @validator("value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


AccountT = Annotated[Union[BaseAccount, ModuleAccount], Field(discriminator="type_")]


class Account(Base):
    __root__: Annotated[Union[BaseAccount, ModuleAccount], Field(discriminator="type_")]

    @property
    def type_(self):
        return self.__root__.type_

    @property
    def value(self):
        return self.__root__.value



class AuthParams(Base):
    fee_multipliers: FeeMultiplier
    max_memo_characters: str
    tx_sig_limit: str


class SupplyItem(Base):
    amount: str
    denom: str


class AuthState(Base):
    accounts: List[Account]
    params: AuthParams
    supply: List[SupplyItem]


class GovParams(Base):

    acl: List[ACLKey]
    dao_owner: str
    upgrade: Upgrade


class GovState(Base):
    DAO_Tokens: str
    params: GovParams


class ClaimHeader(Base):
    app_public_key: str
    chain: str
    session_height: int


class Claim(Base):
    evidence_type: str
    expiration_height: int
    from_address: str


class PocketCoreParams(Base):
    claim_expiration: str
    minimum_number_of_proofs: int
    proof_waiting_period: str
    replay_attack_burn_multiplier: str
    session_node_count: int
    supported_blockchains: List[str]


class PocketCoreState(Base):
    claims: Optional[List[Claim]] = None
    params: PocketCoreParams


class PosParams(Base):
    dao_allocation: str
    downtime_jail_duration: str
    max_evidence_age: str
    max_jailed_blocks: int
    max_validators: int
    min_signed_per_window: str
    proposer_allocation: str
    relays_to_tokens_multiplier: str
    session_block_frequency: str
    signed_blocks_window: str
    slash_fraction_double_sign: str
    slash_fraction_downtime: str
    stake_denom: str
    stake_minimum: int
    unstaking_time: int


class ValidatorPowers(Base):
    address: str = Field(..., alias="Address")
    power: str = Field(..., alias="Power")


class Validator(Base):
    address: str
    chains: List[str]
    jailed: bool
    output_address: str
    public_key: str
    service_url: str
    status: int
    tokens: str
    unstaking_time: str


class SigningInfo(Base):
    address: Optional[str] = Field(
        None, description="operator address of the signing info"
    )
    index_offset: Optional[int] = Field(
        None,
        description="The counter for the signing info (reset to 0 after SignedBlocksWindow elapses)",
    )
    jailed_blocks_counter: Optional[int] = Field(
        None, description="The number of blocks jailed (reset to 0 after unjail)"
    )
    jailed_until: Optional[str] = Field(
        None, description="The time the node can be unjailed"
    )
    missed_blocks_counter: Optional[int] = Field(
        None,
        description="The number of blocks missed within SignedBlocksWindow (can be decremented after the fact if new signature information/evidence is found)",
    )
    start_height: Optional[int] = Field(
        None,
        description="The origin height of the node (when it first joined the network)",
    )


class PosState(Base):
    exported: bool
    missed_blocks: Dict[str, Any]
    params: PosParams
    prevState_total_power: str
    prevState_validator_powers: List[ValidatorPowers]
    previous_proposer: str
    signing_infos: Dict[str, SigningInfo]
    validators: List[Validator]


class AppState(Base):
    application: ApplicationState
    auth: AuthState
    gov: GovState
    pocketcore: PocketCoreState
    pos: PosState

class ConsensusBlockParams(Base):
    max_bytes: str
    max_gas: str
    time_iota_ms: str


class ConsensusEvidenceParams(Base):
    max_age: str


class ConsensusValidatorParams(Base):
    pub_key_types: list[str]


class ConsensusParams(Base):
    block: ConsensusBlockParams
    evidence: ConsensusEvidenceParams
    validator: ConsensusValidatorParams
