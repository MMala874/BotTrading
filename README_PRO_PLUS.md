
# Pro Features Extension

## Dynamic Spread/Slippage
`execution_utils.py` provides `dynamic_spread_slippage()` to adjust execution costs by session (Asia/London/NY).

## Time-of-Day Filter
`filters_time.py` has `allow_trade_time()` to restrict signals to desired trading hours.

## Currency Exposure Control
`orchestrator.py` includes `check_currency_exposure()` to aggregate exposure by currency and flag violations.

## Advanced Metrics
`report_generator.py` now computes Ulcer Index, Ulcer Performance Index, Deflated Sharpe Ratio.

## Config Additions (example)
```yaml
risk:
  daily_dd_limit: 0.05
  total_dd_limit: 0.2
  max_currency_exposure: 0.3

execution:
  mode: dynamic   # or fixed
  allowed_hours: [7,20]
```


## Novità integrate
- **Filtro time-of-day**: `trading_hours` nel config, applicato in orchestrator.
- **Limite exposure per currency**: `max_currency_exposure` gestito da PositionManager.
- **Costi dinamici per sessione**: utility in `execution_utils.py` (integrazione esecuzione/backtest da adattare al tuo motore).
