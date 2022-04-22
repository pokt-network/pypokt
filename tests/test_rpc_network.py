import os
from typing import Mapping

from dotenv import load_dotenv
import pytest
from requests import Session

from pokt.rpc.data.network import (
    get_height,
    get_supply,
    get_all_params,
    get_upgrade,
    get_supported_chains,
    get_param,
    get_version,
    get_state,
)
from pokt.rpc.models import (
    QuerySupplyResponse,
    AllParams,
    SingleParam,
    QueryHeightResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    UpgradeResponse,
    IntParam,
    FloatParam,
    BoolParam,
    StrParam,
    SupportedBlockchainsParam,
    FeeMultiplierParam,
    UpgradeParam,
    ACLParam,
)


@pytest.fixture
def rpc_url():
    load_dotenv()
    url = os.environ.get("PORTAL_URL")
    if url is None:
        raise ValueError("No RPC_URL variable configured for testing.")
    return url


@pytest.fixture(params=[lambda: Session(), lambda: None])
def session(request):
    session = request.param()
    yield session
    if session:
        session.close()


@pytest.fixture
def current_height(rpc_url, session):
    return get_height(rpc_url, session).height


def test_get_height_returns_nonzero_int(rpc_url, session):
    height_resp = get_height(rpc_url, session)
    assert isinstance(height_resp, QueryHeightResponse)
    assert isinstance(height_resp.height, int)
    assert height_resp.height > 0


def test_get_version(rpc_url, session):
    version_resp = get_version(rpc_url, session)


@pytest.mark.parametrize("height_diff", (1, 10, 100, 1000))
class TestNetworkWithHeights:
    def test_get_supply(self, rpc_url, session, current_height, height_diff):
        supply_resp = get_supply(
            rpc_url, height=current_height - height_diff, session=session
        )
        assert isinstance(supply_resp, QuerySupplyResponse)

    def test_get_all_params(self, rpc_url, session, current_height, height_diff):
        params_resp = get_all_params(
            rpc_url, height=current_height - height_diff, session=session
        )
        assert isinstance(params_resp, AllParams)

    def test_get_upgrade(self, rpc_url, session, current_height, height_diff):
        upgrade_resp = get_upgrade(
            rpc_url, height=current_height - height_diff, session=session
        )
        assert isinstance(upgrade_resp, UpgradeResponse)

    def test_get_supported_chains(self, rpc_url, session, current_height, height_diff):
        supported_chains_resp = get_supported_chains(
            rpc_url, height=current_height - height_diff, session=session
        )
        assert isinstance(supported_chains_resp, QuerySupportedChainsResponse)

    def test_get_state(self, rpc_url, session, current_height, height_diff):
        state_resp = get_state(
            rpc_url, height=current_height - height_diff, session=session
        )
        assert isinstance(state_resp, Mapping)
