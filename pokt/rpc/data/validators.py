from typing import List, Optional

import requests

from .service import get_nodes
from .network import get_param
from ..models import Node


def get_validators(
    provider_url: str,
    height: int = 0,
    per_page: int = 10000,
    session: Optional[requests.Session] = None,
) -> List[Node]:
    first_node_page = get_nodes(
        provider_url, height=height, page=1, per_page=per_page, session=session
    )
    nodes = first_node_page.result
    if not nodes:
        raise RuntimeError("No nodes returned for page 1.")
    total_pages = first_node_page.total_pages
    if not total_pages:
        raise RuntimeError("No node pages returned")
    for i in range(2, total_pages + 1):
        node_page = get_nodes(
            provider_url, height=height, page=i, per_page=per_page, session=session
        )

        nodes.extend(node_page.result)
    sorted_nodes = sorted(nodes, key=lambda x: (-int(x.tokens), x.address))
    n_validators = get_param(
        provider_url, param_key="pos/MaxValidators", height=height, session=session
    ).param_value
    return sorted_nodes[:]
