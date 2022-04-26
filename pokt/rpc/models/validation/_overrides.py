from enum import Enum
import json
from typing import Any, Callable, Dict, List, Literal, Optional, TypeVar, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, conint, validator, root_validator


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
    staking_status: Optional[StakingStatus] = None
    jailed_status: Optional[JailedStatus] = None
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
    staking_status: Optional[StakingStatus] = None
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
    old_upgrade_height: int = Field(1, alias="OldUpgradeHeight")


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
    txs: Optional[List[str]] = None


class BlockEvidence(BaseModel):
    evidence: Optional[str] = None

    @validator("evidence", pre=True)
    def wtf(cls, v):
        if not isinstance(v, str):
            return str(v)
        return v


class Block(BaseModel):
    header: Optional[BlockHeader] = None
    data: Optional[BlockData] = Field(None, description="Data hash of the block")
    evidence: Optional[BlockEvidence] = Field(None, description="Evidence hash")
    lastCommit: Optional[Commit] = None

    @validator("evidence", pre=True)
    def fix_evidence_issue(cls, v):
        if isinstance(v, str):
            return BlockEvidence(evidence=v)
        return v


class QueryBlockResponse(BaseModel):
    block: Optional[Block] = None
    block_meta: Optional[BlockMeta] = None


class QueryHeightResponse(BaseModel):
    height: int


class MsgChangeParamVal(BaseModel):
    address: Optional[str] = None
    param_key: Optional[str] = None
    param_value: Optional[Any] = None
    # param: SingleParamT


class MsgDaoTransferVal(BaseModel):
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[int] = None
    action: Optional[str] = None


class MsgUpgradeVal(BaseModel):
    address: Optional[str] = None
    upgrade: Optional[Upgrade] = None


class PublicKey(BaseModel):
    type_: str = Field(..., alias="type")
    value: str


class MsgAppStakeVal(BaseModel):
    pubkey: Optional[PublicKey] = None
    chains: Optional[list[str]] = None
    value: Optional[int] = None


class MsgBeginAppUnstakeVal(BaseModel):
    application_address: Optional[str] = None


class MsgAppUnjailVal(BaseModel):
    address: Optional[str] = None


class MsgValidatorStakeVal(BaseModel):
    public_key: Optional[PublicKey] = None
    chains: Optional[list[str]] = None
    value: Optional[int] = None
    service_url: Optional[str] = None
    output_address: Optional[str] = None


class MsgBeginValidatorUnstakeVal(BaseModel):
    validator_address: Optional[str] = None
    signer_address: Optional[str] = None


class MsgValidatorUnjailVal(BaseModel):
    address: Optional[str] = None
    signer_address: Optional[str] = None


class MsgSendVal(BaseModel):
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[int] = None


class Range(BaseModel):
    lower: Optional[str] = None
    upper: Optional[str] = None


class HashRange(BaseModel):
    merkleHash: Optional[str] = None
    range_: Optional[Range] = Field(None, alias="range")


class MerkleProof(BaseModel):
    index: Optional[int] = None
    hash_ranges: Optional[list[HashRange]] = None
    target_range: Optional[HashRange] = None


class AAT(BaseModel):
    version: Optional[str] = None
    app_pub_key: Optional[str] = Field(None, description="Application hex public key")
    client_pub_key: Optional[str] = Field(
        None, description="Application hex public key associated with a client"
    )
    signature: Optional[str] = Field(None, description="Application's signature in hex")


class RelayProof(BaseModel):
    request_hash: Optional[str] = Field(None, description="request hash identifier")
    entropy: Optional[int] = Field(None, description="Entropy value to add uniqueness")
    session_block_height: Optional[int] = Field(
        None, description="Height of the session"
    )
    servicer_pub_key: Optional[str] = Field(
        None, description="Servicer public hex public key"
    )
    blockchain: Optional[str] = Field(None, description="Blockchain hex string")
    aat: Optional[AAT] = None
    signature: Optional[str] = Field(None, description="client's signature in hex")


class RelayResponse(BaseModel):
    signature: Optional[str] = None
    payload: Optional[str] = None
    proof: Optional[RelayProof] = None


class ChallengeProofInvalidData(BaseModel):
    majority_responses: Optional[list[RelayResponse]] = None
    minority_response: Optional[RelayResponse] = None
    reporters_address: Optional[str] = None


Proof = Union[RelayProof, ChallengeProofInvalidData]


class EvidenceType(BaseModel):
    pass


class MsgProofVal(BaseModel):
    merkle_proofs: Optional[MerkleProof] = None
    leaf: Optional[Proof] = None
    evidence_type: Optional[int] = None  # EvidenceType = None


class SessionHeader(BaseModel):
    app_public_key: Optional[str] = Field(
        None, description="Application hex public key associated with a client"
    )
    chain: Optional[str] = Field(None, description="Network Identified in hex")
    session_height: Optional[int] = Field(None, description="Height of the session")


