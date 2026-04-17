"""
app_dashboard.py  ─  Streamlit Interactive Dashboard
Run:  streamlit run app_dashboard.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys

sys.path.insert(0, "src")
from analyzer import vote_share, leading_option

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Poll Results Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

PALETTE = ["#01696f","#5591c7","#da7101","#a86fdf",
           "#6daa45","#dd6974","#e8af34","#d163a7"]

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = "data/poll_data_cleaned.csv"
    if not os.path.exists(path):
        path = "data/poll_data.csv"
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🗳️ Poll Visualizer")
questions = df["question"].unique().tolist()
selected_q = st.sidebar.selectbox("📋 Select Question", questions)

region_filter = st.sidebar.multiselect(
    "🌍 Filter by Region",
    df["region"].unique().tolist(),
    default=df["region"].unique().tolist())

age_filter = st.sidebar.multiselect(
    "👥 Filter by Age Group",
    df["age_group"].unique().tolist(),
    default=df["age_group"].unique().tolist())

# Apply filters
filtered = df[
    df["region"].isin(region_filter) &
    df["age_group"].isin(age_filter)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 Poll Results Visualizer")
st.markdown(f"**Active Question:** _{selected_q}_")
st.divider()

# ── KPI Row ───────────────────────────────────────────────────────────────────
sub = filtered[filtered["question"] == selected_q]
winner, pct = leading_option(filtered, selected_q)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Responses",  f"{len(sub):,}")
c2.metric("Leading Option",   winner)
c3.metric("Leading Share",    f"{pct:.1f}%")
c4.metric("Options Available", sub["option_selected"].nunique())

st.divider()

# ── Row 1: Bar + Donut ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Vote Share — Bar")
    vs = vote_share(filtered, selected_q)
    fig = px.bar(vs, x="share_%", y="option_selected",
                 orientation="h", color="option_selected",
                 color_discrete_sequence=PALETTE,
                 text="share_%",
                 labels={"share_%":"Share (%)","option_selected":""})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, height=320,
                      margin=dict(l=0,r=40,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Vote Share — Donut")
    fig2 = px.pie(vs, values="votes", names="option_selected",
                  color_discrete_sequence=PALETTE, hole=0.45)
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                       showlegend=True,
                       legend=dict(orientation="h",y=-0.1))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Region Stacked + Age Heatmap ──────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Region-wise Breakdown")
    pivot_r = sub.pivot_table(index="region",
                              columns="option_selected",
                              aggfunc="size", fill_value=0)
    pct_r = pivot_r.div(pivot_r.sum(axis=1),axis=0).mul(100).round(1).reset_index()
    options = [c for c in pct_r.columns if c != "region"]
    fig3 = go.Figure()
    for i, opt in enumerate(options):
        fig3.add_trace(go.Bar(name=opt, x=pct_r["region"],
                              y=pct_r[opt],
                              marker_color=PALETTE[i % len(PALETTE)]))
    fig3.update_layout(barmode="stack", height=320,
                       yaxis_title="Share (%)",
                       margin=dict(l=0,r=0,t=10,b=0),
                       legend=dict(orientation="h",y=-0.2))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Age-Group Heatmap")
    pivot_a = sub.pivot_table(index="age_group",
                              columns="option_selected",
                              aggfunc="size", fill_value=0)
    pct_a = pivot_a.div(pivot_a.sum(axis=1),axis=0).mul(100).round(1)
    fig4 = px.imshow(pct_a, text_auto=True, aspect="auto",
                     color_continuous_scale="teal",
                     zmin=0,
                     labels=dict(color="Share %"))
    fig4.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Monthly Trend ──────────────────────────────────────────────────────
st.subheader("📅 Monthly Response Trend")
sub_t = sub.copy()
sub_t["month"] = sub_t["date"].dt.to_period("M").astype(str)
trend = sub_t.pivot_table(index="month", columns="option_selected",
                          aggfunc="size", fill_value=0).reset_index()
fig5 = go.Figure()
for i, col_ in enumerate([c for c in trend.columns if c != "month"]):
    fig5.add_trace(go.Scatter(
        x=trend["month"], y=trend[col_],
        mode="lines+markers", name=col_,
        line=dict(color=PALETTE[i % len(PALETTE)], width=2.5),
        marker=dict(size=5)))
fig5.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                   xaxis_title="Month", yaxis_title="Responses",
                   legend=dict(orientation="h", y=1.15))
st.plotly_chart(fig5, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────────────────────
with st.expander("📋 View & Download Raw Data"):
    st.dataframe(sub.head(100), use_container_width=True)
    csv_bytes = sub.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        csv_bytes, "filtered_poll_data.csv", "text/csv")