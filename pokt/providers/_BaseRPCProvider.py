from typing import Callable, Concatenate, ParamSpec, TypeVar, Optional
import requests

P = ParamSpec("P")
R = TypeVar("R")


class _BaseRPCProvider:
    def __init__(self, provider_url: str):
        self._url = provider_url
        self._session = requests.Session()

    @property
    def url(self) -> str:
        return self._url

    @property
    def session(self) -> requests.Session:
        return self._session

    def _make_rpc_call(
        self,
        rpc_method: Callable[Concatenate[str, P], R],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> R:
        return rpc_method(self.url, *args, **kwargs)
