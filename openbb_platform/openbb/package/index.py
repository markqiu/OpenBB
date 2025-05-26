### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from openbb_core.app.static.container import Container
from openbb_core.app.model.obbject import OBBject
import openbb_core.provider
from openbb_core.provider.abstract.data import Data
import pandas
from pandas import DataFrame, Series
import numpy
from numpy import ndarray
import datetime
from datetime import date
import pydantic
from pydantic import BaseModel
from inspect import Parameter
import typing
from typing import TYPE_CHECKING, ForwardRef, Union, Optional, Literal, Any
from annotated_types import Ge, Le, Gt, Lt
from warnings import warn, simplefilter
from typing_extensions import Annotated, deprecated
from openbb_core.app.static.utils.decorators import exception_handler, validate

from openbb_core.app.static.utils.filters import filter_inputs

from openbb_core.app.deprecation import OpenBBDeprecationWarning

from openbb_core.app.model.field import OpenBBField
from fastapi import Depends
import openbb_core.app.model.command_context
import openbb_core.app.provider_interface
import typing

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.provider_interface import (
    OBBject_AvailableIndices,
    OBBject_IndexConstituents,
    OBBject_IndexSearch,
)

from typing import (
    AvailableIndices,
    IndexConstituents,
    IndexSearch,
)

class ROUTER_index(Container):
    """/index
    available
    constituents
    /fundamental
    /price
    search
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def available(
        self,
        provider: Annotated[Optional[Literal['fmp', 'yfinance']], OpenBBField(description='The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: fmp, yfinance.')] = None,
        **kwargs
    ) -> OBBject:
        """All indices available from a given provider.

        Parameters
        ----------
        provider : str
            The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: fmp, yfinance.

        Returns
        -------
        OBBject
            results : list[AvailableIndices]
                Serializable results.
            provider : Optional[str]
                Provider name.
            warnings : Optional[list[Warning_]]
                list of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        AvailableIndices
        ----------------
        name : Optional[str]
            Name of the index.
        currency : Optional[str]
            Currency the index is traded in.
        stock_exchange : Optional[str]
            Stock exchange where the index is listed. (provider: fmp)
        exchange_short_name : Optional[str]
            Short name of the stock exchange where the index is listed. (provider: fmp)
        code : Optional[str]
            ID code for keying the index in the OpenBB Terminal. (provider: yfinance)
        symbol : Optional[str]
            Symbol for the index. (provider: yfinance)

        Examples
        --------
        >>> from openbb import obb
        >>> obb.index.available(provider='fmp')
        >>> obb.index.available(provider='yfinance')
        """  # noqa: E501

        return self._run(
            "/index/available",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "index.available",
                        ('fmp', 'yfinance'),
                    )
                },
                standard_params={
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def constituents(
        self,
        symbol: Annotated[str, OpenBBField(description='Symbol to get data for.')],
        provider: Annotated[Optional[Literal['fmp', 'xiaoyuan']], OpenBBField(description='The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: fmp, xiaoyuan.')] = None,
        **kwargs
    ) -> OBBject:
        """Get Index Constituents.

        Parameters
        ----------
        provider : str
            The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: fmp, xiaoyuan.
        symbol : str
            Symbol to get data for.
        start_date : Optional[date]
            Date to get the index constituents. (provider: xiaoyuan)
        end_date : Optional[date]
            Date to get the index constituents. (provider: xiaoyuan)

        Returns
        -------
        OBBject
            results : list[IndexConstituents]
                Serializable results.
            provider : Optional[str]
                Provider name.
            warnings : Optional[list[Warning_]]
                list of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexConstituents
        -----------------
        symbol : str
            Symbol representing the entity requested in the data.
        name : Optional[str]
            Name of the constituent company in the index.
        sector : Optional[str]
            Sector the constituent company in the index belongs to. (provider: fmp, xiaoyuan)
        sub_sector : Optional[str]
            Sub-sector the constituent company in the index belongs to. (provider: fmp, xiaoyuan)
        headquarter : Optional[str]
            Location of the headquarter of the constituent company in the index. (provider: fmp, xiaoyuan)
        date_first_added : Optional[Union[str, date]]
            Date the constituent company was added to the index. (provider: fmp, xiaoyuan)
        cik : Optional[int]
            Central Index Key (CIK) for the requested entity. (provider: fmp, xiaoyuan)
        founded : Optional[Union[str, date]]
            Founding year of the constituent company in the index. (provider: fmp, xiaoyuan)

        Examples
        --------
        >>> from openbb import obb
        >>> obb.index.constituents(symbol='dowjones', provider='fmp')
        """  # noqa: E501

        return self._run(
            "/index/constituents",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "index.constituents",
                        ('fmp', 'xiaoyuan'),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )

    @property
    def fundamental(self):
        # pylint: disable=import-outside-toplevel
        from . import index_fundamental

        return index_fundamental.ROUTER_index_fundamental(command_runner=self._command_runner)

    @property
    def price(self):
        # pylint: disable=import-outside-toplevel
        from . import index_price

        return index_price.ROUTER_index_price(command_runner=self._command_runner)

    @exception_handler
    @validate
    def search(
        self,
        query: Annotated[str, OpenBBField(description='Search query.')] = '',
        is_symbol: Annotated[bool, OpenBBField(description='Whether to search by ticker symbol.')] = False,
        provider: Annotated[Optional[Literal['xiaoyuan']], OpenBBField(description='The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: xiaoyuan.')] = None,
        **kwargs
    ) -> OBBject:
        """Filter indices for rows containing the query.

        Parameters
        ----------
        provider : str
            The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: xiaoyuan.
        query : str
            Search query.
        is_symbol : bool
            Whether to search by ticker symbol.

        Returns
        -------
        OBBject
            results : list[IndexSearch]
                Serializable results.
            provider : Optional[str]
                Provider name.
            warnings : Optional[list[Warning_]]
                list of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexSearch
        -----------
        symbol : str
            Symbol representing the entity requested in the data.
        name : str
            Name of the index.
        list_date : Optional[date]
            The date on which the stock was listed on the exchange. (provider: xiaoyuan)
        exchange : Optional[str]
            The exchange on which the stock is listed. (provider: xiaoyuan)
        end_date : Optional[date]
            The date on which the stock was delisted from the exchange. (provider: xiaoyuan)
        limit_up_count : Optional[float]
            The number of times the stock has been limited up. (provider: xiaoyuan)
        limit_down_count : Optional[float]
            The number of times the stock has been limited down. (provider: xiaoyuan)
        suspend_count : Optional[float]
            The number of times the stock has been suspended. (provider: xiaoyuan)
        up_count : Optional[float]
            The number of times the stock has been up. (provider: xiaoyuan)
        down_count : Optional[float]
            The number of times the stock has been down. (provider: xiaoyuan)
        flat_count : Optional[float]
            The number of times the stock has been flat. (provider: xiaoyuan)
        amplitude : Optional[str]
            The amplitude of the stock. (provider: xiaoyuan)
        """  # noqa: E501

        return self._run(
            "/index/search",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "index.search",
                        ('xiaoyuan',),
                    )
                },
                standard_params={
                    "query": query,
                    "is_symbol": is_symbol,
                },
                extra_params=kwargs,
            )
        )
