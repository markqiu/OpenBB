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

class Extensions(Container):
    # fmt: off
    """
Routers:
    /commodity
    /crypto
    /currency
    /derivatives
    /economy
    /equity
    /etf
    /fixedincome
    /fund
    /index
    /news
    /regulators

Extensions:
    - commodity@1.3.1
    - crypto@1.4.1
    - currency@1.4.1
    - derivatives@1.4.1
    - economy@1.4.2
    - equity@1.4.1
    - etf@1.4.1
    - fixedincome@1.4.3
    - fund@0.0.2
    - index@1.4.1
    - news@1.4.1
    - regulators@1.4.2

    - akshare@0.6.2
    - benzinga@1.4.1
    - bls@1.1.2
    - cftc@1.1.1
    - ecb@1.4.2
    - econdb@1.3.1
    - federal_reserve@1.4.3
    - fmp@1.4.2
    - fred@1.4.4
    - government_us@1.4.1
    - imf@1.1.1
    - intrinio@1.4.1
    - nasdaq@1.4.1
    - oecd@1.4.1
    - polygon@1.4.1
    - sec@1.4.3
    - tiingo@1.4.1
    - tradingeconomics@1.4.1
    - us_eia@1.1.1
    - xiaoyuan@0.6.2
    - yfinance@1.4.6    """
    # fmt: on

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @property
    def commodity(self):
        # pylint: disable=import-outside-toplevel
        from . import commodity

        return commodity.ROUTER_commodity(command_runner=self._command_runner)

    @property
    def crypto(self):
        # pylint: disable=import-outside-toplevel
        from . import crypto

        return crypto.ROUTER_crypto(command_runner=self._command_runner)

    @property
    def currency(self):
        # pylint: disable=import-outside-toplevel
        from . import currency

        return currency.ROUTER_currency(command_runner=self._command_runner)

    @property
    def derivatives(self):
        # pylint: disable=import-outside-toplevel
        from . import derivatives

        return derivatives.ROUTER_derivatives(command_runner=self._command_runner)

    @property
    def economy(self):
        # pylint: disable=import-outside-toplevel
        from . import economy

        return economy.ROUTER_economy(command_runner=self._command_runner)

    @property
    def equity(self):
        # pylint: disable=import-outside-toplevel
        from . import equity

        return equity.ROUTER_equity(command_runner=self._command_runner)

    @property
    def etf(self):
        # pylint: disable=import-outside-toplevel
        from . import etf

        return etf.ROUTER_etf(command_runner=self._command_runner)

    @property
    def fixedincome(self):
        # pylint: disable=import-outside-toplevel
        from . import fixedincome

        return fixedincome.ROUTER_fixedincome(command_runner=self._command_runner)

    @property
    def fund(self):
        # pylint: disable=import-outside-toplevel
        from . import fund

        return fund.ROUTER_fund(command_runner=self._command_runner)

    @property
    def index(self):
        # pylint: disable=import-outside-toplevel
        from . import index

        return index.ROUTER_index(command_runner=self._command_runner)

    @property
    def news(self):
        # pylint: disable=import-outside-toplevel
        from . import news

        return news.ROUTER_news(command_runner=self._command_runner)

    @property
    def regulators(self):
        # pylint: disable=import-outside-toplevel
        from . import regulators

        return regulators.ROUTER_regulators(command_runner=self._command_runner)
