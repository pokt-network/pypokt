"""
Any models declared here either:
    - address any discrepancies in the models generated from the rpc.yaml
    - add additional clarification about types that were treated as "any" types in the rpc.yaml
    - programatically express constraints and enumerations documented in the descriptions of the rpc.yaml

Any types not formally expressed in the rpc.yaml can be identified by models with a "Literal"
type field. Pocket core uses amino encoding, and so some returned models follow the given pattern:

{
  type: str
  value: Any (but really of type)
}

We can express these kinds of types via pydantic (and hence OpenAPI) via discriminator fields.
How this works, is any models following the above pattern will define models that represent each
of the possible types, with the type defined on the model as a literal that represents the expected
string. From there, we can define the generic model where the type of type still remains str, but
the type of value becomes a Union of all the types that type could be. By then specifying type as
the discriminator on the value field, this will allow the expected type to be conditionally parsed
based on str given as the type in the object to validate.

The two main instances of this are ParamValueT and MsgT acting
as the Union types for the protocol parameter values and the messages contained in a transaction's
stdTx field.

"""
from enum import Enum
import json
from typing import Any, List, Literal, Optional, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, conint, validator

import pokt.transactions.messages.proto.tx_signer_pb2 as proto


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
    per_page: conint(gt=0, le=10000) = Field(
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
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )
    prove: Optional[bool] = None
    order: SortOrder = Field(
        SortOrder.desc, description="The sort order, either 'asc' or 'desc'"
    )


class QueryAddressHeight(BaseModel):
    height: Optional[int] = None
    address: str


class QueryAccountTXs(BaseModel):
    class Config:
        use_enum_values = True

    address: str
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
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
    features: Optional[list[str]] = Field(None, alias="Features")


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


ParamValueT = Union[
    int, str, float, bool, List[str], UpgradeParamObject, FeeMultiplier, ACLKeysObject
]


class Param(BaseModel):
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


class AllParams(BaseModel):

    app_params: List[Annotated[Params, Field(discriminator="param_key")]]
    node_params: List[Annotated[Params, Field(discriminator="param_key")]]
    pocket_params: List[Annotated[Params, Field(discriminator="param_key")]]
    gov_params: List[Annotated[Params, Field(discriminator="param_key")]]
    auth_params: List[Annotated[Params, Field(discriminator="param_key")]]


class SingleParam(BaseModel):
    __root__: ParamT


class Consensus(BaseModel):
    block: Optional[int] = None
    app: Optional[int] = None


class PartSetHeader(BaseModel):
    class Config:
        allow_population_by_field_name = True

    total: Optional[int] = None
    hash_: Optional[str] = Field(None, alias="hash")


class BlockID(BaseModel):
    class Config:
        allow_population_by_field_name = True

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
    class Config:
        allow_population_by_field_name = True

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


class QueryHeightAndKey(BaseModel):
    height: Optional[int] = None
    key: str


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
    class Config:
        allow_population_by_field_name = True

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


class ProtobufTypes(int, Enum):
    DOUBLE = 1
    FLOAT = 2
    INT64 = 3
    UINT64 = 4
    INT32 = 5
    FIXED64 = 6
    FIXED32 = 7
    BOOL = 8
    STRING = 9
    GROUP = 10
    MESSAGE = 11
    BYTES = 12
    UINT32 = 13
    ENUM = 14
    SFIXED32 = 15
    SFIXED64 = 16
    SINT32 = 17
    SINT64 = 18


def encode_proto_type(value: Any, proto_type: Optional[ProtobufTypes] = None):
    if issubclass(value, ProtobufEncodable):
        return value
    elif proto_type in (
        None,
        ProtobufTypes.FIXED32,
        ProtobufTypes.FIXED64,
        ProtobufTypes.SFIXED32,
        ProtobufTypes.SFIXED64,
        ProtobufTypes.MESSAGE,
        ProtobufTypes.GROUP,
    ):
        return value
    elif proto_type in (ProtobufTypes.DOUBLE, ProtobufTypes.FLOAT):
        return float(value)
    elif proto_type in (
        ProtobufTypes.INT64,
        ProtobufTypes.UINT64,
        ProtobufTypes.INT32,
        ProtobufTypes.UINT32,
        ProtobufTypes.SINT32,
        ProtobufTypes.SINT64,
    ):
        return int(value)
    elif proto_type in (ProtobufTypes.BYTES,):
        return bytes(value, "utf-8")
    elif proto_type in (ProtobufTypes.BOOL,):
        return bool(value)
    elif proto_type in (ProtobufTypes.STRING, ProtobufTypes.ENUM):
        return str(value)


