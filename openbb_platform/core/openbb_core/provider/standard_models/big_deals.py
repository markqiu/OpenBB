"""Big Deals Standard Model."""

from datetime import (
    date as dateType,
    timedelta,
)
from typing import Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)
from pydantic import Field, field_validator


class BigDealsQueryParams(QueryParams):
    """Big Deals Query."""

    symbol: str = Field(description=QUERY_DESCRIPTIONS.get("symbol", ""))
    date: Optional[dateType] = Field(
        default=dateType.today() - timedelta(days=1),
        description=QUERY_DESCRIPTIONS.get("date", ""),
    )

    @field_validator("symbol", mode="before", check_fields=False)
    @classmethod
    def to_upper(cls, v: str) -> str:
        """Convert field to uppercase."""
        return v.upper() if v else None


class BigDealsData(Data):
    """Big Deals Data."""

    symbol: str = Field(description=DATA_DESCRIPTIONS.get("symbol", ""))
    name: str = Field(description="The name of the stock.")
    net_in_flow: Optional[float] = Field(
        default=None,
        description="Net inflow of main funds today.",
    )
    super_net_in_flow: Optional[float] = Field(
        default=None,
        description="Net inflow of super-large orders today.",
    )
    big_deal_net: Optional[float] = Field(
        default=None,
        description="Net inflow of large orders today.",
    )
    mid_deal_net: Optional[float] = Field(
        default=None,
        description="Net inflow of medium orders today.",
    )
    small_deal_net: Optional[float] = Field(
        default=None,
        description="Net inflow of small orders today.",
    )
