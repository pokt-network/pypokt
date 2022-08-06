from functools import lru_cache
from typing import Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, root_validator


class ProxySettings(BaseSettings):
    portal_url: Optional[HttpUrl] = None
    pocket_node_url: Optional[AnyHttpUrl] = None
    prioritize_portal: bool = True

    @root_validator(pre=True)
    def must_have_some_url(cls, vals):
        if vals.get("portal_url") is None and vals.get("pocket_node_url") is None:
            raise ValueError("Either a Portal URL or Pocket Node URL must be provided")
        return vals

    @property
    def url(self) -> Union[AnyHttpUrl, HttpUrl]:
        if self.prioritize_portal:
            return self.pocket_node_url if self.portal_url is None else self.portal_url  # type: ignore
        return self.portal_url if self.pocket_node_url is None else self.pocket_node_url  # type: ignore


@lru_cache
def settings() -> ProxySettings:
    return ProxySettings()
