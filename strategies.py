import numpy as np
import pandas as pd

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = (delta.clip(lower=0)).ewm(alpha=1/period, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
    rs = up / (down.replace(0, np.nan))
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def sma(series: pd.Series, n:int) -> pd.Series:
    return series.rolling(n).mean()

def macd_trend(df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
    close = df['Close']
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    pos = (macd > sig).astype(int)
    return pd.DataFrame({'position': pos}, index=df.index)

def rsi_mean_reversion(df: pd.DataFrame, period=14, low=30, high=70) -> pd.DataFrame:
    r = rsi(df['Close'], period)
    pos = ((r < low).astype(int) - (r > high).astype(int)).clip(lower=0)
    return pd.DataFrame({'position': pos}, index=df.index)

def bollinger_reversion(df: pd.DataFrame, period=20, num_std=2.0) -> pd.DataFrame:
    close = df['Close']
    ma = close.rolling(period).mean()
    std = close.rolling(period).std(ddof=0)
    lower = ma - num_std*std
    pos = (close < lower).astype(int)
    return pd.DataFrame({'position': pos}, index=df.index)

def donchian_breakout(df: pd.DataFrame, window=55, exit_window=20) -> pd.DataFrame:
    high = df['High'].rolling(window).max()
    breakout = (df['Close'] > high.shift(1)).astype(int)
    exit_long = (df['Close'] < df['Low'].rolling(exit_window).min().shift(1)).astype(int)
    pos = breakout.copy()
    pos[exit_long == 1] = 0
    return pd.DataFrame({'position': pos}, index=df.index)

def generate_signals(df: pd.DataFrame, strategy_type: str, params: dict) -> pd.DataFrame:
    if strategy_type == "macd_trend":
        return macd_trend(df, **params)
    if strategy_type == "rsi_mean_reversion":
        return rsi_mean_reversion(df, **params)
    if strategy_type == "bollinger_reversion":
        return bollinger_reversion(df, **params)
    if strategy_type == "donchian_breakout":
        return donchian_breakout(df, **params)
    raise ValueError(f"Strategia non riconosciuta: {strategy_type}")