class ProtobufEncodable(BaseModel):

    __protobuf_model__: Any = None

    @classmethod
    def __proto_fields__(cls):
        proto_fields = {}
        for name, val in cls.__fields__.items():
            proto_name = val.field_info.extra.get("proto_name", name)
            proto_type = val.field_info.extra.get("proto_type")
            proto_fields[name] = (proto_name, proto_type)

        return proto_fields

    def protobuf_payload(self):
        if self.__protobuf_model__ is None:
            raise ValueError("The protobuf model was never defined.")
        msg = self.__protobuf_model__()
        proto_fields = self.__proto_fields__()
        for name, (proto_name, field_type) in proto_fields.items():
            value = getattr(self, name)
            try:
                setattr(msg, proto_name, encode_proto_type(value, field_type))
            except TypeError:
                ft = field_type.value if field_type is not None else "None"
                raise TypeError(
                    "Type error occurred when encoding {} to {} for field {}".format(
                        value, ft, proto_name
                    )
                )
        return msg.SerializeToString()


class MsgSendVal(ProtobufEncodable):
    __protobuf_model__ = proto.MsgSend

    from_address: Optional[str] = Field(
        None, proto_name="FromAddress", proto_type=ProtobufTypes.BYTES
    )
    to_address: Optional[str] = Field(
        None, proto_name="ToAddress", proto_type=ProtobufTypes.BYTES
    )
    amount: Optional[int] = Field(None, proto_type=ProtobufTypes.STRING)


class Range(BaseModel):
    lower: Optional[str] = None
    upper: Optional[str] = None


class HashRange(BaseModel):
    class Config:
        allow_population_by_field_name = True

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


class RelayProofVal(BaseModel):
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
    proof: Optional[RelayProofVal] = None


class ChallengeProofInvalidDataVal(BaseModel):
    majority_responses: Optional[list[RelayResponse]] = None
    minority_response: Optional[RelayResponse] = None
    reporters_address: Optional[str] = None


