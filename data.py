import pandas as pd
import yfinance as yf

def load_data(symbol: str, interval: str, start: str, end: str | None) -> pd.DataFrame:
    df = yf.download(symbol, interval=interval, start=start, end=end, progress=False, auto_adjust=False)
    if df.empty:
        raise ValueError(f"Nessun dato trovato per {symbol} con intervallo {interval}.")
    df = df[['Open','High','Low','Close','Volume']].dropna()
    df.index = pd.to_datetime(df.index)
    return df
