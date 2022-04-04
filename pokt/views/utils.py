from .interfaces import SupportedChains

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


def chain_details_from_id(chain_id: str):
    matches = [chain for chain in SupportedChains if chain_id == chain.chainID]
    if not matches:
        raise ValueError("Unrecognized chain with ID {}".format(chain_id))
    return matches[0]


def chain_ids_to_details(supported_chains: list[str]):
    return [chain_details_from_id(chain) for chain in supported_chains]
