from dataclasses import dataclass
import json
from typing import Optional
import requests

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS


def make_api_url(provider_url: str, route: str, version: str = "v1") -> str:
    if not provider_url.endswith("/"):
        provider_url += "/"
    if not route.startswith("/"):
        route = "/" + route
    return provider_url + version + route


def get(route: str, session: Optional[requests.Session] = None, **params) -> str:
    if session is None:
        resp = requests.get(route, headers=DEFAULT_GET_HEADERS, params=params)
    else:
        resp = session.get(route, params=params, headers=DEFAULT_GET_HEADERS)
    return resp.text


def post(route: str, session: Optional[requests.Session] = None, **payload) -> dict:
    if session is None:
        resp = requests.post(
            route, headers=DEFAULT_POST_HEADERS, data=json.dumps(payload)
        )
    else:
        resp = session.post(
            route, data=json.dumps(payload), headers=DEFAULT_POST_HEADERS
        )
    return resp.json()


_param_keys = [
    "application/MaxApplications",
    "application/AppUnstakingTime",
    "application/MaximumChains",
    "application/StabilityAdjustment",
    "application/BaseRelaysPerPOKT",
    "application/ApplicationStakeMinimum",
    "pos/DAOAllocation",
    "pos/StakeMinimum",
    "pos/MaximumChains",
    "pos/RelaysToTokensMultiplier",
    "pos/MaxJailedBlocks",
    "pos/MaxValidators",
    "pos/UnstakingTime",
    "pos/DowntimeJailDuration",
    "pos/MinSignedPerWindow",
    "pos/ProposerPercentage",
    "pos/BlocksPerSession",
    "pos/MaxEvidenceAge",
    "pos/SignedBlocksWindow",
    "pocketcore/SessionNodeCount",
    "pocketcore/ClaimSubmissionWindow",
    "pocketcore/ReplayAttackBurnMultiplier",
    "pocketcore/ClaimExpiration",
    "pocketcore/MinimumNumberOfProofs",
    "auth/MaxMemoCharacters",
    "auth/TxSigLimit",
    "pos/StakeDenom",
    "gov/daoOwner",
    "pos/SlashFractionDoubleSign",
    "pos/SlashFractionDowntime",
    "application/ParticipationRateOn",
    "pos/MinSignedPerWindow",
    "pocketcore/SupportedBlockchains",
    "auth/FeeMultipliers",
    "gov/acl",
    "gov/upgrade",
]

_key_map = {}

for key in _param_keys:
    module, name = key.split("/")
    _key_map[name] = module


def get_full_param(param_name: str):
    if param_name == "MaximumChains":
        raise ValueError(
            "There are 2 available MaximumChains parameters. Either specify AppMaximumChains or NodeMaximumChains"
        )
    elif param_name == "AppMaximumChains":
        module = "application"
        param_name = "MaximumChains"
    elif param_name == "NodeMaximumChains":
        module = "pos"
        param_name = "MaximumChains"
    else:
        module = _key_map.get(param_name)
    if module not in ("pos", "application", "gov", "pocketcore", "auth"):
        raise ValueError("Unsupported Parameter: {}".format(param_name))
    return module, "{}/{}".format(module, param_name)


@dataclass
class SupportedChain:
    chainID: str
    name: str
    portal_prefix: str
    revenue_generating: bool = False


_SupportedChains = (
    SupportedChain("0001", "Pocket Network", "mainnet", True),
    SupportedChain("0020", "Pocket Network Testnet", "testnet", False),
    SupportedChain("0002", "Bitcoin", "btc-mainnet", False),
    SupportedChain("0003", "Avalanche", "avax-mainnet", True),
    SupportedChain("0004", "Binance Smart Chain", "bsc-mainnet", True),
    SupportedChain("0005", "FUSE", "fuse-mainnet", True),
    SupportedChain("0006", "Solana", "sol-mainnet", True),
    SupportedChain("0009", "Polygon", "poly-mainnet", True),
    SupportedChain("000A", "FUSE Archival", "fuse-archival", True),
    SupportedChain("000B", "Polygon Archival", "poly-archival", True),
    SupportedChain("000C", "Gnosis Chain Archival", "gnosischain-archival", True),
    SupportedChain("000D", "Algorand Archival", "algorand-archival", False),
    SupportedChain("000E", "Avalanche Fuji", "avax-fuji", False),
    SupportedChain("000F", "Polygon Mumbai", "poly-mumbai", False),
    SupportedChain("0010", "Binance Smart Chain Archival", "bsc-archival", True),
    SupportedChain("0011", "Binance Smart Chain Testnet", "bsc-testnet", False),
    SupportedChain(
        "0012", "Binance Smart Chain Testnet Archival", "bsc-testnet-arhival", False
    ),
    SupportedChain("0021", "Ethereum", "eth-mainnet", True),
    SupportedChain("0022", "Ethereum Archival", "eth-archival", True),
    SupportedChain("0023", "Ethereum Ropsten", "eth-ropsten", True),
    SupportedChain("0024", "Ethereum Kovan", "poa-kovan", True),
    SupportedChain("0025", "Ethereum Rinkeby", "eth-rinkeby", True),
    SupportedChain("0026", "Ethereum Goerli", "eth-goerli", True),
    SupportedChain("0027", "Gnosis Chain", "gnosischain-mainnet", True),
    SupportedChain("0028", "Ethereum Archival Trace", "eth-archival-trace", True),
    SupportedChain("0029", "Algorand", "algorand-mainnet", True),
    SupportedChain("0030", "Arweave", "arweave-mainnet", False),
    SupportedChain("0040", "Harmony Shard 0", "harmony-0", True),
    SupportedChain("0041", "Harmony Shard 1", "harmony-1", False),
    SupportedChain("0042", "Harmony Shard 2", "harmony-2", False),
    SupportedChain("0043", "Harmony Shard 3", "harmony-3", False),
    SupportedChain("0044", "IoTeX", "iotex-mainnet", True),
    SupportedChain("0045", "Algorand Testnet", "algorand-testnet", False),
    SupportedChain("0046", "Evmos", "evmos-mainnet", False),
    SupportedChain("0047", "OKExChain", "oec-mainnet", True),
    SupportedChain("0048", "Boba", "boba-mainnet", True),
    SupportedChain("00A3", "Avalanche Archival", "avax-archival", True),
    SupportedChain("00AF", "Polygon Mumbai Archival", "poly-mumbai-archival", False),
    SupportedChain("03DF", "DFKchain Subnet", "dfk-mainnet", True),
    SupportedChain("0A40", "Harmony Shard 0 Archival", "harmony-0-archival", False),
    SupportedChain("0A41", "Harmony Shard 1 Archival", "harmony-1-archival", False),
    SupportedChain("0A42", "Harmony Shard 2 Archival", "harmony-2-archival", False),
    SupportedChain("0A43", "Harmony Shard 3 Archival", "harmony-3-archival", False),
    SupportedChain(
        "0A45", "Algorand Testnet Archival", "algorand-testnet-archival", False
    ),
)


def chain_details_from_id(chain_id: str):
    matches = [chain for chain in _SupportedChains if chain_id == chain.chainID]
    if not matches:
        raise ValueError("Unrecognized chain with ID {}".format(chain_id))
    return matches[0]
