# Trading Bots PRO+ – Upgrade Pack

Questo pacchetto aggiunge cinque cose richieste **prima del backtesting definitivo**:
1) **Strategie logiche e spiegabili** (razionale chiaro, parametri trasparenti).
2) **Connettori dati solidi**: Yahoo, OANDA (placeholder API), Dukascopy CSV.
3) **Backtest robusto con metriche avanzate**: Sharpe, Sortino, Calmar, MaxDD, Turnover, Profit Factor, Hit Rate, Avg Win/Loss.
4) **Execution layer** astratto + **OANDA broker** (paper/live switch) – skeleton pronto per collegare ordini reali.
5) **Test di robustezza & monitoraggio**: Walk‑Forward, Monte Carlo, Telegram alerts e heartbeat.

> Nota: file in stile “skeleton” dove indicato: completare chiavi/API e mapping ordini prima dell’uso live.


## Nuova strategia: mean_reversion_adx_rsi
- Tipo: `mean_reversion_adx_rsi`
- Parametri: `rsi_period`, `rsi_low`, `rsi_high`, `adx_period`, `adx_threshold`

Esempio config:

```
strategies:
  MR_RSI:
    type: "mean_reversion_adx_rsi"
    params: { rsi_period: 14, rsi_low: 30, rsi_high: 70, adx_period: 14, adx_threshold: 20 }
```
