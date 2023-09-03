"""Major indices aggregate end of day price data model."""


from datetime import (
    date as dateType,
    datetime,
)
from typing import Optional

from pydantic import Field, NonNegativeInt, PositiveFloat

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.standard_models.base import BaseSymbol
from openbb_provider.utils.descriptions import DATA_DESCRIPTIONS, QUERY_DESCRIPTIONS


class MajorIndicesHistoricalQueryParams(QueryParams, BaseSymbol):
    """Major Indices end of day Query."""

    start_date: Optional[dateType] = Field(
        description=QUERY_DESCRIPTIONS.get("start_date", ""), default=None
    )
    end_date: Optional[dateType] = Field(
        description=QUERY_DESCRIPTIONS.get("end_date", ""), default=None
    )


class MajorIndicesHistoricalData(Data):
    """Major Indices end of day price data."""

    date: datetime | dateType = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    open: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("open", ""))
    high: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("high", ""))
    low: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("low", ""))
    close: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("close", ""))
    volume: Optional[NonNegativeInt] = Field(
        description=DATA_DESCRIPTIONS.get("volume", "")
    )