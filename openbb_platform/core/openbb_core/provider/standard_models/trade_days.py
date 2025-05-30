"""Trade Days Standard Model."""

from datetime import (
    date as dateType,
)
from typing import Literal, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)
from pydantic import Field


class TradeDaysQueryParams(QueryParams):
    """Trade Days Query."""

    market: Literal["cn", "us"] = Field(
        default="cn", description=QUERY_DESCRIPTIONS.get("symbol", "")
    )
    start_date: Optional[dateType] = Field(
        default=dateType(dateType.today().year, 1, 1),
        description=QUERY_DESCRIPTIONS.get("start_date", ""),
    )
    end_date: Optional[dateType] = Field(
        default=dateType.today(),
        description=QUERY_DESCRIPTIONS.get("end_date", ""),
    )


class TradeDaysData(Data):
    """Trade Days Data."""

    timestamp: list = Field(description=DATA_DESCRIPTIONS.get("date", ""))
