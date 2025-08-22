import pandas as pd
from dukascopy import Downloader

def get_data_dukascopy(symbol="EURUSD", 
                       start="2015-01-01", 
                       end="2020-01-01", 
                       timeframe="1h"):
    """
    Scarica dati Forex da Dukascopy.

    Args:
        symbol (str): Coppia valutaria, es. "EURUSD".
        start (str): Data inizio (YYYY-MM-DD).
        end (str): Data fine (YYYY-MM-DD).
        timeframe (str): "tick", "1m", "5m", "15m", "1h", "1d".

    Returns:
        pd.DataFrame con [Date, Open, High, Low, Close, Volume].
    """
    dl = Downloader()
    df = dl.get(symbol, start, end, timeframe)
    return df

if __name__ == "__main__":
    data = get_data_dukascopy("EURUSD", "2018-01-01", "2019-01-01", "1h")
    print(data.head())
    print(data.tail())
