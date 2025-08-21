import pandas as pd
import matplotlib.pyplot as plt
from metrics import sharpe_ratio, sortino_ratio, calmar_ratio, max_drawdown, profit_factor, turnover

def run_backtest(data: pd.DataFrame):
    data['returns'] = data['Close'].pct_change().fillna(0)
    data['equity_curve'] = (1 + data['returns']).cumprod()

    sharpe = sharpe_ratio(data['returns'])
    sortino = sortino_ratio(data['returns'])
    calmar = calmar_ratio(data['returns'], data['equity_curve'])
    mdd = max_drawdown(data['equity_curve'])

    gains = data.loc[data['returns'] > 0, 'returns']
    losses = data.loc[data['returns'] < 0, 'returns']
    pf = profit_factor(gains, losses)
    to = turnover(data['returns'])

    results = {
        'Sharpe': sharpe,
        'Sortino': sortino,
        'Calmar': calmar,
        'Max Drawdown': mdd,
        'Profit Factor': pf,
        'Turnover': to
    }
    return results, data

def generate_report(data: pd.DataFrame, results: dict, filename="backtest_report.xlsx"):
    writer = pd.ExcelWriter(filename, engine="openpyxl")
    pd.DataFrame([results]).to_excel(writer, sheet_name="Metrics", index=False)
    data.to_excel(writer, sheet_name="EquityCurve", index=False)
    writer.close()

    plt.plot(data['equity_curve'])
    plt.title("Equity Curve")
    plt.savefig("equity_curve.png")
    plt.close()
