import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="Options Trading Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🔥 Options Trading Strategy Dashboard")
st.markdown("*Analyzing debit spread performance and edge analysis*")

# =========================
# LOAD DATA (NO UPLOAD)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("big_search.csv")  # <- bundled file
    df["expiration"] = pd.to_datetime(df["expiration"])
    df["run_start"] = pd.to_datetime(df["run_start"])
    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🎛️ Filters")

selected_tickers = st.sidebar.multiselect(
    "Tickers",
    options=sorted(df["ticker"].unique()),
    default=sorted(df["ticker"].unique())
)

selected_types = st.sidebar.multiselect(
    "Strategy Type",
    options=sorted(df["type"].unique()),
    default=sorted(df["type"].unique())
)

roi_range = st.sidebar.slider(
    "ROI Range",
    min_value=float(df["roi"].min()),
    max_value=float(df["roi"].max()),
    value=(float(df["roi"].min()), float(df["roi"].max()))
)

prob_range = st.sidebar.slider(
    "Probability ITM",
    min_value=float(df["prob_ITM"].min()),
    max_value=float(df["prob_ITM"].max()),
    value=(float(df["prob_ITM"].min()), float(df["prob_ITM"].max()))
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["ticker"].isin(selected_tickers)) &
    (df["type"].isin(selected_types)) &
    (df["roi"].between(*roi_range)) &
    (df["prob_ITM"].between(*prob_range))
]

# =========================
# METRICS ROW
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Trades", len(filtered_df))
col2.metric("Avg ROI", f"{filtered_df['roi'].mean():.2f}")
col3.metric("Avg Prob ITM", f"{filtered_df['prob_ITM'].mean():.2f}")
col4.metric("Total Expected Edge", f"{filtered_df['edge_type'].notna().sum()}")

st.divider()

# =========================
# TABLE VIEW
# =========================
st.subheader("📋 Trade Data")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# ROI VISUALIZATION
# =========================
st.subheader("📈 ROI Distribution")

fig = px.histogram(
    filtered_df,
    x="roi",
    color="type",
    nbins=30,
    title="ROI Distribution by Strategy Type"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TICKER PERFORMANCE
# =========================
st.subheader("📊 Average ROI by Ticker")

ticker_roi = filtered_df.groupby("ticker")["roi"].mean().reset_index()

fig2 = px.bar(
    ticker_roi,
    x="ticker",
    y="roi",
    title="Average ROI per Ticker"
)

st.plotly_chart(fig2, use_container_width=True)