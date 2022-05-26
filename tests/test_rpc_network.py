import pytest

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
    QueryHeightResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    Upgrade,
    StateResponse,
    IntParam,
    FloatParam,
    BoolParam,
    StrParam,
    SupportedBlockchainsParam,
    FeeMultiplierParam,
    UpgradeParam,
    ACLParam,
)


def test_get_height_returns_nonzero_int(rpc_url, session):
    height = get_height(rpc_url, session)
    assert isinstance(height, QueryHeightResponse)
    assert height.height > 0


def test_get_version(rpc_url, session):
    version_resp = get_version(rpc_url, session)
    assert isinstance(version_resp, str)


def test_get_supply(rpc_url, session, height):
    supply_resp = get_supply(rpc_url, height=height, session=session)
    assert isinstance(supply_resp, QuerySupplyResponse)


def test_get_all_params(rpc_url, session, height):
    params_resp = get_all_params(rpc_url, height=height, session=session)
    assert isinstance(params_resp, AllParams)


def test_get_upgrade(rpc_url, session, height):
    upgrade_resp = get_upgrade(rpc_url, height=height, session=session)
    assert isinstance(upgrade_resp, Upgrade)


def test_get_supported_chains(rpc_url, session, height):
    supported_chains_resp = get_supported_chains(
        rpc_url, height=height, session=session
    )
    assert isinstance(supported_chains_resp, QuerySupportedChainsResponse)


def test_get_state(rpc_url, session, height):
    state_resp = get_state(rpc_url, height=height, session=session)
    assert isinstance(state_resp, StateResponse)


@pytest.mark.parametrize(
    ("param_name", "param_type"),
    [
        ("application/MaxApplications", IntParam),
        ("application/AppUnstakingTime", IntParam),
        ("application/MaximumChains", IntParam),
        ("application/StabilityAdjustment", IntParam),
        ("application/BaseRelaysPerPOKT", IntParam),
        ("application/ApplicationStakeMinimum", IntParam),
        ("pos/DAOAllocation", IntParam),
        ("pos/StakeMinimum", IntParam),
        ("pos/MaximumChains", IntParam),
        ("pos/RelaysToTokensMultiplier", IntParam),
        ("pos/MaxJailedBlocks", IntParam),
        ("pos/MaxValidators", IntParam),
        ("pos/UnstakingTime", IntParam),
        ("pos/DowntimeJailDuration", IntParam),
        ("pos/ProposerPercentage", IntParam),
        ("pos/BlocksPerSession", IntParam),
        ("pos/MaxEvidenceAge", IntParam),
        ("pos/SignedBlocksWindow", IntParam),
        ("pocketcore/SessionNodeCount", IntParam),
        ("pocketcore/ClaimSubmissionWindow", IntParam),
        ("pocketcore/ReplayAttackBurnMultiplier", IntParam),
        ("pocketcore/ClaimExpiration", IntParam),
        ("pocketcore/MinimumNumberOfProofs", IntParam),
        ("auth/MaxMemoCharacters", IntParam),
        ("auth/TxSigLimit", IntParam),
        ("pos/StakeDenom", StrParam),
        ("gov/daoOwner", StrParam),
        ("pos/SlashFractionDoubleSign", FloatParam),
        ("pos/SlashFractionDowntime", FloatParam),
        ("pos/MinSignedPerWindow", FloatParam),
        ("application/ParticipationRateOn", BoolParam),
        ("pocketcore/SupportedBlockchains", SupportedBlockchainsParam),
        ("auth/FeeMultipliers", FeeMultiplierParam),
        ("gov/acl", ACLParam),
        ("gov/upgrade", UpgradeParam),
    ],
)
def test_get_params(rpc_url, session, height, param_name, param_type):
    param_resp = get_param(rpc_url, param_name, height=height, session=session)
    assert isinstance(param_resp, param_type)
