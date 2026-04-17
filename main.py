"""
main.py  ─  Poll Results Visualizer
Run:  python main.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_generator import generate_poll_data
from cleaner        import load_and_clean
from analyzer       import summary_insights
from visualizer     import (bar_chart, pie_chart, stacked_bar_region,
                            demographic_heatmap, trend_chart)

print("=" * 60)
print("         POLL RESULTS VISUALIZER")
print("=" * 60)

# Step 1: Generate data (skip if already exists)
csv_path = "data/poll_data.csv"
if not os.path.exists(csv_path):
    print("\n[1] Generating synthetic poll data…")
    df_raw = generate_poll_data(n=500)
    os.makedirs("data", exist_ok=True)
    df_raw.to_csv(csv_path, index=False)
    print(f"    Saved {len(df_raw)} rows → {csv_path}")
else:
    print(f"\n[1] Dataset found at {csv_path}. Skipping generation.")

# Step 2: Clean
print("\n[2] Cleaning data…")
df = load_and_clean(csv_path)
df.to_csv("data/poll_data_cleaned.csv", index=False)
print(f"    Clean dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# Step 3: Insights
print("\n[3] Summary Insights:")
print(summary_insights(df))

# Step 4: Visualize all questions
print("[4] Generating all charts…")
os.makedirs("outputs", exist_ok=True)
for q in df["question"].unique():
    bar_chart(df, q)
    pie_chart(df, q)
    stacked_bar_region(df, q)
    demographic_heatmap(df, q, by="age_group")
    trend_chart(df, q)

print("\n✅ All 25 charts saved to outputs/")
print("   Run:  streamlit run app_dashboard.py  for the dashboard")
print("=" * 60)