import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Trading Dashboard", layout="wide")

st.title("📊 Multi-Strategy Trading Dashboard")

# =========================
# LOAD DATASETS
# =========================

options_df = pd.read_csv("big_search.csv")
options_df["expiration"] = pd.to_datetime(options_df["expiration"])
options_df["run_start"] = pd.to_datetime(options_df["run_start"])

big_move_df = pd.read_csv("big_move_sample.csv")
big_move_df["last_update"] = pd.to_datetime(big_move_df["last_update"])

plays_df = pd.read_csv("plays_sample.csv")
plays_df["expiration"] = pd.to_datetime(plays_df["expiration"])
plays_df["run_start"] = pd.to_datetime(plays_df["run_start"])

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs([
    "📈 Options Strategies",
    "⚡ Big Move Signals",
    "💰 Plays"
])

# =========================
# TAB 1 - OPTIONS (WITH GRAPHS)
# =========================
with tab1:
    st.subheader("Options Strategy Data")

    # Ticker filter
    option_tickers = st.multiselect(
        "Filter Options Tickers",
        options=sorted(options_df["ticker"].unique()),
        default=sorted(options_df["ticker"].unique())
    )

    filtered_options = options_df[
        options_df["ticker"].isin(option_tickers)
    ]

    st.dataframe(filtered_options, use_container_width=True)

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Avg ROI", round(filtered_options["roi"].mean(), 2))

    with col2:
        st.metric("Avg Prob ITM", round(filtered_options["prob_ITM"].mean(), 3))

    # 📈 ROI DISTRIBUTION
    st.subheader("📈 ROI Distribution")
    fig1 = px.histogram(
        filtered_options,
        x="roi",
        color="type",
        nbins=20
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 📊 AVG ROI BY TICKER
    st.subheader("📊 Average ROI by Ticker")
    ticker_avg = filtered_options.groupby("ticker")["roi"].mean().reset_index()

    fig2 = px.bar(
        ticker_avg,
        x="ticker",
        y="roi"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 2 - BIG MOVES (TABLE ONLY)
# =========================
with tab2:
    st.subheader("Big Move Signal Tracker")

    move_tickers = st.multiselect(
        "Filter Big Move Tickers",
        options=sorted(big_move_df["Symbol"].unique()),
        default=sorted(big_move_df["Symbol"].unique())
    )

    filtered_moves = big_move_df[
        big_move_df["Symbol"].isin(move_tickers)
    ]

    st.dataframe(filtered_moves, use_container_width=True)

# =========================
# TAB 3 - PLAYS (TABLE ONLY)
# =========================
with tab3:
    st.subheader("Trade Plays Dashboard")

    st.dataframe(plays_df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Avg ROI", round(plays_df["roi"].mean(), 2))

    with col2:
        st.metric("Max ROI", round(plays_df["roi"].max(), 2))

# in terminal: streamlit run app.py