from typing import List

from pydantic import BaseModel, Field, Json


class TxResult(BaseModel):
    code: int
    data: str
    log: str
    events: List[str]
    codespace: str
    signer: str
    recipient: str
    message_type: str


class SimpleProof(BaseModel):
    total: int
    index: int
    leaf_hash: str
    aunts: List[str]


class TxProof(BaseModel):
    root_hash: str
    data: str
    proof: SimpleProof


class Coin(BaseModel):
    amount: str
    denom: str


class Signature(BaseModel):
    pub_key: str
    signature: str


class StdTx(BaseModel):
    entropy: int
    fee: Coin
    memo: str
    msg: Json
    signautre: Signature


class Tx(BaseModel):

    hash_: str = Field(..., alias="hash")
    height: int
    index: int
    tx: str
    tx_result: TxResult
    proof: TxProof
    stdTx: StdTx
