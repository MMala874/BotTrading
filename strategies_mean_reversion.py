
import numpy as np
import pandas as pd

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = (delta.clip(lower=0)).ewm(alpha=1/period, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
    rs = up / (down.replace(0, np.nan))
    r = 100 - (100 / (1 + rs))
    return r.fillna(50)

def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["High"], df["Low"], df["Close"]
    tr1 = (high - low).abs()
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/period, adjust=False).mean()

    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    plus_di = 100 * (pd.Series(plus_dm, index=df.index).ewm(alpha=1/period, adjust=False).mean() / atr)
    minus_di = 100 * (pd.Series(minus_dm, index=df.index).ewm(alpha=1/period, adjust=False).mean() / atr)
    dx = ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)) * 100
    adx = dx.ewm(alpha=1/period, adjust=False).mean()
    return adx.fillna(0.0)

def mean_reversion_adx_rsi(df: pd.DataFrame, rsi_period:int=14, rsi_low:float=30, rsi_high:float=70, adx_period:int=14, adx_threshold:float=20) -> pd.DataFrame:
    """Entra long quando RSI<rsi_low e ADX<adx_threshold (regime di range); esce quando RSI>50.
    Entra short quando RSI>rsi_high e ADX<adx_threshold; esce quando RSI<50.
    Restituisce DataFrame con colonna 'position' (-1,0,+1).\"""
    r = rsi(df["Close"], rsi_period)
    a = adx(df, adx_period)
    regime_range = (a < adx_threshold)

    long_sig = (r < rsi_low) & regime_range
    short_sig = (r > rsi_high) & regime_range

    exit_long = (r > 50)
    exit_short = (r < 50)

    # propagate discrete positions with hold/exit logic
    current = 0.0
    out = []
    for ls, ss, el, es in zip(long_sig, short_sig, exit_long, exit_short):
        if ls:
            current = 1.0
        elif ss:
            current = -1.0
        else:
            if current == 1.0 and el:
                current = 0.0
            elif current == -1.0 and es:
                current = 0.0
        out.append(current)

    return pd.DataFrame({"position": pd.Series(out, index=df.index)})
