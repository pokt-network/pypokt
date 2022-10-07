import json
from typing import Annotated, Any, Optional, List, Literal, Union

from pydantic import Field, validator

from .base import Base
from .core import ACLKey, FeeMultiplier, Upgrade


ParamKeys = Literal[
    "application/AppUnstakingTime",
    "application/ApplicationStakeMinimum",
    "application/BaseRelaysPerPOKT",
    "application/MaxApplications",
    "application/MaximumChains",
    "application/ParticipationRateOn",
    "application/StabilityAdjustment",
    "auth/FeeMultipliers",
    "auth/MaxMemoCharacters",
    "auth/TxSigLimit",
    "gov/acl",
    "gov/daoOwner",
    "gov/upgrade",
    "pocketcore/ClaimExpiration",
    "pocketcore/ClaimSubmissionWindow",
    "pocketcore/MinimumNumberOfProofs",
    "pocketcore/ReplayAttackBurnMultiplier",
    "pocketcore/SessionNodeCount",
    "pocketcore/SupportedBlockchains",
    "pos/BlocksPerSession",
    "pos/DAOAllocation",
    "pos/DowntimeJailDuration",
    "pos/MaxEvidenceAge",
    "pos/MaxJailedBlocks",
    "pos/MaxValidators",
    "pos/MaximumChains",
    "pos/MinSignedPerWindow",
    "pos/ProposerPercentage",
    "pos/RelaysToTokensMultiplier",
    "pos/ServicerStakeFloorMultiplier",
    "pos/ServicerStakeFloorMultiplierExponent",
    "pos/ServicerStakeWeightCeiling",
    "pos/ServicerStakeWeightMultiplier",
    "pos/SignedBlocksWindow",
    "pos/SlashFractionDoubleSign",
    "pos/SlashFractionDowntime",
    "pos/StakeDenom",
    "pos/StakeMinimum",
    "pos/UnstakingTime",
]


class ObjectParamValue(Base):

    type_: str = Field(..., alias="type")
    value: Any


class UpgradeParamObject(ObjectParamValue):
    value: Upgrade


class ACLKeysObject(ObjectParamValue):
    value: List[ACLKey]


ParamValueT = Union[
    int, str, float, bool, List[str], UpgradeParamObject, FeeMultiplier, ACLKeysObject
]


class Param(Base):
    param_key: str
    param_value: ParamValueT

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
        "application/AppUnstakingTime",
        "application/ApplicationStakeMinimum",
        "application/BaseRelaysPerPOKT",
        "application/MaxApplications",
        "application/MaximumChains",
        "application/StabilityAdjustment",
        "auth/MaxMemoCharacters",
        "auth/TxSigLimit",
        "pocketcore/ClaimExpiration",
        "pocketcore/ClaimSubmissionWindow",
        "pocketcore/MinimumNumberOfProofs",
        "pocketcore/ReplayAttackBurnMultiplier",
        "pocketcore/SessionNodeCount",
        "pos/BlocksPerSession",
        "pos/DAOAllocation",
        "pos/DowntimeJailDuration",
        "pos/MaxEvidenceAge",
        "pos/MaxJailedBlocks",
        "pos/MaxValidators",
        "pos/MaximumChains",
        "pos/ProposerPercentage",
        "pos/RelaysToTokensMultiplier",
        "pos/ServicerStakeFloorMultiplier",
        "pos/ServicerStakeWeightCeiling",
        "pos/SignedBlocksWindow",
        "pos/StakeMinimum",
        "pos/UnstakingTime",
    ]
    param_value: int


class StrParam(Param):
    param_key: Literal["gov/daoOwner", "pos/StakeDenom"]
    param_value: str


class FloatParam(Param):
    param_key: Literal[
        "pos/MinSignedPerWindow",
        "pos/ServicerStakeFloorMultiplierExponent",
        "pos/ServicerStakeWeightMultiplier",
        "pos/SlashFractionDoubleSign",
        "pos/SlashFractionDowntime",
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


Params = Union[
    IntParam,
    StrParam,
    FloatParam,
    BoolParam,
    SupportedBlockchainsParam,
    FeeMultiplierParam,
    ACLParam,
    UpgradeParam,
]

ParamT = Annotated[
    Params,
    Field(discriminator="param_key"),
]


class AllParams(Base):

    app_params: List[Annotated[Params, Field(discriminator="param_key")]]
    node_params: List[Annotated[Params, Field(discriminator="param_key")]]
    pocket_params: List[Annotated[Params, Field(discriminator="param_key")]]
    gov_params: List[Annotated[Params, Field(discriminator="param_key")]]
    auth_params: List[Annotated[Params, Field(discriminator="param_key")]]


class SingleParam(Base):
    __root__: ParamT
