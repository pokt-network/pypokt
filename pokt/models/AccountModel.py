from __future__ import annotations
import string
from typing import List, TYPE_CHECKING

from pydantic import BaseModel, Field, SecretStr, validator

from ..wallet import sign_with_priv_key

if TYPE_CHECKING:
    from .PPKModel import PPK
    from .TxModel import Tx


class UnlockedAccount(BaseModel):
    pubKey: str
    address: str
    privKey: SecretStr

    @validator("pubKey", "address")
    def values_must_be_hex_decodable(cls, v):
        if not all(c in string.hexdigits for c in v):
            raise ValueError("The value for salt cannot be hex decoded.")
        return v

    @validator("privKey")
    def secret_values_must_be_hex_decodable(cls, v):
        if not all(c in string.hexdigits for c in v.get_secret_value()):
            raise ValueError("The value for salt cannot be hex decoded.")
        return v

    def sign(self, payload: bytes) -> bytes:
        return sign_with_priv_key(self.privKey.get_secret_value(), payload)


class Account(BaseModel):

    address: str
    ppk: PPK
    txs: List[Tx]
