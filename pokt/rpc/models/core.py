from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import Field, conint, validator

from .base import Base, ProtobufBase, ProtobufTypes
import pokt.transactions.messages.proto.tx_signer_pb2 as proto

TxResultMessageTypes = Literal[
    "app_stake",
    "app_begin_unstake",
    "stake_validator",
    "begin_unstake_validator",
    "unjail_validator",
    "send",
    "change_param",
    "dao_transfer",
    "claim",
    "proof",
]

SortOrder = Literal["asc", "desc"]
ReceiptType = Literal["challenge", "relay"]
CoinDenom = Literal["pokt", "upokt"]

# https://github.com/pokt-network/pocket-core/blob/3c40b817a5358393b274728c6679b89720f65250/x/auth/alias.go#L21
# https://github.com/pokt-network/pocket-core/blob/3c40b817a5358393b274728c6679b89720f65250/app/pocket.go#L198
ModuleAccountPermissions = Literal["burning", "minting", "staking"]


class StakingStatus(int, Enum):
    unstaking = 1
    staked = 2


class JailedStatus(int, Enum):
    jailed = 1
    unjailed = 2


# class SortOrder(str, Enum):
# asc = "asc"
# desc = "desc"

# class CoinDenom(str, Enum):
#
#    upokt = "upokt"
#    pokt = "pokt"


class Upgrade(Base):

    height: int = Field(..., alias="Height")
    version: str = Field(..., alias="Version")
    old_upgrade_height: int = Field(1, alias="OldUpgradeHeight")
    features: Optional[list[str]] = Field(None, alias="Features")


class ACLKey(Base):
    acl_key: str
    address: str


class FeeMultiplier(Base):
    fee_multiplier: Optional[int] = None
    default: int


class ValidatorOpts(Base):

    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Optional[StakingStatus] = Field(
        None, description="1 for unstaking, 2 for staked"
    )
    jailed_status: Optional[JailedStatus] = Field(
        None, description="1 for jailed; 2 for not jailed"
    )
    blockchain: Optional[str] = None


class ApplicationOpts(Base):

    page: Optional[int] = None
    per_page: conint(gt=0, le=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Optional[StakingStatus] = None
    blockchain: Optional[str] = None


class Consensus(Base):
    block: Optional[int] = None
    app: Optional[int] = None


class PartSetHeader(Base):

    total: Optional[int] = None
    hash_: Optional[str] = Field(None, alias="hash")


class BlockID(Base):

    hash_: Optional[str] = Field(None, alias="hash")
    parts: Optional[PartSetHeader] = None


class BlockHeader(Base):
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


class BlockMeta(Base):
    block_id: Optional[BlockID] = None
    blockHeader: Optional[BlockHeader] = None


class CommitSignature(Base):

    type_: Optional[str] = Field(None, alias="type")
    height: Optional[int] = None
    round_: Optional[int] = Field(None, alias="round")
    block_id: Optional[BlockID] = None
    timestamp: Optional[str] = None
    validator_address: Optional[str] = None
    validator_index: Optional[int] = None
    signature: Optional[str] = None


class Commit(Base):
    block_id: Optional[BlockID] = None
    commit_signature: Optional[CommitSignature] = None


class BlockData(Base):
    txs: Optional[List[str]] = None


class BlockEvidence(Base):
    evidence: Optional[str] = None

    @validator("evidence", pre=True)
    def wtf(cls, v):
        if not isinstance(v, str):
            return str(v)
        return v


class Block(Base):
    header: Optional[BlockHeader] = None
    data: Optional[BlockData] = Field(None, description="Data hash of the block")
    evidence: Optional[BlockEvidence] = Field(None, description="Evidence hash")
    lastCommit: Optional[Commit] = None

    @validator("evidence", pre=True)
    def fix_evidence_issue(cls, v):
        if isinstance(v, str):
            return BlockEvidence(evidence=v)
        return v


class PublicKey(Base):
    type_: str = Field(..., alias="type")
    value: str


class Range(Base):
    lower: Optional[str] = None
    upper: Optional[str] = None


class HashRange(Base):

    merkleHash: Optional[str] = None
    range_: Optional[Range] = Field(None, alias="range")


class MerkleProof(Base):
    index: Optional[int] = None
    hash_ranges: Optional[List[HashRange]] = None
    target_range: Optional[HashRange] = None


class AAT(Base):
    version: Optional[str] = None
    app_pub_key: Optional[str] = Field(None, description="Application hex public key")
    client_pub_key: Optional[str] = Field(
        None, description="Application hex public key associated with a client"
    )
    signature: Optional[str] = Field(None, description="Application's signature in hex")


class RelayProofVal(Base):
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


class RelayResponse(Base):
    signature: Optional[str] = None
    payload: Optional[str] = None
    proof: Optional[RelayProofVal] = None


class ChallengeProofInvalidDataVal(Base):
    majority_responses: Optional[list[RelayResponse]] = None
    minority_response: Optional[RelayResponse] = None
    reporters_address: Optional[str] = None


class Proof(Base):

    type_: str = Field(..., alias="type")
    value: Any


class RelayProof(Proof):
    type_: Literal["pocketcore/relay_proof"] = Field(alias="type")
    value: RelayProofVal


class ChallengeProofInvalidData(Proof):
    type_: Literal["pocketcore/challenge_proof"] = Field(alias="type")
    value: ChallengeProofInvalidDataVal


ProofT = Union[RelayProof, ChallengeProofInvalidData]


class EvidenceType(Base):
    pass


class SessionHeader(Base):
    app_public_key: Optional[str] = Field(
        None, description="Application hex public key associated with a client"
    )
    chain: Optional[str] = Field(None, description="Network Identified in hex")
    session_height: Optional[int] = Field(None, description="Height of the session")


class TxResult(Base):
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


class SimpleProof(Base):
    total: Optional[int] = None
    index: Optional[int] = None
    leaf_hash: Optional[str] = None
    aunts: Optional[List[str]] = None


class TXProof(Base):
    root_hash: Optional[str] = None
    data: Optional[str] = None
    proof: Optional[SimpleProof] = None


class Application(Base):
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


class Node(Base):
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
