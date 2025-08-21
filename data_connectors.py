"""
Connettori dati: Yahoo, OANDA (placeholder), Dukascopy CSV.
Scegli la sorgente da config e restituisci un DataFrame con colonne: Open, High, Low, Close, Volume (index datetime).
"""

import pandas as pd

def from_yahoo(symbol: str, interval: str, start: str, end: str | None) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(symbol, interval=interval, start=start, end=end, progress=False, auto_adjust=False)
    df = df[["Open","High","Low","Close","Volume"]].dropna()
    df.index = pd.to_datetime(df.index)
    return df

def from_dukascopy_csv(path: str, tz: str = "UTC") -> pd.DataFrame:
    df = pd.read_csv(path)
    # atteso: Date, Open, High, Low, Close, Volume
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(tz, nonexistent='shift_forward', ambiguous='NaT', errors='ignore')
    df = df.rename(columns={"Date":"Datetime"}).set_index("Datetime")
    df = df[["Open","High","Low","Close","Volume"]].dropna()
    return df

def from_oanda(api_key: str, account_type: str, instrument: str, granularity: str, start_iso: str, end_iso: str | None, price="M", batch=5000) -> pd.DataFrame:
    # Placeholder: implementare batch loop + paginazione
    try:
        import oandapyV20
        import oandapyV20.endpoints.instruments as instruments
    except Exception as e:
        raise RuntimeError("Installa oandapyV20 per usare il connettore OANDA") from e

    client = oandapyV20.API(access_token=api_key)
    params = {"granularity": granularity, "price": price, "count": batch, "from": start_iso}
    if end_iso: params["to"] = end_iso
    req = instruments.InstrumentsCandles(instrument=instrument, params=params)
    client.request(req)
    rows = []
    for c in req.response["candles"]:
        if not c["complete"]: continue
        rows.append([c["time"], float(c["mid"]["o"]), float(c["mid"]["h"]), float(c["mid"]["l"]), float(c["mid"]["c"]), int(c["volume"])])
    df = pd.DataFrame(rows, columns=["Date","Open","High","Low","Close","Volume"])
    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    df = df.set_index("Date")[["Open","High","Low","Close","Volume"]]
    return df
