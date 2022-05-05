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
    get_account,
    get_account_transactions,
    get_transaction_by_hash,
    get_app,
    get_apps,
    get_node,
    get_nodes,
    get_node_claim,
    get_node_claims,
    get_signing_info,
)


from ..views.utils import get_full_param, chain_ids_to_details
from ..views.interfaces import ProtocolParams


class PoktRPCDataProvider(_BaseRPCProvider):
    """
    Handles all methods for querying data from the Pocket Network mainnet, these are handled via the /query/ routes.
    """
    @wraps(get_height)
    def get_height(self):
        return self._make_rpc_call(get_height).height

    @wraps(get_block)
    def get_block(self, *args, **kwargs):
        return self._make_rpc_call(get_block, *args, **kwargs)

    @wraps(get_block_transactions)
    def get_block_transactions(self, *args, **kwargs):
        return self._make_rpc_call(get_block_transactions, *args, **kwargs)

    @wraps(get_account)
    def get_account(self, *args, **kwargs):
        return self._make_rpc_call(get_account, *args, **kwargs)

    @wraps(get_account_transactions)
    def get_account_transactions(self, *args, **kwargs):
        return self._make_rpc_call(get_account_transactions, *args, **kwargs)

    @wraps(get_all_params)
    def get_all_params(self, *args, **kwargs):
        all_params = self._make_rpc_call(get_all_params, *args, **kwargs)
        return ProtocolParams.from_model(all_params)

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
        chain_response = self._make_rpc_call(get_supported_chains, *args, **kwargs)
        return chain_ids_to_details(chain_response.supported_chains)

    @wraps(get_upgrade)
    def get_upgrade(self, *args, **kwargs):
        return self._make_rpc_call(get_upgrade, *args, **kwargs)

    @wraps(get_version)
    def get_version(self, *args, **kwargs):
        return self._make_rpc_call(get_version, *args, **kwargs)

    @wraps(get_transaction_by_hash)
    def get_transaction_by_hash(self, *args, **kwargs):
        return self._make_rpc_call(get_transaction_by_hash, *args, **kwargs)

    @wraps(get_app)
    def get_app(self, *args, **kwargs):
        return self._make_rpc_call(get_app, *args, **kwargs)

    @wraps(get_apps)
    def get_apps(self, *args, **kwargs):
        return self._make_rpc_call(get_apps, *args, **kwargs)

    @wraps(get_node)
    def get_node(self, *args, **kwargs):
        return self._make_rpc_call(get_node, *args, **kwargs)

    @wraps(get_nodes)
    def get_nodes(self, *args, **kwargs):
        return self._make_rpc_call(get_nodes, *args, **kwargs)

    @wraps(get_node_claim)
    def get_node_claim(self, *args, **kwargs):
        return self._make_rpc_call(get_node_claim, *args, **kwargs)

    @wraps(get_node_claims)
    def get_node_claims(self, *args, **kwargs):
        return self._make_rpc_call(get_node_claims, *args, **kwargs)

    @wraps(get_signing_info)
    def get_signing_info(self, *args, **kwargs):
        return self._make_rpc_call(get_signing_info, *args, **kwargs)
