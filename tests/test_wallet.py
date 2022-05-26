from pokt.wallet import (
    address_from_pubkey,
    create_new_ppk,
    ppk_from_priv_key,
    sign_with_priv_key,
    verify_signature,
    unlock_ppk,
)


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
