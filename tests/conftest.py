import json
import os

from dotenv import load_dotenv
import requests
import pytest

from pokt.rpc.data import get_height
from pokt.wallet import PPK, UnlockedPPK


def node_url():
    load_dotenv()
    url = os.environ.get("POCKET_NODE_URL")
    if url is None:
        raise ValueError("No RPC_URL variable configured for testing.")
    return url


def portal_url():
    load_dotenv()
    url = os.environ.get("PORTAL_URL")
    if url is None:
        raise ValueError("No RPC_URL variable configured for testing.")
    return url


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(0, marks=pytest.mark.mainnet),
        pytest.param(1, marks=pytest.mark.testnet),
        pytest.param(2, marks=pytest.mark.localnet),
    ],
    ids=["mainnet", "testnet", "localnet"],
)
def network(request):
    if request.param == 0:
        return "mainnet"
    elif request.param == 1:
        return "testnet"
    elif request.param == 2:
        return "localnet"


@pytest.fixture
def node_claim_args():
    return {
        "address": "000162dbb53a582cac6b2afb58cd37f5c2024a0b",
        "app_pubkey": "4fa09c328d31a61895b721a74cc2a0057ac897304e02777b3d5dda607c597cd7",
        "blockchain": "0009",
        "session_block_height": 60353,
        "height": 60367,
        "receipt_type": "relay",
    }


@pytest.fixture
def node_address(network):
    if network == "mainnet":
        return "000162dbb53a582cac6b2afb58cd37f5c2024a0b"


@pytest.fixture
def app_address(network):
    if network == "mainnet":
        return "00353abd21ef72725b295ba5a9a5eb6082548e23"


@pytest.fixture
def account_address(network):
    if network == "mainnet":
        return "fd35e963452eb9b7b938c36661715cce334b0068"


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(0, marks=pytest.mark.node),
        pytest.param(1, marks=pytest.mark.portal),
    ],
    ids=["node", "portal"],
)
def rpc_url(request):
    if request.param == 0:
        return node_url()
    elif request.param == 1:
        return portal_url()


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(lambda: requests.Session(), marks=pytest.mark.reuse_session),
        pytest.param(lambda: None, marks=pytest.mark.new_session),
    ],
    ids=["reuse session", "new session"],
)
def session(request):
    session = request.param()
    yield session
    if session:
        session.close()


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(None, marks=pytest.mark.latest),
        pytest.param(1, marks=pytest.mark.one_behind),
        pytest.param(10, marks=pytest.mark.many_behind),
        pytest.param(100, marks=pytest.mark.many_behind),
        pytest.param(1000, marks=pytest.mark.many_behind),
        pytest.param(10000, marks=pytest.mark.many_behind),
        pytest.param(25000, marks=pytest.mark.many_behind),
    ],
    ids=[
        "latest block",
        "1 block ago",
        "10 blocks ago",
        "100 blocks ago",
        "1000 blocks ago",
        "10000 blocks ago",
        "25000 blocks ago",
    ],
)
def height(rpc_url, session, request):
    diff = 0 if request.param is None else request.param
    return get_height(rpc_url, session).height - diff


@pytest.fixture
def ppk() -> PPK:
    _dir = os.path.abspath(os.path.dirname(__file__))
    ppk_path = os.path.join(_dir, "reference", "ppk.json")
    return PPK.from_file(ppk_path)


@pytest.fixture
def unlocked() -> UnlockedPPK:
    _dir = os.path.abspath(os.path.dirname(__file__))
    unlocked_path = os.path.join(_dir, "reference", "raw.json")
    with open(unlocked_path, "r") as f:
        data = json.load(f)
    return UnlockedPPK(**data)


@pytest.fixture
def public_key(unlocked) -> str:
    return unlocked.pub_key


@pytest.fixture
def private_key(unlocked) -> str:
    return unlocked.priv_key.get_secret_value()


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
