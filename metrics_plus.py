
import numpy as np
import pandas as pd

def ulcer_index(equity: pd.Series) -> float:
    """Ulcer Index basato su drawdown percentuale. equity: serie dell'equity cumulativa (valore o indice base=1).\"""
    ec = equity.astype(float)
    peak = ec.cummax()
    dd = 100.0 * (ec - peak) / peak.replace(0, np.nan)
    return float(np.sqrt(np.nanmean(dd**2)))

def ulcer_performance_index(annual_return: float, ui: float) -> float:
    if ui == 0 or np.isnan(ui):
        return np.nan
    return annual_return / ui

def deflated_sharpe_ratio(sharpe: float, n_trials: int, T: int) -> float:
    """Approximate DSR per Bailey et al. using simple noise max-sr adjustment.\"""
    if T <= 1:
        return np.nan
    import numpy as np
    if n_trials <= 1:
        return sharpe
    import math
    z = (np.sqrt(2*np.log(n_trials)) - (np.log(np.log(n_trials)) + np.log(4*np.pi)) / (2*np.sqrt(2*np.log(n_trials))))
    return sharpe - z / np.sqrt(T)