class MsgClaimVal(BaseModel):
    header: SessionHeader
    merkle_root: Optional[HashRange] = None
    total_proofs: Optional[int] = None
    from_address: Optional[str] = None
    evidence_type: Optional[int] = None  # EvidenceType = None
    expiration_height: Optional[int] = None


class Msg(BaseModel):
    type_: str = Field(..., alias="type")
    value: Any


class MsgClaim(Msg):
    type_: Literal["pocketcore/claim"] = Field(alias="type")
    value: MsgClaimVal


class MsgProof(Msg):
    type_: Literal["pocketcore/proof"] = Field(alias="type")
    value: MsgProofVal


class MsgValidatorStake(Msg):
    type_: Literal["pos/MsgStake"] = Field(alias="type")
    value: MsgValidatorStakeVal


class MsgBeginValidatorUnstake(Msg):
    type_: Literal["pos/MsgBeginUnstake"] = Field(alias="type")
    value: MsgBeginValidatorUnstakeVal


class MsgValidatorUnjail(Msg):
    type_: Literal["pos/MsgUnjail"] = Field(alias="type")
    value: MsgValidatorUnjailVal


class MsgSend(Msg):
    type_: Literal["pos/Send"] = Field(alias="type")
    value: MsgSendVal


class MsgAppStake(Msg):
    type_: Literal["apps/MsgAppStake"] = Field(alias="type")
    value: MsgAppStakeVal


class MsgBeginAppUnstake(Msg):
    type_: Literal["apps/MsgAppBeginUnstake"] = Field(alias="type")
    value: MsgBeginAppUnstakeVal


class MsgAppUnjail(Msg):
    type_: Literal["apps/MsgAppUnjail"] = Field(alias="type")
    value: MsgAppUnjailVal


class MsgDaoTransfer(Msg):
    type_: Literal["gov/msg_dao_transfer"] = Field(alias="type")
    value: MsgDaoTransferVal


class MsgChangeParam(Msg):
    type_: Literal["gov/msg_change_param"] = Field(alias="type")
    value: MsgChangeParamVal


class MsgUpgrade(Msg):
    type_: Literal["gov/msg_upgrade"] = Field(alias="type")
    value: MsgUpgradeVal


MsgT = Union[
    MsgClaim,
    MsgProof,
    MsgSend,
    MsgValidatorStake,
    MsgValidatorUnjail,
    MsgSend,
    MsgBeginValidatorUnstake,
    MsgUpgrade,
    MsgDaoTransfer,
    MsgChangeParam,
    MsgAppStake,
    MsgBeginAppUnstake,
    MsgAppUnjail,
]


class TxResult(BaseModel):
    code: Optional[int] = None
    data: Optional[str] = None
    log: Optional[str] = None
    info: Optional[str] = None
    events: Optional[List[str]] = None
    codespace: Optional[str] = None
    signer: Optional[str] = None
    recipient: Optional[str] = Field(
        None, description="The receiver of the transaction, will be null if no receiver"
    )
    message_type: Optional[str] = Field(
        None,
        description='The type of the transaction, can be "app_stake", "app_begin_unstake", "stake_validator", "begin_unstake_validator", "unjail_validator", "send", "upgrade", "change_param", "dao_tranfer", "claim", or "proof"',
    )


class SimpleProof(BaseModel):
    total: Optional[int] = None
    index: Optional[int] = None
    leaf_hash: Optional[str] = None
    aunts: Optional[List[str]] = None


class TXProof(BaseModel):
    root_hash: Optional[str] = None
    data: Optional[str] = None
    proof: Optional[SimpleProof] = None


class Coin(BaseModel):
    amount: Optional[str] = None
    denom: Optional[str] = None


class Signature(BaseModel):
    pub_key: Optional[str] = None
    signature: Optional[str] = None


class StdTx(BaseModel):
    entropy: Optional[int] = None
    fee: Optional[Coin] = None
    memo: Optional[str] = None
    msg: Optional[MsgT] = Field(None, discriminator="type_")
    signature: Optional[Signature] = None


class Transaction(BaseModel):
    hash_: Optional[str] = Field(
        None, alias="hash", description="Hash of the transaction"
    )
    height: Optional[int] = Field(None, description="Blockheight of the transaction")
    index: Optional[int] = None
    tx_result: Optional[TxResult] = None
    tx: Optional[str] = Field(None, description="Raw data of the transaction")
    proof: Optional[TXProof] = None
    stdTx: Optional[StdTx] = None


class QueryBlockTXsResponse(BaseModel):
    txs: Optional[List[Transaction]] = None
    total_txs: Optional[str] = None
    page_total: Optional[str] = None
    total_count: Optional[int] = None


class QueryAccountTXsResponse(BaseModel):
    txs: Optional[List[Transaction]] = None
    total_txs: Optional[str] = None
    page_total: Optional[str] = None
    total_count: Optional[str] = None


class QueryTXResponse(BaseModel):
    transaction: Optional[Transaction] = None
