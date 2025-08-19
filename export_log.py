import pandas as pd
import sys

def export_to_excel(csv_file="results/trading_log.csv", excel_file="results/trading_log.xlsx"):
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)
    print(f"Esportato {excel_file}")

if __name__ == "__main__":
    csvf = sys.argv[1] if len(sys.argv)>1 else "results/trading_log.csv"
    xlsx = sys.argv[2] if len(sys.argv)>2 else "results/trading_log.xlsx"
    export_to_excel(csvf, xlsx)
