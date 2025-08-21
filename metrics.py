"""
Metriche avanzate per valutare le strategie.
"""

import numpy as np
import pandas as pd

def max_drawdown(equity: pd.Series) -> float:
    roll_max = equity.cummax()
    dd = equity / roll_max - 1.0
    return float(dd.min())

def sharpe(returns: pd.Series, periods_per_year=252) -> float:
    mu = returns.mean() * periods_per_year
    sd = returns.std(ddof=1) * np.sqrt(periods_per_year)
    return float(mu / sd) if sd > 0 else float("nan")

def sortino(returns: pd.Series, periods_per_year=252) -> float:
    downside = returns.clip(upper=0)
    dr = downside.std(ddof=1) * np.sqrt(periods_per_year)
    mu = returns.mean() * periods_per_year
    return float(mu / dr) if dr > 0 else float("nan")

def calmar(equity: pd.Series, returns: pd.Series, periods_per_year=252) -> float:
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (periods_per_year / len(equity)) - 1
    mdd = abs(max_drawdown(equity))
    return float(cagr / mdd) if mdd > 0 else float("nan")

def turnover(signals: pd.Series) -> float:
    # proxy: numero di cambi di stato / n
    changes = (signals != signals.shift()).sum()
    return float(changes) / max(len(signals), 1)

def trade_stats(trades_df: pd.DataFrame) -> dict:
    closed = trades_df.dropna(subset=["close_price"])
    wins = (closed["pnl"] > 0).sum()
    losses = (closed["pnl"] <= 0).sum()
    hit_rate = wins / max(wins + losses, 1)
    avg_win = closed.loc[closed["pnl"] > 0, "pnl"].mean()
    avg_loss = closed.loc[closed["pnl"] <= 0, "pnl"].mean()
    profit_factor = (closed.loc[closed["pnl"] > 0, "pnl"].sum()) / abs(closed.loc[closed["pnl"] <= 0, "pnl"].sum()) if losses>0 else float("inf")
    return {
        "HitRate": float(hit_rate),
        "AvgWin": float(avg_win) if pd.notna(avg_win) else 0.0,
        "AvgLoss": float(avg_loss) if pd.notna(avg_loss) else 0.0,
        "ProfitFactor": float(profit_factor),
    }
