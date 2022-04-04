from functools import wraps

from ._BaseRPCProvider import _BaseRPCProvider

from ..rpc.data import (
    get_block,
    get_block_transactions,
    get_height,
    get_all_params,
    get_param,
    get_state,
    get_supply,
    get_supported_chains,
    get_upgrade,
    get_version,
)


from ..rpc.utils import get_full_param


class PoktRPCDataProvider(_BaseRPCProvider):
    @wraps(get_height)
    def get_height(self):
        return self._make_rpc_call(get_height).height

    @wraps(get_block)
    def get_block(self, *args, **kwargs):
        return self._make_rpc_call(get_block, *args, **kwargs)

    @wraps(get_block_transactions)
    def get_block_transactions(self, *args, **kwargs):
        return self._make_rpc_call(get_block_transactions, *args, **kwargs)

    @wraps(get_all_params)
    def get_all_params(self, *args, **kwargs):
        return self._make_rpc_call(get_all_params, *args, **kwargs)

    @wraps(get_param)
    def get_param(self, *args, **kwargs):
        param_name = args[0]
        _, full_name = get_full_param(param_name)
        if len(args) > 1:
            args = (full_name,) + args[1:]
        else:
            args = (full_name,)
        return self._make_rpc_call(get_param, *args, **kwargs).param_value

    @wraps(get_state)
    def get_state(self, *args, **kwargs):
        return self._make_rpc_call(get_state, *args, **kwargs)

    @wraps(get_supply)
    def get_supply(self, *args, **kwargs):
        return self._make_rpc_call(get_supply, *args, **kwargs)

    @wraps(get_supported_chains)
    def get_supported_chains(self, *args, **kwargs):
        "TODO: Chain ID Map"
        return self._make_rpc_call(get_supported_chains, *args, **kwargs)

    @wraps(get_upgrade)
    def get_upgrade(self, *args, **kwargs):
        return self._make_rpc_call(get_upgrade, *args, **kwargs)

    @wraps(get_version)
    def get_version(self, *args, **kwargs):
        return self._make_rpc_call(get_version, *args, **kwargs)
