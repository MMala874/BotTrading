import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns, ddof=1)

def sortino_ratio(returns, risk_free_rate=0.0):
    downside = returns[returns < 0]
    if downside.std(ddof=1) == 0:
        return np.inf
    return (np.mean(returns) - risk_free_rate) / downside.std(ddof=1)

def calmar_ratio(returns, equity_curve):
    max_dd = max_drawdown(equity_curve)
    if max_dd == 0:
        return np.inf
    return np.mean(returns) / abs(max_dd)

def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max) / roll_max
    return drawdown.min()

def profit_factor(gains, losses):
    if abs(losses.sum()) == 0:
        return np.inf
    return gains.sum() / abs(losses.sum())

def turnover(trades):
    return len(trades)
