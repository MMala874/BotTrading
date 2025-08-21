"""
Strategie logiche e spiegabili.
Ogni strategia espone:
- name: nome leggibile
- rationale: testo breve che spiega la logica
- parameters: dizionario di parametri chiave
- signal(df): funzione che restituisce una serie 'position' (1 long, 0 flat)
"""

import pandas as pd

def _sma(series, n):
    return series.rolling(n).mean()

def _rsi(series, n=14):
    delta = series.diff()
    up = (delta.clip(lower=0)).ewm(alpha=1/n, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / (down.replace(0, pd.NA))
    return 100 - (100/(1+rs))

class SMACrossover:
    name = "SMA Crossover (Trend-Following)"
    rationale = "Compra quando la media breve supera la media lunga: si punta a cavalcare trend direzionali."
    parameters = {"fast": 20, "slow": 50}

    def __init__(self, fast=20, slow=50):
        self.fast, self.slow = fast, slow

    def signal(self, df: pd.DataFrame) -> pd.DataFrame:
        fast_ma = _sma(df["Close"], self.fast)
        slow_ma = _sma(df["Close"], self.slow)
        pos = (fast_ma > slow_ma).astype(int)
        return pd.DataFrame({"position": pos}, index=df.index)

class RSI_MeanReversion:
    name = "RSI Mean Reversion"
    rationale = "Compra quando RSI è ipervenduto: si assume rimbalzo verso la media."
    parameters = {"period": 14, "oversold": 30, "overbought": 70}

    def __init__(self, period=14, oversold=30, overbought=70):
        self.period, self.oversold, self.overbought = period, oversold, overbought

    def signal(self, df: pd.DataFrame) -> pd.DataFrame:
        rsi = _rsi(df["Close"], self.period)
        pos = (rsi < self.oversold).astype(int)
        # opzionale: chiusura quando rsi torna sopra 50
        return pd.DataFrame({"position": pos}, index=df.index)
