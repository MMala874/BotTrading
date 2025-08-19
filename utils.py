import numpy as np
import pandas as pd

def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    h, l, c = df['High'], df['Low'], df['Close']
    tr1 = h - l
    tr2 = (h - c.shift()).abs()
    tr3 = (l - c.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(n).mean().fillna(method='bfill')

def adx(df: pd.DataFrame, n: int = 14) -> pd.Series:
    high, low, close = df['High'], df['Low'], df['Close']
    plus_dm = high.diff().clip(lower=0)
    minus_dm = (-low.diff()).clip(lower=0)
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_n = tr.rolling(n).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/n, adjust=False).mean() / atr_n)
    minus_di = 100 * (minus_dm.ewm(alpha=1/n, adjust=False).mean() / atr_n)
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.ewm(alpha=1/n, adjust=False).mean().fillna(0)

def resample_higher(df: pd.DataFrame, ratio: int) -> pd.DataFrame:
    # Funziona per intervalli uniformi (es. 1h). Usa rolling window per simulare timeframe superiore.
    return df.rolling(ratio, min_periods=1).agg({
        'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'
    })

def sharpe_ratio(returns: pd.Series, periods_per_year: int) -> float:
    mu = returns.mean() * periods_per_year
    sigma = returns.std(ddof=1) * (periods_per_year ** 0.5)
    return mu / sigma if sigma > 0 else float('nan')

def freq_from_interval(interval: str) -> int:
    if interval == "1d": return 252
    if interval in ("1h","60m"): return 24*252
    if interval in ("15m","5m","1m"): return 26*252* (60 // int(interval.replace('m','')))
    return 252
