from typing import Optional

from ._BaseRPCProvider import _BaseRPCProvider

import requests

from ..rpc.data import (
    get_account,
    get_account_transactions,
    get_accounts,
    get_all_params,
    get_app,
    get_apps,
    get_block,
    get_block_transactions,
    get_height,
    get_mempool_txs,
    get_node,
    get_node_claim,
    get_node_claims,
    get_nodes,
    get_param,
    get_signing_info,
    get_state,
    get_supply,
    get_supported_chains,
    get_transaction_by_hash,
    get_unconfirmed_transaction_by_hash,
    get_upgrade,
    get_version,
)
from ..rpc.models import (
    AllParams,
    Application,
    BaseAccountVal,
    Node,
    ParamKeys,
    ParamValueT,
    QueryAccountTXsResponse,
    QueryAccountsResponse,
    QueryAppsResponse,
    QueryBlockResponse,
    QueryBlockResponse,
    QueryBlockTXsResponse,
    QueryBlockTXsResponse,
    QueryNodeClaimResponse,
    QueryNodeClaimsResponse,
    QueryNodesResponse,
    QuerySigningInfoResponse,
    QuerySupplyResponse,
    QuerySupportedChainsResponse,
    QueryUnconfirmedTXsResponse,
    ReceiptType,
    SortOrder,
    StateResponse,
    Transaction,
    UnconfirmedTransaction,
    Upgrade,
)