class Proof(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: str = Field(..., alias="type")
    value: Any


class RelayProof(Proof):
    type_: Literal["pocketcore/relay_proof"] = Field(alias="type")
    value: RelayProofVal


class ChallengeProofInvalidData(Proof):
    type_: Literal["pocketcore/challenge_proof"] = Field(alias="type")
    value: ChallengeProofInvalidDataVal


ProofT = Union[RelayProof, ChallengeProofInvalidData]


class EvidenceType(BaseModel):
    pass


class MsgProofVal(BaseModel):
    merkle_proofs: Optional[MerkleProof] = None
    leaf: Optional[ProofT] = Field(None, discriminator="type_")
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


MsgValT = Union[
    MsgSendVal,
    MsgValidatorStakeVal,
    MsgAppStakeVal,
    MsgValidatorUnjailVal,
    MsgAppUnjailVal,
    MsgBeginValidatorUnstakeVal,
    MsgBeginAppUnstakeVal,
]


class Msg(BaseModel):
    class Config:
        allow_population_by_field_name = True

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
    MsgAppStake,
    MsgAppUnjail,
    MsgBeginAppUnstake,
    MsgBeginValidatorUnstake,
    MsgChangeParam,
    MsgClaim,
    MsgDaoTransfer,
    MsgProof,
    MsgSend,
    MsgUpgrade,
    MsgValidatorStake,
    MsgValidatorUnjail,
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


class CoinDenom(str, Enum):
    upokt = "upokt"
    pokt = "pokt"


class Coin(ProtobufEncodable):
    class Confg:
        use_enum_values = True

    amount: Optional[str] = None
    denom: Optional[CoinDenom] = CoinDenom.upokt

    __protobuf_model__ = proto.Coin


class Signature(ProtobufEncodable):

    pub_key: Optional[str] = Field(
        None, proto_name="publicKey", proto_type=ProtobufTypes.BYTES
    )
    signature: Optional[str] = Field(
        None, proto_name="Signature", proto_type=ProtobufTypes.BYTES
    )

    __protobuf_model__ = proto.ProtoStdSignature


class StdTx(BaseModel):
    entropy: Optional[int] = None
    fee: Optional[List[Coin]] = None
    memo: Optional[str] = None
    msg: Optional[MsgT] = Field(None, discriminator="type_")
    signature: Optional[Signature] = None


class QueryTX(BaseModel):
    hash_: str = Field(..., alias="hash")
    prove: Optional[bool] = None


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


class QueryNodeClaimsResponse(BaseModel):
    result: Optional[list[MsgClaimVal]] = None
    page: int
    total_pages: int


class ReceiptType(str, Enum):
    realy = "relay"
    challenge = "challenge"


class QueryNodeReceipt(BaseModel):
    class Config:
        use_enum_values = True

    address: str
    blockchain: str
    app_pubkey: str
    session_block_height: int
    height: int
    receipt_type: ReceiptType


class QueryNodeClaimResponse(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type_: str = Field(..., alias="type")
    value: MsgClaimVal


class Application(BaseModel):
    address: Optional[str] = Field(
        None, description="The hex address of the application"
    )
    public_key: Optional[str] = Field(
        None, description="The hex public key of the application"
    )
    jailed: Optional[bool] = Field(
        False, description="Has the application been jailed from staked status"
    )
    status: Optional[int] = Field(None, description="Application status")
    chains: Optional[List[str]] = Field(None, description="Blockchains supported")
    staked_tokens: Optional[str] = Field(
        None, description="How many tokens has this node staked in uPOKT"
    )
    max_relays: Optional[int] = Field(
        None, description="Maximum number of relays supported"
    )
    unstaking_time: Optional[str] = Field(
        None,
        description="If unstaking, the minimum time for the validator to complete unstaking",
    )


class QueryAppsResponse(BaseModel):
    result: Optional[List[Application]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class ApplicationParams(BaseModel):
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


class ModuleAccountPermissions(str, Enum):
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


AccountT = Annotated[Union[BaseAccount, ModuleAccount], Field(discriminator="type_")]


class Account(BaseModel):
    __root__: Annotated[Union[BaseAccount, ModuleAccount], Field(discriminator="type_")]

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


class SigningInfo(BaseModel):
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


class QueryBalanceResponse(BaseModel):
    balance: Optional[int] = None


class QueryBlock(BaseModel):
    height: Optional[int] = None


class QueryHeight(BaseModel):
    height: Optional[int] = None


class QuerySupplyResponse(BaseModel):
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


class QuerySupportedChainsResponse(BaseModel):
    supported_chains: List[str] = Field(None, description="Supported blockchains")


class Node(BaseModel):
    address: Optional[str] = Field(None, description="The hex address of the validator")
    chains: Optional[List[str]] = Field(None, description="Blockchains supported")
    jailed: Optional[bool] = Field(
        False, description="Has the validator been jailed from staked status"
    )
    public_key: Optional[str] = Field(None, description="The validator public hex key")
    service_url: Optional[str] = Field(None, description="The validator service url")
    status: Optional[int] = Field(None, description="Validator status")
    tokens: Optional[str] = Field(
        None, description="How many tokens has this node staked in uPOKT"
    )
    unstaking_time: Optional[str] = Field(
        None,
        description="If unstaking, the minimum time for the validator to complete unstaking",
    )


class QueryNodesResponse(BaseModel):
    result: Optional[List[Node]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class QuerySigningInfoResponse(BaseModel):
    result: Optional[List[SigningInfo]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")


class QueryPaginatedHeightParams(BaseModel):
    height: Optional[int] = None
    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )


class QueryAccountsResponse(BaseModel):
    result: Optional[List[BaseAccountVal]] = None
    page: Optional[int] = Field(None, description="current page")
    total_pages: Optional[int] = Field(None, description="maximum amount of pages")
