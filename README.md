# Trading Bots PRO (Forex) – multi-bot, risk, trailing, MTF, news filter

Questo pacchetto implementa i miglioramenti richiesti:
- ✅ **Log book per bot** (CSV + export in Excel)
- ✅ **Evitare accavallamenti nocivi** (PositionManager con regole di conflitto)
- ✅ **Sizing dinamico** basato su volatilità (ATR-like) e rischio per trade
- ✅ **Trailing stop** dinamico
- ✅ **Circuit breaker** su drawdown giornaliero e totale
- ✅ **Filtro regime** (ADX) e **conferma Multi‑Timeframe** (MA su timeframe superiore)
- ✅ **Filtro eventi macro** via CSV (es. calendario economico)
- ✅ **Spread/commissioni/slippage** specifici Forex
- ✅ **Orchestratore multi-bot** (stesso mercato) con priorità bot

> ⚠️ Educativo. Nessuna garanzia di profitto. Testate solo in **demo**.

## Requisiti
```bash
pip install -r requirements.txt
```

## Configurazione rapida
Modificate `config.yaml`:
- `symbol`: es. `EURUSD=X` (Yahoo) oppure `GBPUSD=X`
- `interval`: `1h` o `1d` (per Forex consigliato `1h`)
- `initial_cash`, `commission_pct`, `slippage_pct`, `spread_pct`
- `risk` -> `risk_per_trade`, `daily_dd_limit`, `total_dd_limit`
- `conflict_policy`: `block_opposite` (default) | `netting` | `allow`
- `news_filter.csv_path`: file CSV opzionale con eventi macro (es. `news_events.csv`)

## Esecuzione
Esegui **tutti i bot** e genera log + report:
```bash
python orchestrator.py
```
Oppure solo backtest su dati storici (Yahoo):
```bash
python backtest_pro.py
```

## Output
- `results/trading_log.csv` – log dettagliato di ogni trade con `bot_name`
- `results/trading_log.xlsx` – export Excel
- `results/summary.csv` – metriche per bot
- `results/equity_<bot>.png` – equity curve

## Note su news filter
Create un CSV con colonne: `timestamp,impact,currency,title`. Esempio:
```
2025-08-20 12:30:00,high,USD,CPI m/m
2025-08-21 13:45:00,high,EUR,ECB Rate Decision
```
Impostate `news_filter.enabled: true` e `blackout_minutes_before/after` nel `config.yaml`.
