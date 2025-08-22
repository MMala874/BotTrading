
from data_feed import get_data_dukascopy
# Qui supponiamo di avere già backtest_pro.py con run_backtest e save_report

from backtest_pro import run_backtest, save_report
from dukascopy_python.instruments import INSTRUMENT_FX_MAJORS_EUR_USD
from dukascopy_python import INTERVAL_HOUR_1

df = get_data_dukascopy(
    symbol=INSTRUMENT_FX_MAJORS_EUR_USD,
    start="2018-01-01",
    end="2022-01-01",
    interval=INTERVAL_HOUR_1
)

results = run_backtest(df, strategy="mean_reversion")
save_report(results, "report.xlsx")
print("Backtest completato. Report salvato in report.xlsx")
