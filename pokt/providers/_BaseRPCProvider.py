from requests import Session


class _BaseRPCProvider:
    def __init__(self, provider_url: str):
        self._url = provider_url
        self._session = Session()

    @property
    def url(self):
        return self._url

    @property
    def session(self):
        return self._session

    def _make_rpc_call(self, rpc_method, *args, **kwargs):
        if not kwargs.get("session"):
            kwargs["session"] = self.session
        return rpc_method(self.url, *args, **kwargs)
