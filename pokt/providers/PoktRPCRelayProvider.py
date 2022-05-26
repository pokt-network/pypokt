from ._BaseRPCProvider import _BaseRPCProvider
from .PoktSigner import PoktSigner


class PoktRPCRelayProvider(_BaseRPCProvider, PoktSigner):
    def __init__(self):
        raise NotImplemented
