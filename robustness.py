"""
Test di robustezza: Walk-Forward e Monte Carlo.
"""

import numpy as np
import pandas as pd

def walk_forward(df, strategy_factory, param_grid, n_splits=6):
    """
    strategy_factory: funzione che crea una strategia: lambda params -> strategy_instance
    param_grid: lista di dizionari parametri
    Restituisce performance out-of-sample concatenata su tutte le finestre.
    """
    splits = np.array_split(df, n_splits)
    oos_results = []
    for i in range(len(splits)-1):
        train = pd.concat(splits[:i+1])
        test = splits[i+1]
        best_params, best_score = None, -1e9
        for p in param_grid:
            strat = strategy_factory(p)
            sig = strat.signal(train)
            ret = train["Close"].pct_change().fillna(0) * sig["position"].shift().fillna(0)
            score = ret.sum()  # semplice; sostituire con Sharpe o altro
            if score > best_score:
                best_params, best_score = p, score
        # test con best_params
        best = strategy_factory(best_params)
        sig_oos = best.signal(test)
        oos_ret = test["Close"].pct_change().fillna(0) * sig_oos["position"].shift().fillna(0)
        oos_results.append(oos_ret)
    return pd.concat(oos_results)

def monte_carlo(returns: pd.Series, n=1000, seed=42):
    rng = np.random.default_rng(seed)
    sims = []
    arr = returns.dropna().values
    for _ in range(n):
        # bootstrap con rimpiazzo
        sample = rng.choice(arr, size=len(arr), replace=True)
        sims.append(sample.cumsum()[-1])
    return np.array(sims)
