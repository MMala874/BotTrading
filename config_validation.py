
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, Literal
from datetime import datetime

class StrategyConfig(BaseModel):
    type: Literal["macd_trend","rsi_mean_reversion","bollinger_reversion","donchian_breakout","mean_reversion_adx_rsi"]
    params: Dict[str, Any] = {}

class Filters(BaseModel):
    adx_period: int = 14
    adx_trend_min: float = 20

class Risk(BaseModel):
    daily_dd_limit: float = 0.05
    total_dd_limit: float = 0.2

class Execution(BaseModel):
    spread: float = 0.0002
    slippage: float = 0.0001

class Config(BaseModel):
    symbol: str
    interval: str
    start: str
    end: str
    conflict_policy: Literal["netting","block_opposite","allow"] = "netting"
    bot_priority: Optional[list[str]] = None
    strategies: Dict[str, StrategyConfig]
    filters: Filters = Filters()
    risk: Risk = Risk()
    execution: Execution = Execution()

    @validator("start","end")
    def valid_date(cls, v):
        datetime.fromisoformat(v)
        return v
