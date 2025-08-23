
from __future__ import annotations
import pandas as pd

def session_from_hour(hour: int) -> str:
    # Semplice partizione oraria (UTC): Asia 00-07, London 07-15, NewYork 12-21, Off altrimenti
    if 0 <= hour < 7:
        return "Asia"
    if 7 <= hour < 12:
        return "London"
    if 12 <= hour < 21:
        return "NewYork"
    return "Off"

def dynamic_costs(timestamp: pd.Timestamp, base_spread: float, base_slippage: float, session_multipliers: dict[str,float] | None = None) -> tuple[float,float]:
    session = session_from_hour(int(timestamp.hour))
    mult = (session_multipliers or {}).get(session, 1.0)
    return base_spread * mult, base_slippage * mult
