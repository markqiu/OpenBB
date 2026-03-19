"""Price Router."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.example import APIEx
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="/price")

# pylint: disable=unused-argument


@router.command(
    model="EquityQuote",
    examples=[APIEx(parameters={"symbol": "AAPL", "provider": "fmp"})],
)
async def quote(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get the latest quote for a given stock. Quote includes price, volume, and other data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="EquityNBBO",
)
async def nbbo(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get the National Best Bid and Offer for a given stock."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="EquityHistorical",
    examples=[
        APIEx(parameters={"symbol": "AAPL", "provider": "fmp"}),
        APIEx(parameters={"symbol": "AAPL", "interval": "1d", "provider": "intrinio"}),
    ],
)
async def historical(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get historical price data for a given stock. This includes open, high, low, close, and volume."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="PricePerformance",
    examples=[APIEx(parameters={"symbol": "AAPL", "provider": "fmp"})],
)
async def performance(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get price performance data for a given stock. This includes price changes for different time periods."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="MoneyFlow",
    examples=[
        APIEx(
            description="Get money flow data (net inflow by order size) from East Money.",
            parameters={"symbol": "600000.SH", "provider": "eastmoney"},
        ),
        APIEx(
            description="Get money flow data from JoinQuant.",
            parameters={"symbol": "600000.XSHG", "provider": "joinquant"},
        ),
    ],
)
async def money_flow(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get money flow data for a stock.
    
    Money flow tracks the net buying/selling pressure from different
    order sizes (super large, large, medium, small orders).
    
    Providers: eastmoney, joinquant
    """
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="EquityPledge",
    examples=[
        APIEx(
            description="Get equity pledge data from East Money.",
            parameters={"symbol": "600000.SH", "provider": "eastmoney"},
        ),
        APIEx(
            description="Get equity pledge data from JoinQuant.",
            parameters={"symbol": "600000.XSHG", "provider": "joinquant"},
        ),
    ],
)
async def pledge(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get equity pledge data for a stock.
    
    Equity pledge tracks the shares pledged by major shareholders
    as collateral for loans.
    
    Providers: eastmoney, joinquant
    """
    return await OBBject.from_query(Query(**locals()))
