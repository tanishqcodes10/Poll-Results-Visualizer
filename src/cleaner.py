"""
cleaner.py
Loads raw poll CSV, validates, cleans, and returns a clean DataFrame.
"""
import pandas as pd

def load_and_clean(path="data/poll_data.csv"):
    df = pd.read_csv(path)
    print(f"[cleaner] Loaded {len(df)} rows, {df.shape[1]} columns")

    # 1. Type conversion
    df["date"]             = pd.to_datetime(df["date"], errors="coerce")
    df["response_time_sec"] = pd.to_numeric(df["response_time_sec"], errors="coerce")

    # 2. Strip whitespace from string columns
    for col in ["question","option_selected","region","age_group","gender"]:
        df[col] = df[col].str.strip()

    # 3. Drop rows missing critical fields
    before = len(df)
    df.dropna(subset=["option_selected","question","region","age_group"], inplace=True)
    print(f"[cleaner] Dropped {before - len(df)} invalid rows. Remaining: {len(df)}")

    # 4. Feature engineering: extract time dimensions
    df["month"]   = df["date"].dt.to_period("M").astype(str)
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)

    # 5. Clip extreme response times (within 3 std deviations)
    mu, sigma = df["response_time_sec"].mean(), df["response_time_sec"].std()
    df["response_time_sec"] = df["response_time_sec"].clip(mu - 3*sigma, mu + 3*sigma)

    return df

if __name__ == "__main__":
    df = load_and_clean()
    df.to_csv("data/poll_data_cleaned.csv", index=False)
    print("[cleaner] Saved → data/poll_data_cleaned.csv")