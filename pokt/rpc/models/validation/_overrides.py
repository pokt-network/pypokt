from enum import Enum
import json
from typing import Any, Callable, Dict, List, Literal, Optional, TypeVar, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, conint, validator

from ...utils import get_full_param


class StakingStatus(int, Enum):
    unstaking = 1
    staked = 2


class JailedStatus(int, Enum):
    jailed = 1
    unjailed = 2


class ValidatorOpts(BaseModel):
    class Config:
        use_enum_values = True

    page: Optional[int] = None
    per_page: conint(gt=0, lt=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Union[StakingStatus, str] = ""
    jailed_status: Union[JailedStatus, str] = ""
    blockchain: Optional[str] = None


class QueryHeightAndValidatorsOpts(BaseModel):
    opts: ValidatorOpts
    height: int


class ApplicationOpts(BaseModel):
    class Config:
        use_enum_values = True

    page: Optional[int] = None
    per_page: conint(gt=0, lt=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Union[StakingStatus, str] = ""
    blockchain: Optional[str] = None


class QueryHeightAndApplicationsOpts(BaseModel):
    opts: ApplicationOpts
    height: int


class QueryPaginatedHeightAndAddrParams(BaseModel):
    height: int
    address: Optional[str] = None
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class QueryBlockTXs(BaseModel):
    class Config:
        use_enum_values = True

    height: int
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )
    prove: Optional[bool] = None
    order: SortOrder = Field(
        SortOrder.desc, description="The sort order, either 'asc' or 'desc'"
    )


class QueryAccountTXs(BaseModel):
    class Config:
        use_enum_values = True

    address: str
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )
    received: Optional[bool] = None
    prove: Optional[bool] = None
    order: SortOrder = Field(
        SortOrder.desc, description="The sort order, either 'asc' or 'desc'"
    )


