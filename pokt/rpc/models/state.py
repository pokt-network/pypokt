import enum
import json
from typing import Any, Literal, Optional, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, validator
from .validation import (
    ACLKey,
    Application,
    ApplicationParams,
    Coin,
    FeeMultiplier,
    SigningInfo,
    Upgrade,
)


class ApplicationState(BaseModel):
    applications: list[Application]
    exported: bool
    params: ApplicationParams


class PubKey(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: str = Field(..., alias="type")
    value: str


class BaseAccountVal(BaseModel):
    address: str
    coins: list[Coin]
    public_key: Optional[Union[str, PubKey]] = Field(None)


class ModuleAccountPermissions(str, enum.Enum):
    # https://github.com/pokt-network/pocket-core/blob/3c40b817a5358393b274728c6679b89720f65250/x/auth/alias.go#L21
    # https://github.com/pokt-network/pocket-core/blob/3c40b817a5358393b274728c6679b89720f65250/app/pocket.go#L198
    burning = "burning"
    minting = "minting"
    staking = "staking"


class ModuleAccountVal(BaseModel):
    base_account: Optional[BaseAccountVal] = Field(None, alias="BaseAccount")
    name: Optional[str]
    permissions: Optional[list[str]]  #


class BaseAccount(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: Literal["posmint/Account"] = Field(..., alias="type")
    value: BaseAccountVal

    @validator("value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class ModuleAccount(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: Literal["posmint/ModuleAccount"] = Field(..., alias="type")
    value: ModuleAccountVal

    @validator("value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


AccountT = Union[BaseAccount, ModuleAccount]


class Account(BaseModel):
    __root__: Annotated[AccountT, Field(discriminator="type_")]

    @property
    def type_(self):
        return self.__root__.type_

    @property
    def value(self):
        return self.__root__.value


class AuthParams(BaseModel):
    fee_multipliers: FeeMultiplier
    max_memo_characters: str
    tx_sig_limit: str


class SupplyItem(BaseModel):
    amount: str
    denom: str


class AuthState(BaseModel):
    accounts: list[Account]
    params: AuthParams
    supply: list[SupplyItem]


class GovParams(BaseModel):

    acl: list[ACLKey]
    dao_owner: str
    upgrade: Upgrade


class GovState(BaseModel):
    DAO_Tokens: str
    params: GovParams


class ClaimHeader(BaseModel):
    app_public_key: str
    chain: str
    session_height: int


class Claim(BaseModel):
    evidence_type: str
    expiration_height: int
    from_address: str


class PocketCoreParams(BaseModel):
    claim_expiration: str
    minimum_number_of_proofs: int
    proof_waiting_period: str
    replay_attack_burn_multiplier: str
    session_node_count: int
    supported_blockchains: list[str]


class PocketCoreState(BaseModel):
    claims: Optional[list[Claim]] = None
    params: PocketCoreParams


class PosParams(BaseModel):
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


class ValidatorPowers(BaseModel):
    address: str = Field(..., alias="Address")
    power: str = Field(..., alias="Power")


class Validator(BaseModel):
    address: str
    chains: list[str]
    jailed: bool
    output_address: str
    public_key: str
    service_url: str
    status: int
    tokens: str
    unstaking_time: str


class PosState(BaseModel):
    exported: bool
    missed_blocks: dict[str, Any]
    params: PosParams
    prevState_total_power: str
    prevState_validator_powers: list[ValidatorPowers]
    previous_proposer: str
    signing_infos: dict[str, SigningInfo]
    validators: list[Validator]


class AppState(BaseModel):
    application: ApplicationState
    auth: AuthState
    gov: GovState
    pocketcore: PocketCoreState
    pos: PosState


class ConsensusBlockParams(BaseModel):
    max_bytes: str
    max_gas: str
    time_iota_ms: str


class ConsensusEvidenceParams(BaseModel):
    max_age: str


class ConsensusValidatorParams(BaseModel):
    pub_key_types: list[str]


class ConsensusParams(BaseModel):
    block: ConsensusBlockParams
    evidence: ConsensusEvidenceParams
    validator: ConsensusValidatorParams


class StateResponse(BaseModel):
    app_hash: str
    app_state: AppState
    chain_id: str
    consensus_params: ConsensusParams
    genesis_time: str
