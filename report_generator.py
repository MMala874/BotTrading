import pandas as pd
from backtest_pro import run_backtest, generate_report

def main():
    data = pd.read_csv("sample_data.csv")
    results, enriched_data = run_backtest(data)
    print("Risultati:", results)
    generate_report(enriched_data, results)

if __name__ == "__main__":
    main()
