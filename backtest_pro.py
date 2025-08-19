import os
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data import load_data
from strategies import generate_signals
from utils import atr, adx, resample_higher, sharpe_ratio, freq_from_interval
from risk import position_size, CircuitBreaker
from positioning import PositionManager

RESULTS_DIR = "results"

def run_strategy(df: pd.DataFrame, name: str, stype: str, params: dict, cfg: dict):
    # --- Filters ---
    # ADX regime
    adx_vals = adx(df, cfg['filters']['adx_period'])
    mtf_enabled = cfg['filters']['mtf']['enabled']
    if mtf_enabled:
        ratio = cfg['filters']['mtf']['higher_interval_ratio']
        higher = resample_higher(df, ratio)
        ma = higher['Close'].rolling(cfg['filters']['mtf']['ma_period']).mean()
        ma = ma.reindex(df.index, method='nearest')
    else:
        ma = None

    # Base signals
    sig = generate_signals(df, stype, params)
    pos = sig['position'].copy().astype(int)

    # Apply regime: prefer trend when ADX high
    pos[(adx_vals < cfg['filters']['adx_trend_min']) & (stype in ('macd_trend','donchian_breakout'))] = 0
    # MTF filter: only long if price above higher MA
    if mtf_enabled and ma is not None:
        pos[df['Close'] < ma] = 0

    sig = pd.DataFrame({'position': pos}, index=df.index)
    return sig

def run_backtest(df: pd.DataFrame, signals: pd.DataFrame, initial_cash: float, commission_pct: float, slippage_pct: float, spread_pct: float, name: str, cfg: dict):
    close = df['Close']
    # Bid/Ask simulation
    ask = close * (1 + spread_pct/2)
    bid = close * (1 - spread_pct/2)

    position = signals['position'].fillna(0).astype(int)
    entries = (position.shift(1).fillna(0) == 0) & (position == 1)
    exits = (position.shift(1).fillna(0) == 1) & (position == 0)

    cash = initial_cash
    shares = 0.0
    equity = []
    last_entry_price = None
    in_trade = False

    # Risk tools
    atr_series = atr(df, cfg['risk']['atr_window'])
    cb = CircuitBreaker(pd.Series([initial_cash], index=[df.index[0]]), cfg['risk']['daily_dd_limit'], cfg['risk']['total_dd_limit'])
    trailing_mult = cfg['risk']['trailing_atr_mult']
    trailing_stop = None

    log_rows = []

    for i, ts in enumerate(close.index):
        price_bid = bid.iloc[i]
        price_ask = ask.iloc[i]
        equity_now = cash + shares * price_bid  # mark-to-bid
        if not cb.allow_trading(ts, equity_now):
            equity.append(equity_now)
            continue

        # trailing stop update
        if in_trade and trailing_mult and not np.isnan(atr_series.iloc[i]):
            trail = last_entry_price - trailing_mult * atr_series.iloc[i]
            trailing_stop = max(trailing_stop or trail, trail)

        # Exit logic (signal or trailing)
        if in_trade:
            exit_flag = False
            exit_reason = ""
            if trailing_stop and df['Low'].iloc[i] <= trailing_stop:
                px = max(trailing_stop, price_bid) * (1 - slippage_pct)
                exit_flag = True; exit_reason = "TRAILING"
            elif exits.iloc[i]:
                px = price_bid * (1 - slippage_pct)
                exit_flag = True; exit_reason = "SIGNAL"

            if exit_flag:
                trade_value = shares * px
                fee = abs(trade_value) * commission_pct
                cash += trade_value - fee
                pnl = trade_value - fee - (shares * last_entry_price)
                log_rows.append({
                    'bot_name': name, 'symbol':'FOREX', 'side':'SELL', 'open_time': last_ts, 'open_price': last_entry_price,
                    'close_time': ts, 'close_price': px, 'stop_loss': trailing_stop, 'take_profit': None, 'pnl': pnl
                })
                shares = 0.0; in_trade = False; last_entry_price = None; trailing_stop = None

        # Entry
        if entries.iloc[i] and (not in_trade):
            # position sizing
            size_value = position_size(cash, cfg['risk']['risk_per_trade'], atr_series.iloc[i])
            px = price_ask * (1 + slippage_pct)
            fee = size_value * commission_pct
            size_value_after_fee = max(size_value - fee, 0)
            qty = size_value_after_fee / px
            if qty > 0:
                shares = qty; cash -= shares * px + fee
                last_entry_price = px; last_ts = ts; in_trade = True
                trailing_stop = None
                log_rows.append({
                    'bot_name': name, 'symbol':'FOREX', 'side':'BUY', 'open_time': ts, 'open_price': px,
                    'close_time': None, 'close_price': None, 'stop_loss': None, 'take_profit': None, 'pnl': None
                })

        equity.append(cash + shares * price_bid)

    equity = pd.Series(equity, index=close.index, name='Equity')
    returns = equity.pct_change().fillna(0.0)
    metrics = {
        "Total Return": equity.iloc[-1]/equity.iloc[0]-1,
        "Sharpe": sharpe_ratio(returns, periods_per_year=252*24 if 'h' in cfg['interval'] else 252),
        "Max Drawdown": (equity / equity.cummax() - 1).min(),
        "Trades": sum(entries)
    }
    log_df = pd.DataFrame(log_rows)
    return equity, returns, metrics, log_df

def plot_equity(equity: pd.Series, name: str):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    equity.plot()
    plt.title(f"Equity Curve – {name}")
    plt.xlabel("Date"); plt.ylabel("Equity")
    plt.tight_layout()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(RESULTS_DIR, f"equity_{name}.png"))
    plt.close()

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    cfg = yaml.safe_load(open("config.yaml"))
    df = load_data(cfg['symbol'], cfg['interval'], cfg['start'], cfg['end'])

    all_metrics = []
    all_logs = []

    for bot_name, st in cfg['strategies'].items():
        sig = run_strategy(df.copy(), bot_name, st['type'], st['params'], cfg)
        equity, returns, metrics, log_df = run_backtest(df.copy(), sig, cfg['initial_cash'], cfg['commission_pct'], cfg['slippage_pct'], cfg['spread_pct'], bot_name, cfg)
        plot_equity(equity, bot_name)
        all_metrics.append({'Strategy': bot_name} | metrics)
        all_logs.append(log_df)

    summary = pd.DataFrame(all_metrics).set_index('Strategy')
    summary.to_csv(os.path.join(RESULTS_DIR, "summary.csv"))

    logs = pd.concat(all_logs, ignore_index=True)
    logs.to_csv(os.path.join(RESULTS_DIR, "trading_log.csv"), index=False)
    try:
        logs.to_excel(os.path.join(RESULTS_DIR, "trading_log.xlsx"), index=False)
    except Exception:
        pass

    print("Backtest PRO completato. Risultati in ./results/")

if __name__ == "__main__":
    main()
