from typing import Any, Literal, List, Optional, Union

from .base import Base, ProtobufBase, ProtobufTypes
from .core import (
    CoinDenom,
    HashRange,
    MerkleProof,
    ProofT,
    PublicKey,
    TXProof,
    TxResult,
    SessionHeader,
    Upgrade,
)
from .gov_params import ParamKeys, ParamValueT

import pokt.transactions.messages.proto.tx_signer_pb2 as proto

from pydantic import Field


class MsgSendVal(ProtobufBase):
    __protobuf_model__ = proto.MsgSend

    from_address: Optional[str] = Field(
        None, proto_name="FromAddress", proto_type=ProtobufTypes.BYTES
    )
    to_address: Optional[str] = Field(
        None, proto_name="ToAddress", proto_type=ProtobufTypes.BYTES
    )
    amount: Optional[int] = Field(None, proto_type=ProtobufTypes.STRING)


class MsgChangeParamVal(Base):
    address: Optional[str] = None
    param_key: Optional[ParamKeys] = None
    param_value: Optional[ParamValueT] = None
    # param: SingleParamT


class MsgDaoTransferVal(Base):
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[int] = None
    action: Optional[str] = None


class MsgUpgradeVal(Base):
    address: Optional[str] = None
    upgrade: Optional[Upgrade] = None


class MsgAppStakeVal(Base):
    pubkey: Optional[PublicKey] = None
    chains: Optional[list[str]] = None
    value: Optional[int] = None


class MsgBeginAppUnstakeVal(Base):
    application_address: Optional[str] = None


class MsgAppUnjailVal(Base):
    address: Optional[str] = None


class MsgValidatorStakeVal(Base):
    public_key: Optional[PublicKey] = None
    chains: Optional[list[str]] = None
    value: Optional[int] = None
    service_url: Optional[str] = None
    output_address: Optional[str] = None


class MsgBeginValidatorUnstakeVal(Base):
    validator_address: Optional[str] = None
    signer_address: Optional[str] = None


class MsgValidatorUnjailVal(Base):
    address: Optional[str] = None
    signer_address: Optional[str] = None


class MsgProofVal(Base):
    merkle_proofs: Optional[MerkleProof] = None
    leaf: Optional[ProofT] = Field(None, discriminator="type_")
    evidence_type: Optional[int] = None  # EvidenceType = None


class MsgClaimVal(Base):
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


class Msg(Base):
    type_: str = Field(..., alias="type")
    value: Any


class MsgClaim(Msg):
    type_: Literal["pocketcore/claim"] = Field(alias="type")
    value: MsgClaimVal


class MsgProof(Msg):
    type_: Literal["pocketcore/proof"] = Field(alias="type")
    value: MsgProofVal


class MsgValidatorStake(Msg):
    type_: Literal["pos/8.0MsgStake", "pos/MsgStake"] = Field(alias="type")
    value: MsgValidatorStakeVal


class MsgBeginValidatorUnstake(Msg):
    type_: Literal["pos/8.0MsgBeginUnstake", "pos/MsgBeginUnstake"] = Field(
        alias="type"
    )
    value: MsgBeginValidatorUnstakeVal


class MsgValidatorUnjail(Msg):
    type_: Literal["pos/MsgUnjail", "pos/8.0MsgUnjail"] = Field(alias="type")
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


class Coin(ProtobufBase):

    __protobuf_model__ = proto.Coin

    amount: Optional[str] = None
    denom: Optional[CoinDenom] = "upokt"


class Signature(ProtobufBase):

    __protobuf_model__ = proto.ProtoStdSignature

    pub_key: Optional[str] = Field(
        None, proto_name="publicKey", proto_type=ProtobufTypes.BYTES
    )
    signature: Optional[str] = Field(
        None, proto_name="Signature", proto_type=ProtobufTypes.BYTES
    )


class StdTx(Base):
    entropy: Optional[int] = None
    fee: Optional[List[Coin]] = None
    memo: Optional[str] = None
    msg: Optional[MsgT] = Field(None, discriminator="type_")
    signature: Optional[Signature] = None


class UnconfirmedTransaction(Base):
    hash_: Optional[str] = Field(
        None, alias="hash", description="Hash of the transaction"
    )
    message_type: Optional[str] = Field(
        None,
        description='The type of the transaction, can be "app_stake", "app_begin_unstake", "stake_validator", "begin_unstake_validator", "unjail_validator", "send", "upgrade", "change_param", "dao_tranfer", "claim", or "proof"',
    )
    stdTx: Optional[StdTx] = None


class Transaction(Base):
    hash_: Optional[str] = Field(
        None, alias="hash", description="Hash of the transaction"
    )
    height: Optional[int] = Field(None, description="Blockheight of the transaction")
    index: Optional[int] = None
    tx_result: Optional[TxResult] = None
    tx: Optional[str] = Field(None, description="Raw data of the transaction")
    proof: Optional[TXProof] = None
    stdTx: Optional[StdTx] = None
