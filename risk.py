import pandas as pd
import numpy as np
from utils import atr

def position_size(equity_now: float, risk_per_trade: float, atr_value: float) -> float:
    # sizing value in currency; risk defined as 2*ATR stop
    if pd.isna(atr_value) or atr_value <= 0:
        return equity_now * risk_per_trade
    risk_atr = 2.0 * atr_value
    size_value = (equity_now * risk_per_trade) / risk_atr
    return max(min(size_value, equity_now), 0)

class CircuitBreaker:
    def __init__(self, equity_series: pd.Series, daily_limit: float, total_limit: float):
        self.daily_limit = daily_limit
        self.total_limit = total_limit
        self.start_equity = float(equity_series.iloc[0]) if len(equity_series)>0 else 1.0
        self.daily_start = None

    def allow_trading(self, timestamp, equity_now: float) -> bool:
        # Initialize daily start
        if (self.daily_start is None) or (timestamp.date() != self.daily_start[0]):
            self.daily_start = (timestamp.date(), equity_now)
        daily_dd = (equity_now / self.daily_start[1]) - 1.0
        total_dd = (equity_now / self.start_equity) - 1.0
        if daily_dd <= -abs(self.daily_limit): return False
        if total_dd <= -abs(self.total_limit): return False
        return True
