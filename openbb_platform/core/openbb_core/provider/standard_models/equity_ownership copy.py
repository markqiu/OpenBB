"""Equity Ownership Standard Model."""

from datetime import date as dateType
from typing import Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)
from pydantic import Field, field_validator


class EquityOwnershipQueryParams(QueryParams):
    """Equity Ownership Query."""

    symbol: str = Field(description=QUERY_DESCRIPTIONS.get("symbol", ""))
    start_date: Optional[dateType] = Field(
        default=None, description=QUERY_DESCRIPTIONS.get("start_date", "")
    )
    end_date: Optional[dateType] = Field(
        default=None, description=QUERY_DESCRIPTIONS.get("start_date", "")
    )

    @field_validator("date", mode="before", check_fields=False)
    @classmethod
    def time_validate(cls, v: str):
        """Validate the date."""
        if v is None:
            v = dateType.today()

    @field_validator("symbol", mode="before", check_fields=False)
    @classmethod
    def to_upper(cls, v: str) -> str:
        """Convert field to uppercase."""
        return v.upper()


class EquityOwnershipData(Data):
    """Equity Ownership Data."""
    symbol: str = Field(description=DATA_DESCRIPTIONS.get("symbol", ""))
