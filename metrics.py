import numpy as np

def compute_metrics(returns):
    sharpe = np.mean(returns) / (np.std(returns) + 1e-9)
    dd = max_drawdown(returns)
    turnover = np.sum(np.abs(np.diff(np.sign(returns))))

    return {
        "Sharpe": sharpe,
        "MaxDrawdown": dd,
        "Turnover": turnover
    }

def max_drawdown(returns):
    cumret = (1 + returns).cumprod()
    peak = cumret.expanding(min_periods=1).max()
    dd = (cumret - peak) / peak
    return dd.min()
