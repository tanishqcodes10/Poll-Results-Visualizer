"""
visualizer.py
All chart functions using Matplotlib/Seaborn.
Each function saves a PNG to outputs/ and returns the figure.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)

# Project color palette (teal-led, professional)
PALETTE = ["#01696f","#5591c7","#da7101","#a86fdf",
           "#6daa45","#dd6974","#e8af34","#d163a7"]

sns.set_theme(style="whitegrid", font_scale=1.1)

# ── 1. HORIZONTAL BAR CHART ──────────────────────────────────────────────────
def bar_chart(df, question, save=True):
    sub = df[df["question"] == question]["option_selected"].value_counts()
    pct = (sub / sub.sum() * 100).sort_values()

    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(pct.index, pct.values,
                   color=PALETTE[:len(pct)], edgecolor="white", height=0.6)

    for bar, val in zip(bars, pct.values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=10)

    ax.set_xlabel("Vote Share (%)")
    ax.set_title(question, fontsize=13, fontweight="bold", pad=10)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()

    if save:
        fname = f"outputs/bar_{question[:20].replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig

# ── 2. DONUT / PIE CHART ─────────────────────────────────────────────────────
def pie_chart(df, question, save=True):
    sub = df[df["question"] == question]["option_selected"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        sub.values, labels=None,          # use legend instead of labels
        colors=PALETTE[:len(sub)],
        autopct="%1.1f%%", startangle=140,
        pctdistance=0.78,
        wedgeprops=dict(edgecolor="white", linewidth=2.5)
    )
    for t in autotexts:
        t.set_fontsize(10); t.set_color("white"); t.set_fontweight("bold")

    ax.legend(sub.index, loc="lower center", ncol=2,
              bbox_to_anchor=(0.5, -0.08), fontsize=10)
    ax.set_title(question, fontsize=13, fontweight="bold", pad=16)
    plt.tight_layout()

    if save:
        fname = f"outputs/pie_{question[:20].replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig

# ── 3. STACKED BAR — REGION-WISE ─────────────────────────────────────────────
def stacked_bar_region(df, question, save=True):
    sub   = df[df["question"] == question]
    pivot = sub.pivot_table(index="region", columns="option_selected",
                            aggfunc="size", fill_value=0)
    pct   = pivot.div(pivot.sum(axis=1), axis=0).mul(100)

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom  = pd.Series([0.0]*len(pct), index=pct.index)
    for i, col in enumerate(pct.columns):
        ax.bar(pct.index, pct[col], bottom=bottom,
               color=PALETTE[i % len(PALETTE)], label=col, edgecolor="white")
        bottom += pct[col]

    ax.set_ylabel("Share (%)")
    ax.set_title(f"Region-wise: {question}", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.8,
              bbox_to_anchor=(1.18, 1))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()

    if save:
        fname = f"outputs/region_{question[:20].replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig

# ── 4. DEMOGRAPHIC HEATMAP ───────────────────────────────────────────────────
def demographic_heatmap(df, question, by="age_group", save=True):
    sub   = df[df["question"] == question]
    pivot = sub.pivot_table(index=by, columns="option_selected",
                            aggfunc="size", fill_value=0)
    pct   = pivot.div(pivot.sum(axis=1), axis=0).mul(100).round(1)

    fig, ax = plt.subplots(figsize=(11, 4))
    sns.heatmap(pct, annot=True, fmt=".1f", cmap="YlGn",
                linewidths=0.5, ax=ax,
                cbar_kws={"label":"Share %", "shrink":0.8},
                vmin=0, vmax=pct.values.max())

    ax.set_title(f"{by.replace('_',' ').title()}-wise: {question}",
                 fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel(""); ax.set_ylabel(by.replace("_"," ").title())
    plt.tight_layout()

    if save:
        fname = f"outputs/heatmap_{by}_{question[:15].replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig

# ── 5. MONTHLY TREND LINE ────────────────────────────────────────────────────
def trend_chart(df, question, save=True):
    sub         = df[df["question"] == question].copy()
    sub["month"] = pd.to_datetime(sub["date"]).dt.to_period("M").astype(str)
    trend        = sub.pivot_table(index="month", columns="option_selected",
                                   aggfunc="size", fill_value=0).reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, col in enumerate([c for c in trend.columns if c != "month"]):
        ax.plot(trend["month"], trend[col], marker="o",
                linewidth=2.5, color=PALETTE[i % len(PALETTE)], label=col)

    ax.set_xlabel("Month"); ax.set_ylabel("Responses")
    ax.set_title(f"Monthly Trend: {question}", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left", framealpha=0.8)
    ax.tick_params(axis="x", rotation=45)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()

    if save:
        fname = f"outputs/trend_{question[:20].replace(' ','_')}.png"
        fig.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig

# ── RUN ALL ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = pd.read_csv("data/poll_data_cleaned.csv")
    for q in df["question"].unique():
        bar_chart(df, q)
        pie_chart(df, q)
        stacked_bar_region(df, q)
        demographic_heatmap(df, q)
        trend_chart(df, q)
    print(f"✅ All charts saved to outputs/")