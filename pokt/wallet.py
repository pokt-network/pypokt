from __future__ import annotations
import base64
from enum import Enum
import hashlib
from typing import Optional, Union, TYPE_CHECKING

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey
from nacl.exceptions import BadSignatureError

if TYPE_CHECKING:
    from .models import PPK, UnlockedAccount


class ImplementedKDFs(str, Enum):
    scrypt = "scrypt"


class _ScryptConfig:
    N: int = 32768
    r: int = 8
    p: int = 1
    maxmem: int = 2147483647
    keylen: int = 32


def _address_from_privkey(privKey: bytes) -> str:
    return address_from_pubkey(privKey[64:])


def address_from_pubkey(pubKey: Union[str, bytes]) -> str:
    pubKey = pubKey.decode("utf-8") if isinstance(pubKey, bytes) else pubKey
    h = hashlib.sha256()
    h.update(bytes.fromhex(pubKey))
    return bytes.fromhex(h.hexdigest())[:20].hex()


def create_new_ppk(
    password: str, hint: Optional[str] = None, secparam: int = 12
) -> PPK:
    priv_key = PrivateKey.generate()
    priv_key_str = bytes(priv_key).hex() + bytes(priv_key.public_key).hex()
    return ppk_from_priv_key(priv_key_str, password, hint, secparam)


def ppk_from_priv_key(
    priv_key: str, password: str, hint: Optional[str] = None, secparam: int = 12
) -> PPK:
    from .models.PPKModel import PPK

    salt_bytes = get_random_bytes(16)
    scrypt_hash_bytes = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt_bytes,
        n=_ScryptConfig.N,
        r=_ScryptConfig.r,
        p=_ScryptConfig.p,
        maxmem=_ScryptConfig.maxmem,
        dklen=_ScryptConfig.keylen,
    )
    nonce = scrypt_hash_bytes[:secparam]
    cipher = AES.new(scrypt_hash_bytes, AES.MODE_GCM, nonce)
    ciphertext_bytes, tag = cipher.encrypt_and_digest(priv_key.encode("utf-8"))
    hint = "POKTWalletQt: {}".format(hint) if hint is not None else "POKTWalletQt"
    return PPK(
        kdf=ImplementedKDFs.scrypt,
        salt=salt_bytes.hex(),
        secparam=secparam,
        hint=hint,
        ciphertext=base64.b64encode(ciphertext_bytes + tag).decode("utf-8"),
    )


def unlock_ppk(ppk: PPK, password: str) -> UnlockedAccount:
    from .models.AccountModel import UnlockedAccount

    scrypt_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=ppk.salt_bytes,
        n=_ScryptConfig.N,
        r=_ScryptConfig.r,
        p=_ScryptConfig.p,
        maxmem=_ScryptConfig.maxmem,
        dklen=_ScryptConfig.keylen,
    )

    nonce = scrypt_hash[: ppk.secparam]
    data = ppk.ciphertext_bytes[:-16]
    cipher = AES.new(scrypt_hash, AES.MODE_GCM, nonce)
    priv_bytes = cipher.decrypt(data)

    address = _address_from_privkey(priv_bytes)
    pub_bytes = priv_bytes[64:]
    return UnlockedAccount(
        pubKey=pub_bytes.decode("utf-8"),
        address=address,
        privKey=priv_bytes.decode("utf-8"),
    )


def verify_signature(
    signer_pub_key: str, signed_msg: bytes, signature: Optional[bytes] = None
) -> bool:
    verify_key = VerifyKey(bytes.fromhex(signer_pub_key))
    try:
        verify_key.verify(signed_msg, signature)
    except BadSignatureError:
        return False
    return True


def sign_with_priv_key(priv_key: str, payload: bytes) -> bytes:
    sig_key = SigningKey(bytes.fromhex(priv_key[:64]))
    signed = sig_key.sign(payload)
    return signed.signature + signed.message
