import os
import json

import pytest
from pokt import PPK, UnlockedAccount
from pokt.wallet import (
    address_from_pubkey,
    create_new_ppk,
    ppk_from_priv_key,
    sign_with_priv_key,
    verify_signature,
    unlock_ppk,
)
from nacl.signing import VerifyKey


@pytest.fixture
def ppk() -> PPK:
    _dir = os.path.abspath(os.path.dirname(__file__))
    ppk_path = os.path.join(_dir, "reference", "ppk.json")
    with open(ppk_path, "r") as f:
        data = json.load(f)
    return PPK(**data)


@pytest.fixture
def unlocked() -> UnlockedAccount:
    _dir = os.path.abspath(os.path.dirname(__file__))
    unlocked_path = os.path.join(_dir, "reference", "raw.json")
    with open(unlocked_path, "r") as f:
        data = json.load(f)
    return UnlockedAccount(**data)


@pytest.fixture
def public_key(unlocked) -> str:
    return unlocked.pubKey


@pytest.fixture
def private_key(unlocked) -> str:
    return unlocked.privKey.get_secret_value()


@pytest.fixture
def address(unlocked):
    return unlocked.address


@pytest.fixture
def passphrase():
    _dir = os.path.abspath(os.path.dirname(__file__))
    passphrase_path = os.path.join(_dir, "reference", "passphrase.txt")
    with open(passphrase_path, "r", encoding="utf-8") as f:
        passphrase = f.read().strip()
    return passphrase


def test_unlock_ppk(ppk, passphrase, unlocked):
    result = unlock_ppk(ppk, passphrase)
    assert result.pubKey == unlocked.pubKey
    assert result.privKey == unlocked.privKey
    assert result.address == unlocked.address


def test_create_new_ppk_unlocks_with_passphrase():
    result = create_new_ppk("ThisIsAPassphrase")
    _ = unlock_ppk(result, "ThisIsAPassphrase")


def test_ppk_from_priv_key_unlocks_with_passphrase(private_key):
    result = ppk_from_priv_key(private_key, "ThisIsAPassphrase")
    unlocked_result = unlock_ppk(result, "ThisIsAPassphrase")
    assert unlocked_result.privKey.get_secret_value() == private_key


def test_address_from_pubkey(public_key, address):
    result = address_from_pubkey(public_key)
    assert result == address


def test_sign_with_priv_key_and_verify(private_key, public_key):
    signed_msg = sign_with_priv_key(private_key, "Hi There!".encode("utf-8"))
    is_valid = verify_signature(public_key, signed_msg)
    assert is_valid
