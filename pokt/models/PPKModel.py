from __future__ import annotations
import base64
import binascii
import json
import string
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, validator

from ..wallet import unlock_ppk, ImplementedKDFs

if TYPE_CHECKING:
    from .AccountModel import UnlockedAccount


class PPK(BaseModel):
    class Config:
        use_enum_values = True

    kdf: ImplementedKDFs = Field(
        ..., description="Currently only scrypt is implemented"
    )
    salt: str = Field(..., description="Cannot be empty, and can be decoded from hex")
    secparam: int = Field(
        ...,
        description="The cost, and the value that determines how many bytes are used to determine the nonce.",
    )
    hint: Optional[str] = Field(
        "", description="An optional hint for the password used to encrypt"
    )
    ciphertext: str = Field(..., description="Can be decoded from base64.")

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, "r") as kf:
            data = json.load(kf)
        return cls(**data)

    @property
    def salt_bytes(self) -> bytes:
        return bytes.fromhex(self.salt)

    @property
    def ciphertext_bytes(self) -> bytes:
        return base64.b64decode(self.ciphertext)

    @validator("salt")
    def salt_cannot_be_empty(cls, v):
        if not v:
            raise ValueError("The value for salt cannot be empty.")
        return v

    @validator("salt")
    def salt_must_be_hex_decodable(cls, v):
        if not all(c in string.hexdigits for c in v):
            raise ValueError("The value for salt cannot be hex decoded.")
        return v

    @validator("ciphertext")
    def ciphertext_must_be_base64_decoable(cls, v):
        try:
            base64.b64decode(v, validate=True)
        except binascii.Error:
            raise ValueError("The value for ciphertext cannot be base64 decoded.")
        return v

    def unlock(self, password: str) -> UnlockedAccount:
        return unlock_ppk(self, password)
