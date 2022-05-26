import pytest
from pokt.rpc.data import (
    get_app,
    get_apps,
    get_node,
    get_node_claim,
    get_node_claims,
    get_nodes,
    get_signing_info,
)

from pokt.rpc.models import (
    Application,
    Node,
    QueryAppsResponse,
    QueryNodeClaimsResponse,
    QueryNodesResponse,
    QuerySigningInfoResponse,
    QueryNodeClaimResponse,
)


def test_get_app(rpc_url, session, height, app_address):
    app = get_app(rpc_url, app_address, height=height, session=session)
    assert isinstance(app, Application)


def test_get_apps(rpc_url, session, height):
    apps = get_apps(rpc_url, height=height, session=session)
    assert isinstance(apps, QueryAppsResponse)


def test_get_signing_info(rpc_url, session, height):
    signing_info = get_signing_info(rpc_url, height=height, session=session)
    assert isinstance(signing_info, QuerySigningInfoResponse)


def test_get_signing_info_for_address(rpc_url, session, height, account_address):
    signing_info = get_signing_info(
        rpc_url, address=account_address, height=height, session=session
    )
    assert isinstance(signing_info, QuerySigningInfoResponse)


def test_get_node(rpc_url, session, height, node_address):
    node = get_node(rpc_url, node_address, height=height, session=session)
    assert isinstance(node, Node)


def test_get_nodes(rpc_url, session, height):
    nodes = get_nodes(rpc_url, height=height, session=session)
    assert isinstance(nodes, QueryNodesResponse)


def test_get_node_claim(rpc_url, session, node_claim_args):
    node_claim = get_node_claim(rpc_url, session=session, **node_claim_args)
    assert isinstance(node_claim, QueryNodeClaimResponse)


def test_get_node_claims(rpc_url, session, height):
    node_claims = get_node_claims(rpc_url, height=height, session=session)
    assert isinstance(node_claims, QueryNodeClaimsResponse)


def test_get_node_claims_for_address(rpc_url, session, height, node_address):
    node_claims = get_node_claims(
        rpc_url, address=node_address, height=height, session=session
    )
    assert isinstance(node_claims, QueryNodeClaimsResponse)
