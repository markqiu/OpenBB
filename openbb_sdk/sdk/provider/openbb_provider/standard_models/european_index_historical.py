"""European Indices End of Day data model."""


from datetime import (
    date as dateType,
    datetime,
)
from typing import Optional

from pydantic import Field

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.standard_models.base import BaseSymbol
from openbb_provider.utils.descriptions import DATA_DESCRIPTIONS, QUERY_DESCRIPTIONS


class EuropeanIndexHistoricalQueryParams(QueryParams, BaseSymbol):
    """European Indices end of day Query."""

    start_date: Optional[dateType] = Field(
        description=QUERY_DESCRIPTIONS.get("start_date", ""), default=None
    )
    end_date: Optional[dateType] = Field(
        description=QUERY_DESCRIPTIONS.get("end_date", ""), default=None
    )


class EuropeanIndexHistoricalData(Data):
    """European Indices end of day price data."""

    date: dateType | datetime = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    close: float = Field(description=DATA_DESCRIPTIONS.get("close", ""))