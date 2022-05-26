from dataclasses import dataclass, field
from typing import Any, List, Optional

from ..rpc.models.validation import AllParams, SingleParamT, ParamValueT


class ProtocolParams(AllParams):
    @classmethod
    def from_model(cls, model):
        return cls(**model.dict())

    def get_module_params(self, module_name: str) -> Optional[List[SingleParamT]]:
        check = module_name.lower()
        if check in ("app", "application"):
            return self.app_params
        elif check in ("pos", "node"):
            return self.node_params
        elif check in ("pocket", "core", "pocketcore", "pocket_core", "pocket-core"):
            return self.pocket_params
        elif check in ("gov", "governance", "dao"):
            return self.gov_params
        elif check in ("auth", "authentication"):
            return self.auth_params
        return None

    def get_param(self, param_name: str) -> ParamValueT:
        from ..views.utils import get_full_param

        module, match = get_full_param(param_name)
        group = self.get_module_params(module)
        return [item for item in group if item.param_key == match][0].param_value

    def max_relays(self, app_stake: int) -> float:
        paricipation_rate_on = self.get_param("ParticipationRateOn")
        participation_rate = (
            self.get_param("ParticipationRate") if paricipation_rate_on else 1
        )
        stability_adjustment = self.get_param("StabilityAdjustment")
        base_relays = self.get_param("BaseRelaysPerPOKT")
        return (
            stability_adjustment + participation_rate * (base_relays / 100) * app_stake
        )

    def __getattribute__(self, name: str) -> Any:
        try:
            return self.get_param(name)
        except:
            return super().__getattribute__(name)


@dataclass
class SupportedChain:
    chainID: str
    name: str
    portal_prefix: str
    revenue_generating: bool = False
    aliases: Optional[list[str]] = None

    def __post_init__(self):
        if self.aliases:
            self.aliases.append(self.name)
            self.aliases.append(self.portal_prefix)
        else:
            self.aliases = [self.name, self.portal_prefix]

    def __str__(self):
        return "{} | {} | {} | {}".format(
            self.name,
            self.portal_prefix,
            self.chainID,
            "Y" if self.revenue_generating else "-",
        )


SupportedChains = (
    SupportedChain(
        "0001", "Pocket Network", "mainnet", True, aliases=["pocket", "pokt"]
    ),
    SupportedChain("0002", "Pocket Network Testnet", "testnet", False),
    SupportedChain("0002", "Bitcoin", "btc-mainnet", False),
    SupportedChain("0003", "Avalanche", "avax-mainnet", True, aliases=["avax"]),
    SupportedChain(
        "0004", "Binance Smart Chain", "bsc-mainnet", True, aliases=["bsc", "binance"]
    ),
    SupportedChain("0005", "FUSE", "fuse-mainnet", True),
    SupportedChain("0006", "Solana", "sol-mainnet", True, aliases=["sol"]),
    SupportedChain("0009", "Polygon", "poly-mainnet", True, aliases=["poly, matic"]),
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
    SupportedChain("0021", "Ethereum", "eth-mainnet", True, aliases=["eth"]),
    SupportedChain("0022", "Ethereum Archival", "eth-archival", True),
    SupportedChain(
        "0023", "Ethereum Ropsten", "eth-ropsten", True, aliases=["ropsten"]
    ),
    SupportedChain("0024", "Ethereum Kovan", "poa-kovan", True, aliases=["kovan"]),
    SupportedChain(
        "0025", "Ethereum Rinkeby", "eth-rinkeby", True, aliases=["rinkeby"]
    ),
    SupportedChain("0026", "Ethereum Goerli", "eth-goerli", True, aliases=["goerli"]),
    SupportedChain(
        "0027", "Gnosis Chain", "gnosischain-mainnet", True, aliases=["gnosis", "xdai"]
    ),
    SupportedChain("0028", "Ethereum Archival Trace", "eth-archival-trace", True),
    SupportedChain("0029", "Algorand", "algorand-mainnet", True, aliases=["algo"]),
    SupportedChain("0030", "Arweave", "arweave-mainnet", False, aliases=["arweave"]),
    SupportedChain(
        "0040", "Harmony Shard 0", "harmony-0", True, aliases=["harmony", "hmy"]
    ),
    SupportedChain("0041", "Harmony Shard 1", "harmony-1", False),
    SupportedChain("0042", "Harmony Shard 2", "harmony-2", False),
    SupportedChain("0043", "Harmony Shard 3", "harmony-3", False),
    SupportedChain("0044", "IoTeX", "iotex-mainnet", True),
    SupportedChain("0045", "Algorand Testnet", "algorand-testnet", False),
    SupportedChain("0046", "Evmos", "evmos-mainnet", False),
    SupportedChain("0047", "OKExChain", "oec-mainnet", True, aliases=["okex"]),
    SupportedChain("0048", "Boba", "boba-mainnet", True),
    SupportedChain("00A3", "Avalanche Archival", "avax-archival", False),
    SupportedChain("00AF", "Polygon Mumbai Archival", "poly-mumbai-archival", False),
    SupportedChain("03DF", "DFKchain Subnet", "dfk-mainnet", True, aliases=["dfk"]),
    SupportedChain("0A40", "Harmony Shard 0 Archival", "harmony-0-archival", False),
    SupportedChain("0A41", "Harmony Shard 1 Archival", "harmony-1-archival", False),
    SupportedChain("0A42", "Harmony Shard 2 Archival", "harmony-2-archival", False),
    SupportedChain("0A43", "Harmony Shard 3 Archival", "harmony-3-archival", False),
    SupportedChain(
        "0A45", "Algorand Testnet Archival", "algorand-testnet-archival", False
    ),
    SupportedChain("0A43", "Harmony Shard 3 Archival", "harmony-3-archival", False),
    SupportedChain("03CB", "Swimmer Network Mainnet", "avax-cra", False),
)