class PoktRPCDataProvider(_BaseRPCProvider):
    """
    Handles all methods for querying data from the Pocket Network mainnet, these are handled via the /query/ routes.
    """

    def get_height(self, session: Optional[requests.Session] = None) -> int:
        """
        Get the current height of the network.

        Returns
        -------
        int
        """
        session = self.session if session is None else session
        return get_height(self.url, session=session).height

    def get_block(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> QueryBlockResponse:
        """
        Get the block at a specified height.


        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryBlockResponse
        """
        session = self.session if session is None else session
        return get_block(self.url, height=height, session=session)

    def get_block_transactions(
        self,
        height: int = 0,
        page: int = 1,
        per_page: int = 100,
        prove: bool = False,
        order: SortOrder = "desc",
        session: Optional[requests.Session] = None,
    ) -> QueryBlockTXsResponse:
        """
        Get a list of transactions from the block at the specfified height.

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        received: optional
            Whether to include only received transactions, defaults to True.
        prove: optional
            If you want to be certain that the transaction is from the block, it's inherited from TM.
            If this is true, txs.proof = null.
        order: optional
            The order that the results should be sorted in, either 'desc' or 'asc', defaults to 'desc'
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryBlockTXsResponse
        """
        session = self.session if session is None else session
        return get_block_transactions(
            self.url,
            height=height,
            page=page,
            per_page=per_page,
            prove=prove,
            order=order,
            session=session,
        )

    def get_account(
        self,
        address: str,
        height: int = 0,
        session: Optional[requests.Session] = None,
    ) -> BaseAccountVal:
        """
        Get the account with the given address at a specified height.

        Parameters
        ----------
        address
            The address of the account
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        BaseAccountVal
        """
        session = self.session if session is None else session
        return get_account(self.url, address, height=height, session=session)

    def get_accounts(
        self,
        height: int = 0,
        page: int = 1,
        per_page: int = 100,
        session: Optional[requests.Session] = None,
    ) -> QueryAccountsResponse:
        """
        Get a list of all accounts on the network by page

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        page: optional
            The page to access; defaults to the first page.
        per_page: optional
            The total amount of accounts per page, max value of 10,000; defaults to 100.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.


        Returns
        -------
        QueryAccountsResponse
        """
        session = self.session if session is None else session
        return get_accounts(
            self.url, height=height, page=page, per_page=per_page, session=session
        )

    def get_account_transactions(
        self,
        address: str,
        page: int = 1,
        per_page: int = 100,
        received: bool = False,
        prove: bool = False,
        order: SortOrder = "desc",
        session: Optional[requests.Session] = None,
    ) -> QueryAccountTXsResponse:
        """
        Get a list of transactions for a given account at a specified height.

        Parameters
        ----------
        address
            The address of the account
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        received: optional
            Whether to include only received transactions, defaults to False.
        prove: optional
            Whether to include only proof transactions, defaults to False.
        order: optional
            The order that the results should be sorted in, either 'desc' or 'asc', defaults to 'desc'
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryAccountTXsResponse
        """
        session = self.session if session is None else session
        return get_account_transactions(
            self.url,
            address,
            page=page,
            per_page=per_page,
            received=received,
            prove=prove,
            order=order,
            session=session,
        )

    def get_all_params(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> AllParams:
        """
        Get the values of all protocol parameters at a specified height.


        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        AllParams
        """
        session = self.session if session is None else session
        return get_all_params(self.url, height=height, session=session)

    def get_param(
        self,
        param_key: ParamKeys,
        height: int = 0,
        session: Optional[requests.Session] = None,
    ) -> ParamValueT:
        """
        Get the value of the desired protocol parameter at a specified height

        Parameters
        ----------
        param_key
            The key to the desired parameter
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        ParamValueT
        """
        session = self.session if session is None else session
        return get_param(
            self.url, param_key, height=height, session=session
        ).param_value

    def get_state(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> StateResponse:
        """
        Get the network state at a specified height.

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        StateResponse
        """
        session = self.session if session is None else session
        return get_state(self.url, height=height, session=session)

    def get_supply(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> QuerySupplyResponse:
        """
        Get the supply infomration at a specified height.

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QuerySupplyResponse
        """
        session = self.session if session is None else session
        return get_supply(self.url, height=height, session=session)

    def get_supported_chains(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> QuerySupportedChainsResponse:
        """
        Get the list of supported chain ids at a specified height.


        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QuerySupportedChainsResponse
        """
        session = self.session if session is None else session
        return get_supported_chains(self.url, height=height, session=session)

    def get_upgrade(
        self, height: int = 0, session: Optional[requests.Session] = None
    ) -> Upgrade:
        """
        Get the upgrade information at a specified height.


        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        Upgrade
        """
        session = self.session if session is None else session
        return get_upgrade(self.url, height=height, session=session)

    def get_version(self, session: Optional[requests.Session] = None) -> str:
        """
        Get the current version.

        Parameters
        ----------
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        str
        """
        session = self.session if session is None else session
        return get_version(self.url, session=session)

    def get_transaction_by_hash(
        self,
        tx_hash: str,
        prove: bool = False,
        session: Optional[requests.Session] = None,
    ) -> Transaction:
        """
        Get a specific transaction by hash.

        Parameters
        ----------
        tx_hash
            The hash of the transaction
        prove: optional
            Whether or not to inclue to proof of the transaction, defaults to False.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        Transaction
        """
        session = self.session if session is None else session
        return get_transaction_by_hash(self.url, tx_hash, prove=prove, session=session)

    def get_app(
        self,
        address: str,
        height: int = 0,
        session: Optional[requests.Session] = None,
    ) -> Application:
        """
        Get the application by address at a specified height

        Parameters
        ----------
        address
            The address of the app
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        Application
        """
        session = self.session if session is None else session
        return get_app(self.url, address, height=height, session=session)

    def get_apps(
        self,
        height: int = 0,
        page: int = 1,
        per_page: int = 100,
        staking_status: Optional[int] = None,
        blockchain: str = "",
        session: Optional[requests.Session] = None,
    ) -> QueryAppsResponse:
        """
        Get a paginated list of apps on the network by search criteria

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        staking_status: optional
            Whether or not the app is staked (2) or unstaking (1); defaults to staked.
        blockchain: optional
            The relay chain the apps are staked for.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryAppsReponse
        """
        session = self.session if session is None else session
        return get_apps(
            self.url,
            height=height,
            page=page,
            per_page=per_page,
            staking_status=staking_status,
            blockchain=blockchain,
            session=session,
        )

    def get_node(
        self,
        address: str,
        height: int = 0,
        session: Optional[requests.Session] = None,
    ) -> Node:
        """
        Get the node by address at a specified height

        Parameters
        ----------
        address
            The address of the node
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        Node
        """
        session = self.session if session is None else session
        return get_node(self.url, address, height=height, session=session)

    def get_nodes(
        self,
        height: int = 0,
        page: int = 0,
        per_page: int = 10,
        staking_status: Optional[int] = None,
        jailed_status: Optional[int] = None,
        blockchain: str = "",
        session: Optional[requests.Session] = None,
    ) -> QueryNodesResponse:
        """
        Get a paginated list of apps on the network by search criteria

        Parameters
        ----------
        height: optional
            The height to get the state at, if none is provided, defaults to the latest height.
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        staking_status: optional
            Whether or not the node is staked (2) or unstaking (1); defaults to neither.
        jailed_status: optional
            Whether or not the node is jailed (1) or unjailed (1); defaults to neither
        blockchain: optional
            The relay chain the nodes are staked for.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryNodesResponse
        """
        session = self.session if session is None else session
        return get_nodes(
            self.url,
            height=height,
            page=page,
            per_page=per_page,
            staking_status=staking_status,
            jailed_status=jailed_status,
            blockchain=blockchain,
            session=session,
        )

    def get_node_claim(
        self,
        address: str,
        blockchain: str,
        app_pubkey: str,
        height: int,
        session_block_height: int,
        receipt_type: ReceiptType = "relay",
        session: Optional[requests.Session] = None,
    ) -> QueryNodeClaimResponse:
        """
        Get the specific outstanding claim for a node

        Parameters
        ----------
        provider_url
            The URL to make the RPC call to.
        address
            The address of the node
        blockchain: str
            The chain the node claimed service on
        app_pubkey:
            The public key of the app the node claimed to service
        height:
            The height the claim was made
        session_block_height:
            The height of the session the node is claiming for
        receipt_type: optional
            The kind of claim; defaults to Relay
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryNodeClaimResponse
        """
        session = self.session if session is None else session
        return get_node_claim(
            self.url,
            address,
            blockchain,
            app_pubkey,
            height,
            session_block_height,
            receipt_type=receipt_type,
            session=session,
        )

    def get_node_claims(
        self,
        address: str = "",
        height: int = 0,
        page: int = 1,
        per_page: int = 1000,
        session: Optional[requests.Session] = None,
    ) -> QueryNodeClaimsResponse:
        """
        Get a paginated list of claims made by a given node

        Parameters
        ----------
        address
            The address of the node
        height: optional
            The height the claims were made after
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryNodeClaimsResponse
        """
        session = self.session if session is None else session
        return get_node_claims(
            self.url,
            address=address,
            height=height,
            page=page,
            per_page=per_page,
            session=session,
        )

    def get_signing_info(
        self,
        address: Optional[str] = None,
        height: int = 0,
        page: int = 0,
        per_page: int = 100,
        session: Optional[requests.Session] = None,
    ) -> QuerySigningInfoResponse:
        """
        Get either the signing info of a particular address, or a paginated list for all accounts

        Parameters
        ----------
        provider_url
            The URL to make the RPC call to.
        address: optional
            The address of the account
        height: optional
            The height to look after
        page: optional
            The index of the page, defaults to the first page.
        per_page: optional
            The amount of results to return for each page, defaults to 100.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QuerySigningInfoResponse
        """
        session = self.session if session is None else session
        return get_signing_info(
            self.url,
            address=address,
            height=height,
            page=page,
            per_page=per_page,
            session=session,
        )

    def get_unconfirmed_transaction_by_hash(
        self,
        tx_hash: str,
        session: Optional[requests.Session] = None,
    ) -> UnconfirmedTransaction:
        """
        Get a specific transaction by hash.

        Parameters
        ----------
        tx_hash
            The hash of the transaction
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        UnconfirmedTransaction
        """
        session = self.session if session is None else session
        return get_unconfirmed_transaction_by_hash(self.url, tx_hash, session=session)

    def get_mempool_txs(
        self,
        page: int = 1,
        per_page: int = 100,
        session: Optional[requests.Session] = None,
    ) -> QueryUnconfirmedTXsResponse:
        """
        Get the paginated unconfirmed transactions from the mempool

        Parameters
        ----------
        page: optional
            The page to retrieve; defaults to the first page.
        per_page: optional
            The number of transactions to return per page; defaults to 100.
        session: optional
            The optional requests session, if none is provided, the request will be handled by calling requests.post directly.

        Returns
        -------
        QueryUnconfirmedTXsResponse
        """
        session = self.session if session is None else session
        return get_mempool_txs(self.url, page=page, per_page=per_page, session=session)
