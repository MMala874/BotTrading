import pandas as pd

def load_news(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    if 'timestamp' not in df.columns:
        raise ValueError("CSV news deve avere colonna 'timestamp'")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if 'impact' not in df.columns:
        df['impact'] = 'high'
    return df

def blackout_mask(index, news_df: pd.DataFrame, before_min: int, after_min: int, impact_levels: list[str]) -> pd.Series:
    if news_df is None or news_df.empty:
        return pd.Series(False, index=index)
    news_df = news_df[news_df['impact'].str.lower().isin([i.lower() for i in impact_levels])]
    mask = pd.Series(False, index=index)
    for ts in news_df['timestamp']:
        start = ts - pd.Timedelta(minutes=before_min)
        end = ts + pd.Timedelta(minutes=after_min)
        mask |= (index >= start) & (index <= end)
    return mask
