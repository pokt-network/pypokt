from enum import Enum
import json
from typing import Any, Callable, Dict, List, Literal, Optional, TypeVar, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, conint, validator


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

param_keys = [
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
    "pos/StakeDenom",
    "gov/daoOwner",
    "pos/SlashFractionDoubleSign",
    "pos/SlashFractionDowntime",
    "application/ParticipationRateOn",
    "pos/MinSignedPerWindow",
    "pocketcore/SupportedBlockchains",
    "auth/FeeMultipliers",
    "gov/acl",
    "gov/upgrade",
]

key_map = {}

for key in param_keys:
    module, name = key.split("/")
    key_map[name] = module


class AllParams(BaseModel):

    app_params: Optional[List[SingleParamT]] = None
    node_params: Optional[List[SingleParamT]] = None
    pocket_params: Optional[List[SingleParamT]] = None
    gov_params: Optional[List[SingleParamT]] = None
    auth_params: Optional[List[SingleParamT]] = None

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
        if param_name == "MaximumChains":
            raise ValueError(
                "There are 2 available MaximumChains parameters. Either specify AppMaximumChains or NodeMaximumChains"
            )
        if param_name == "AppMaximumChains":
            module = "application"
            param_name = "MaximumChains"
        elif param_name == "NodeMaximumChains":
            module = "pos"
            param_name = "MaximumChains"
        else:
            module = key_map.get(param_name)
        if module == "pos":
            group = self.node_params
        elif module == "application":
            group = self.app_params
        elif module == "gov":
            group = self.gov_params
        elif module == "pocketcore":
            group = self.pocket_params
        elif module == "auth":
            group = self.auth_params
        else:
            raise ValueError("Unsupported Parameter: {}".format(param_name))
        match = "{}/{}".format(module, param_name)
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
