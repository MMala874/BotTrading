import pandas as pd

def save_report(results, filename="report.xlsx"):
    df = results["history"]
    metrics = results["metrics"]
    df.to_excel(filename, index=False)
    print(f"Report salvato in {filename}")
    print("Metriche:", metrics)
