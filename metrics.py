
import numpy as np

def calculate_metrics(df):
    """Calcola Sharpe ratio, max drawdown, turnover."""
    returns = df['strategy_returns']
    sharpe = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0

    cum_returns = (1 + returns).cumprod()
    peak = cum_returns.cummax()
    dd = (cum_returns - peak) / peak
    max_dd = dd.min()

    turnover = (df['signal'].diff().abs().sum()) / len(df)

    metrics = {
        "SharpeRatio": sharpe,
        "MaxDrawdown": max_dd,
        "Turnover": turnover,
        "CumulativeReturn": cum_returns.iloc[-1] - 1
    }
    return {"df": df, "metrics": metrics}
