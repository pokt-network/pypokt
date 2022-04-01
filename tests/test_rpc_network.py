import os

from dotenv import load_dotenv
import pytest
from requests import Session

from pokt.rpc.data.network import get_height, get_supply, get_all_params
from pokt.rpc.models import (
    QuerySupplyResponse,
    AllParams,
)
from pokt.rpc.models.validation._overrides import (
    IntParam,
    FloatParam,
    BoolParam,
    StrParam,
    SupportedBlockchainsParam,
    FeeMultiplier,
    FeeMultiplierParam,
    Upgrade,
    UpgradeParamObject,
    UpgradeParam,
    ACLKey,
    ACLKeysObject,
    ACLParam,
)


@pytest.fixture
def rpc_url():
    load_dotenv()
    url = os.environ.get("PORTAL_URL")
    if url is None:
        raise ValueError("No RPC_URL variable configured for testing.")
    return url


@pytest.fixture(scope="session", params=[lambda: Session(), lambda: None])
def session(request):
    session = request.param()
    yield session
    if session:
        session.close()


def test_get_height_returns_nonzero_int(rpc_url, session):
    height_resp = get_height(rpc_url, session)
    assert isinstance(height_resp.height, int)
    assert height_resp.height > 0
