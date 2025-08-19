import yaml
import pandas as pd
from data import load_data
from strategies import generate_signals
from positioning import PositionManager
from backtest_pro import run_backtest, run_strategy, plot_equity, RESULTS_DIR

def orchestrate():
    cfg = yaml.safe_load(open("config.yaml"))
    df = load_data(cfg['symbol'], cfg['interval'], cfg['start'], cfg['end'])
    pm = PositionManager(policy=cfg['conflict_policy'], bot_priority=cfg.get('bot_priority', []))

    all_logs = []; all_metrics = []

    for bot_name in cfg['strategies']:
        st = cfg['strategies'][bot_name]
        sig = run_strategy(df.copy(), bot_name, st['type'], st['params'], cfg)

        # Enforce conflicts at signal level: zero out entries that violate policy
        position = 0
        filtered = sig['position'].copy().astype(int)
        for i, ts in enumerate(filtered.index):
            side = "BUY" if filtered.iloc[i]==1 else None
            if side and not pm.can_open(cfg['symbol'], bot_name, side):
                filtered.iloc[i] = 0
            elif side:
                pm.register_open(cfg['symbol'], bot_name, side)
            else:
                pm.register_close(cfg['symbol'], bot_name)
        sig['position'] = filtered

        equity, returns, metrics, log_df = run_backtest(df.copy(), sig, cfg['initial_cash'], cfg['commission_pct'], cfg['slippage_pct'], cfg['spread_pct'], bot_name, cfg)
        plot_equity(equity, bot_name)
        all_metrics.append({'Strategy': bot_name} | metrics); all_logs.append(log_df)

    summary = pd.DataFrame(all_metrics).set_index('Strategy')
    summary.to_csv(f"{RESULTS_DIR}/summary.csv")
    logs = pd.concat(all_logs, ignore_index=True)
    logs.to_csv(f"{RESULTS_DIR}/trading_log.csv", index=False)
    try:
        logs.to_excel(f"{RESULTS_DIR}/trading_log.xlsx", index=False)
    except Exception:
        pass
    print("Orchestrazione completata. Vedi cartella results.")

if __name__ == "__main__":
    orchestrate()
