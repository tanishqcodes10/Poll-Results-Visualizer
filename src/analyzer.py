"""
analyzer.py
Vote share, regional breakdown, demographic breakdown,
monthly trend, NPS-style scoring, leading option detection.
"""
import pandas as pd

def vote_share(df, question):
    """Returns vote counts and % share per option."""
    sub    = df[df["question"] == question]
    counts = sub["option_selected"].value_counts()
    pct    = (counts / counts.sum() * 100).round(2)
    return pd.DataFrame({"votes": counts, "share_%": pct}).reset_index()\
             .rename(columns={"index":"option"})

def region_breakdown(df, question):
    """Pivot table: region × option → percentage."""
    sub   = df[df["question"] == question]
    pivot = sub.pivot_table(index="region", columns="option_selected",
                            aggfunc="size", fill_value=0)
    return pivot.div(pivot.sum(axis=1), axis=0).mul(100).round(1)

def demographic_breakdown(df, question, by="age_group"):
    """Pivot table: demographic dimension × option → percentage."""
    sub   = df[df["question"] == question]
    pivot = sub.pivot_table(index=by, columns="option_selected",
                            aggfunc="size", fill_value=0)
    return pivot.div(pivot.sum(axis=1), axis=0).mul(100).round(1)

def monthly_trend(df, question):
    """Monthly response counts per option."""
    sub         = df[df["question"] == question].copy()
    sub["month"] = pd.to_datetime(sub["date"]).dt.to_period("M").astype(str)
    return sub.pivot_table(index="month", columns="option_selected",
                           aggfunc="size", fill_value=0).reset_index()

def leading_option(df, question):
    """Returns (winning_option, share_%)."""
    shares = vote_share(df, question)
    top    = shares.loc[shares["share_%"].idxmax()]
    return top["option_selected"], top["share_%"]

def summary_insights(df):
    """Generates a printed text summary for all questions."""
    lines = []
    for q in df["question"].unique():
        winner, pct = leading_option(df, q)
        n           = len(df[df["question"] == q])
        lines.append(f"Q: {q}")
        lines.append(f"   → Leading: '{winner}' with {pct}% ({n} total responses)")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    df = pd.read_csv("data/poll_data_cleaned.csv")
    print(summary_insights(df))