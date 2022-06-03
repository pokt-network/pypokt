"""
Handles the functionality for handling keybase operations.
"""
from __future__ import annotations
import base64
import hashlib
from typing import Optional, Union, TYPE_CHECKING

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey
from nacl.exceptions import BadSignatureError

if TYPE_CHECKING:
    from .models import PPK


class _ScryptConfig:
    N: int = 32768
    r: int = 8
    p: int = 1
    maxmem: int = 2147483647
    keylen: int = 32


def address_from_pubkey(pubKey: Union[str, bytes]) -> str:
    """
    Get the address given a public key.

    Parameters
    ----------
    pubKey: str, bytes

    Returns
    -------
    address : str
    """
    pubKey = pubKey.decode("utf-8") if isinstance(pubKey, bytes) else pubKey
    h = hashlib.sha256()
    h.update(bytes.fromhex(pubKey))
    return bytes.fromhex(h.hexdigest())[:20].hex()


def create_new_ppk(
    password: str, hint: Optional[str] = None, secparam: int = 12
) -> PPK:
    """
    Create a new PPK given a password. A PPK is the private and
    public key pair, encrypted using the Armored JSON to allow
    for storing the private key and public key pair in a file
    protected by a password.

    Parameters
    ----------
    password
        The password that will be used to unlock the ppk.
    hint
        Any desired hint to include in the PPK
    secparam
        A value to tune the increase in security. Defaults to 12.

    Returns
    -------
    ppk: pokt.models.PPK
    """
    priv_key = PrivateKey.generate()
    priv_key_str = bytes(priv_key).hex() + bytes(priv_key.public_key).hex()
    return ppk_from_priv_key(priv_key_str, password, hint, secparam)


def ppk_from_priv_key(
    priv_key: str, password: str, hint: Optional[str] = None, secparam: int = 12
) -> PPK:
    """
    Create a PPK given an existing private key,

    Parameters
    ----------
    priv_key
        The private key to generate a PPK for.
    password
        The password that will be used to unlock the ppk.
    hint
        Any desired hint to include in the PPK
    secparam
        A value to tune the increase in security. Defaults to 12.

    Returns
    -------
    ppk: pokt.models.PPK
    """
    from .models import PPK, ImplementedKDFs

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
        pub_key=priv_key[64:],
    )


def priv_key_from_ppk(ppk: PPK, password: str) -> str:
    """
    Get a private key give a ppk and password

    Parameters
    ----------
    ppk
    password
        The password that was used to initially create the ppk

    Returns
    -------
    str
        The decoded private key.
    """
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
    return cipher.decrypt(data).decode("utf-8")


def verify_signature(
    signer_pub_key: str, signed_msg: bytes, signature: Optional[bytes] = None
) -> bool:
    """
    Verify whether the message was signed by the given public key.

    Parameters
    ----------
    signer_pub_key: hex str
        The public key to verify as the signer.
    signed_msg
        The signed message. Either the signature concatenated
        with the original message, or just the raw bytes of the message.
        If only the raw message bytes are passed, the signature
        must be passed through the optional signature keyword argument.
    signature:
        The signature, only required if not concatenated in the message
        signature (the expected behavior.

    Returns
    -------
    True if the signature matched the signing key,
    """
    verify_key = VerifyKey(bytes.fromhex(signer_pub_key))
    try:
        verify_key.verify(signed_msg, signature)
    except BadSignatureError:
        return False
    return True


def sign_with_priv_key(priv_key: str, payload: bytes) -> bytes:
    """
    Sign a given message with a private key.

    Parameters
    ----------
    priv_key: hex str
        The private key to sign the message with.
    payload:
        The message to be signed.

    Returns
    -------
    bytes
        The signature concatenated with the original message.
    """
    sig_key = SigningKey(bytes.fromhex(priv_key[:64]))
    signed = sig_key.sign(payload)
    return signed.signature + signed.message
