import pandas as pd
import numpy as np
from metrics import compute_metrics

def run_backtest(df, strategy="mean_reversion"):
    """
    Esegue un backtest semplice su dati storici.

    Args:
        df (pd.DataFrame): Dati OHLCV.
        strategy (str): Nome strategia ("mean_reversion", "momentum").

    Returns:
        dict con metriche e risultati.
    """
    df = df.copy()
    df["Return"] = df["Close"].pct_change()
    
    if strategy == "mean_reversion":
        df["Signal"] = -np.sign(df["Return"].rolling(5).mean())
    elif strategy == "momentum":
        df["Signal"] = np.sign(df["Return"].rolling(5).mean())
    else:
        raise ValueError("Strategia non supportata")
    
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Return"]
    cumret = (1 + df["Strategy_Return"]).cumprod()
    
    metrics = compute_metrics(df["Strategy_Return"].dropna())
    
    return {
        "cumulative_return": cumret.iloc[-1],
        "metrics": metrics,
        "history": df
    }
