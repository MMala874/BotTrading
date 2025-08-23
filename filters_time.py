
from __future__ import annotations
import pandas as pd

def _in_window(ts, start_str: str, end_str: str) -> bool:
    h, m = map(int, start_str.split(":"))
    hs, ms = h, m
    h, m = map(int, end_str.split(":"))
    he, me = h, m
    t = ts.time()
    return (t >= pd.Timestamp(hour=hs, minute=ms).time()) and (t <= pd.Timestamp(hour=he, minute=me).time())

def allowed_trading_window(index: pd.DatetimeIndex, windows: list[dict]) -> pd.Series:
    """
    windows es.: [ {"start":"07:00","end":"22:00","weekdays":[1,2,3,4,5]} ]
    Ritorna una Series booleana stessa lunghezza dell'index.
    Nota: assume timestamps già nella timezone operativa (es. UTC).
    """
    if not isinstance(index, pd.DatetimeIndex):
        index = pd.DatetimeIndex(index)
    mask = pd.Series(False, index=index)
    for w in windows or []:
        wd = set(w.get("weekdays", [1,2,3,4,5]))
        s = w.get("start","00:00")
        e = w.get("end","23:59")
        cond = index.to_series().apply(lambda ts: (ts.isoweekday() in wd) and _in_window(ts, s, e))
        mask = mask | cond
    return mask
