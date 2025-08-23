
from metrics_plus import ulcer_index, ulcer_performance_index, deflated_sharpe_ratio

def generate_report(equity_series, returns, sharpe:float, ann_return:float):
    ui = ulcer_index(equity_series)
    upi = ulcer_performance_index(ann_return, ui)
    dsr = deflated_sharpe_ratio(sharpe, n_trials=20, T=len(returns))
    return {
        "UlcerIndex": ui,
        "UlcerPerfIdx": upi,
        "DeflatedSharpe": dsr
    }
