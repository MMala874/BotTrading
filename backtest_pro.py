
import pandas as pd
import numpy as np
from metrics import calculate_metrics

def run_backtest(df, strategy="mean_reversion"):
    """
    Semplice motore di backtest su dati OHLC.
    Attualmente supporta strategia 'mean_reversion' o 'trend_following'.
    """
    df = df.copy()
    df['returns'] = df['close'].pct_change()

    if strategy == "mean_reversion":
        df['signal'] = np.where(df['close'] < df['close'].rolling(20).mean(), 1, -1)
    elif strategy == "trend_following":
        df['signal'] = np.where(df['close'] > df['close'].rolling(50).mean(), 1, -1)
    else:
        raise ValueError("Strategia non supportata")

    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    df.dropna(inplace=True)
    results = calculate_metrics(df)
    return results

def save_report(results, filename="report.xlsx"):
    """Salva i risultati e le metriche in un file Excel."""
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        results['df'].to_excel(writer, sheet_name="EquityCurve")
        pd.DataFrame(results['metrics'], index=[0]).to_excel(writer, sheet_name="Metrics")
