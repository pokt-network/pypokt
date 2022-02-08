from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field, conint


class StakingStatus(int, Enum):
    unstaking = 1
    staked = 2


class JailedStatus(int, Enum):
    jailed = 1
    unjailed = 2


class ValidatorOpts(BaseModel):
    class Config:
        use_enum_values = True

    page: Optional[int] = None
    per_page: conint(gt=0, lt=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Union[StakingStatus, str] = ""
    jailed_status: Union[JailedStatus, str] = ""
    blockchain: Optional[str] = None


class QueryHeightAndValidatorOpts(BaseModel):
    opts: ValidatorOpts
    height: int


class ApplicationOpts(BaseModel):
    class Config:
        use_enum_values = True

    page: Optional[int] = None
    per_page: conint(gt=0, lt=10000) = Field(
        100, description="Number of applications per page"
    )
    staking_status: Union[StakingStatus, str] = ""
    blockchain: Optional[str] = None


class QueryHeightAndApplicationsOpts(BaseModel):
    opts: ApplicationOpts
    height: int


class QueryPaginatedHeightAndAddrParams(BaseModel):
    height: int
    address: Optional[str] = None
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class QueryBlockTXs(BaseModel):
    class Config:
        use_enum_values = True

    height: int
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )
    prove: Optional[bool] = None
    order: SortOrder = Field(
        SortOrder.desc, description="The sort order, either 'asc' or 'desc'"
    )


class QueryAccountTXs(BaseModel):
    class Config:
        use_enum_values = True

    address: str
    page: Optional[int] = None
    per_page: conint(gt=0, le=1000) = Field(
        100, description="Number of transactions per page. Max of 1000"
    )
    received: Optional[bool] = None
    prove: Optional[bool] = None
    order: SortOrder = Field(
        SortOrder.desc, description="The sort order, either 'asc' or 'desc'"
    )
