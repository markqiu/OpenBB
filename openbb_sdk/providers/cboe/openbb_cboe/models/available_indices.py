"""Available Indices fetcher for CBOE"""

from datetime import time
from typing import Any, Dict, List, Optional

from openbb_provider.abstract.fetcher import Fetcher
from openbb_provider.standard_models.available_indices import (
    AvailableIndicesData,
    AvailableIndicesQueryParams,
)
from pydantic import Field

from openbb_cboe.utils.helpers import Europe, get_cboe_index_directory


class CboeAvailableIndicesQueryParams(AvailableIndicesQueryParams):
    """CBOE Available Indices query.

    Source: https://www.cboe.com/europe/indices/
    """

    europe: bool = Field(
        description="Filter for European indices. False for US indices.", default=False
    )


class CboeAvailableIndicesData(AvailableIndicesData):
    """CBOE Available Indices data.

    Source: https://www.cboe.com/europe/indices/
    """

    isin: Optional[str] = Field(
        description="ISIN code for the index. Valid only for European indices."
    )

    region: Optional[str] = Field(
        description="Region for the index. Valid only for European indices"
    )

    symbol: Optional[str] = Field(description="Symbol for the index.")

    description: Optional[str] = Field(
        description="Description for the index. Valid only for US indices."
    )

    data_delay: Optional[int] = Field(
        description="Data delay for the index. Valid only for US indices."
    )

    open_time: Optional[time] = Field(
        description="Opening time for the index. Valid only for US indices."
    )

    close_time: Optional[time] = Field(
        description="Closing time for the index. Valid only for US indices."
    )

    time_zone: Optional[str] = Field(
        description="Time zone for the index. Valid only for US indices."
    )

    tick_days: Optional[str] = Field(
        description="The trading days for the index. Valid only for US indices."
    )

    tick_frequency: Optional[str] = Field(
        description="The frequency of the index ticks. Valid only for US indices."
    )

    tick_period: Optional[str] = Field(
        description="The period of the index ticks. Valid only for US indices."
    )


class CboeAvailableIndicesFetcher(
    Fetcher[
        CboeAvailableIndicesQueryParams,
        CboeAvailableIndicesData,
    ]
):
    """Transform the query, extract and transform the data from the CBOE endpoints"""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> CboeAvailableIndicesQueryParams:
        """Transform the query params."""

        return CboeAvailableIndicesQueryParams(**params)

    @staticmethod
    def extract_data(
        query: CboeAvailableIndicesQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the CBOE endpoint"""

        if query.europe is True:
            return Europe.list_indices()
        return get_cboe_index_directory().sort_index().reset_index().to_dict("records")

    @staticmethod
    def transform_data(data: List[Dict]) -> List[CboeAvailableIndicesData]:
        """Transform the data to the standard format"""

        return [CboeAvailableIndicesData.parse_obj(d) for d in data]