class ObjectParamValue(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: str = Field(..., alias="type")
    value: Any


class Upgrade(BaseModel):
    class Config:
        allow_population_by_field_name = True

    height: int = Field(..., alias="Height")
    version: str = Field(..., alias="Version")
    old_upgrade_height: int = Field(..., alias="OldUpgradeHeight")


class UpgradeParamObject(ObjectParamValue):
    value: Upgrade


class ACLKey(BaseModel):
    acl_key: str
    address: str


class ACLKeysObject(ObjectParamValue):
    value: List[ACLKey]


class FeeMultiplier(BaseModel):
    fee_multiplier: Optional[int] = None
    default: int


class Param(BaseModel):
    param_key: str
    param_value: Any

    @property
    def name(self):
        if self.param_key is not None:
            return self.param_key.split("/")[1]
        return self.param_key

    @property
    def module(self):
        if self.param_key is not None:
            return self.param_key.split("/")[0].title()
        return self.param_key

    @property
    def value(self):
        return self.param_value

    def __str__(self):
        return "{}={}".format(self.name, self.value)


class IntParam(Param):
    param_key: Literal[
        "application/MaxApplications",
        "application/AppUnstakingTime",
        "application/MaximumChains",
        "application/StabilityAdjustment",
        "application/BaseRelaysPerPOKT",
        "application/ApplicationStakeMinimum",
        "pos/DAOAllocation",
        "pos/StakeMinimum",
        "pos/MaximumChains",
        "pos/RelaysToTokensMultiplier",
        "pos/MaxJailedBlocks",
        "pos/MaxValidators",
        "pos/UnstakingTime",
        "pos/DowntimeJailDuration",
        "pos/ProposerPercentage",
        "pos/BlocksPerSession",
        "pos/MaxEvidenceAge",
        "pos/SignedBlocksWindow",
        "pocketcore/SessionNodeCount",
        "pocketcore/ClaimSubmissionWindow",
        "pocketcore/ReplayAttackBurnMultiplier",
        "pocketcore/ClaimExpiration",
        "pocketcore/MinimumNumberOfProofs",
        "auth/MaxMemoCharacters",
        "auth/TxSigLimit",
    ]
    param_value: int


class StrParam(Param):
    param_key: Literal["pos/StakeDenom", "gov/daoOwner"]
    param_value: str


class FloatParam(Param):
    param_key: Literal[
        "pos/SlashFractionDoubleSign",
        "pos/SlashFractionDowntime",
        "pos/MinSignedPerWindow",
    ]
    param_value: float


class BoolParam(Param):
    param_key: Literal["application/ParticipationRateOn"]
    param_value: bool


class SupportedBlockchainsParam(Param):
    param_key: Literal["pocketcore/SupportedBlockchains"]
    param_value: List[str]

    @validator("param_value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class FeeMultiplierParam(Param):
    param_key: Literal["auth/FeeMultipliers"]
    param_value: FeeMultiplier

    @validator("param_value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class ACLParam(Param):
    param_key: Literal["gov/acl"]
    param_value: ACLKeysObject

    @validator("param_value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class UpgradeParam(Param):
    param_key: Literal["gov/upgrade"]
    param_value: UpgradeParamObject

    @validator("param_value", pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


SingleParamT = Union[
    IntParam,
    StrParam,
    FloatParam,
    BoolParam,
    SupportedBlockchainsParam,
    FeeMultiplierParam,
    ACLParam,
    UpgradeParam,
]

ParamValueT = Union[
    int, str, float, bool, List[str], Upgrade, FeeMultiplier, List[ACLKey], Upgrade
]


class AllParams(BaseModel):

    app_params: List[SingleParamT]
    node_params: List[SingleParamT]
    pocket_params: List[SingleParamT]
    gov_params: List[SingleParamT]
    auth_params: List[SingleParamT]

    def get_module_params(self, module_name: str) -> Optional[List[SingleParamT]]:
        check = module_name.lower()
        if check in ("app", "application"):
            return self.app_params
        elif check in ("pos", "node"):
            return self.node_params
        elif check in ("pocket", "core", "pocketcore", "pocket_core", "pocket-core"):
            return self.pocket_params
        elif check in ("gov", "governance", "dao"):
            return self.gov_params
        elif check in ("auth", "authentication"):
            return self.auth_params
        return None

    def get_param(self, param_name: str) -> ParamValueT:
        module, match = get_full_param(param_name)
        group = self.get_module_params(module)
        return [item for item in group if item.param_key == match][0].param_value

    def max_relays(self, app_stake: int) -> float:
        paricipation_rate_on = self.get_param("ParticipationRateOn")
        participation_rate = (
            self.get_param("ParticipationRate") if paricipation_rate_on else 1
        )
        stability_adjustment = self.get_param("StabilityAdjustment")
        base_relays = self.get_param("BaseRelaysPerPOKT")
        return (
            stability_adjustment + participation_rate * (base_relays / 100) * app_stake
        )

    def __getattribute__(self, name: str) -> Any:
        try:
            return self.get_param(name)
        except:
            return super().__getattribute__(name)


class SingleParam(BaseModel):
    __root__: Annotated[
        SingleParamT,
        Field(discriminator="param_key"),
    ]


class Consensus(BaseModel):
    block: Optional[int] = None
    app: Optional[int] = None


class PartSetHeader(BaseModel):
    total: Optional[int] = None
    hash_: Optional[str] = Field(None, alias="hash")


class BlockID(BaseModel):
    hash_: Optional[str] = Field(None, alias="hash")
    parts: Optional[PartSetHeader] = None


class BlockHeader(BaseModel):
    version: Optional[Consensus] = None
    chain_id: Optional[str] = None
    height: Optional[int] = None
    time: Optional[str] = None
    num_txs: Optional[int] = None
    total_txs: Optional[int] = None
    last_block_id: Optional[BlockID] = None
    last_commit_hash: Optional[str] = None
    data_hash: Optional[str] = None
    validators_hash: Optional[str] = None
    next_validators_hash: Optional[str] = None
    consensus_hash: Optional[str] = None
    app_hash: Optional[str] = None
    last_results_hash: Optional[str] = None
    evidence_hash: Optional[str] = None
    proposer_address: Optional[str] = None


class BlockMeta(BaseModel):
    block_id: Optional[BlockID] = None
    blockHeader: Optional[BlockHeader] = None


class CommitSignature(BaseModel):
    type_: Optional[str] = Field(None, alias="type")
    height: Optional[int] = None
    round_: Optional[int] = Field(None, alias="round")
    block_id: Optional[BlockID] = None
    timestamp: Optional[str] = None
    validator_address: Optional[str] = None
    validator_index: Optional[int] = None
    signature: Optional[str] = None


class Commit(BaseModel):
    block_id: Optional[BlockID] = None
    commit_signature: Optional[CommitSignature] = None


class BlockData(BaseModel):
    txs: List[str]


class BlockEvidence(BaseModel):
    evidence: Optional[str] = None


class Block(BaseModel):
    header: Optional[BlockHeader] = None
    data: Optional[BlockData] = Field(None, description="Data hash of the block")
    evidence: Optional[BlockEvidence] = Field(None, description="Evidence hash")
    lastCommit: Optional[Commit] = None


class QueryBlockResponse(BaseModel):
    block: Optional[Block] = None
    block_meta: Optional[BlockMeta] = None
