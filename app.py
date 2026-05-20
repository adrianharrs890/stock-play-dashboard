import streamlit as st
import pandas as pd
import plotly.express as px
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# THEME (DARK GREY + READABLE)
# =========================
st.markdown("""
<style>
    .stApp {
        background-color: #bfc7d1;
        color: #000000;
    }

    section[data-testid="stSidebar"] {
        background-color: #9aa4b2;
    }

    html, body, [class*="css"] {
        color: #000000 !important;
    }

    h1, h2, h3 {
        color: #000000 !important;
        font-weight: 700;
    }

    button[data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 600;
    }

    .stButton button {
        background-color: #334155;
        color: white;
    }

    .stDataFrame {
        background-color: white;
    }

    /* FIX captions */
    div[data-testid="stCaptionContainer"] p {
        color: #000000 !important;
    }

    header, .stDeployButton, .viewerBadge {
        color: white !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Trading Dashboard")

# =========================
# RUN INFO (AS REQUESTED)
# =========================
run_start = "Time I started the script"
_start = time.time()

# =========================
# LOAD DATA
# =========================
big_search = pd.read_csv("big_search.csv")
money_flow = pd.read_csv("money_flow.csv")
entry_table = pd.read_csv("entry_table.csv")
plays = pd.read_csv("plays.csv")
big_move = pd.read_csv("big_move.csv")

# =========================
# DATE CLEANING
# =========================
big_search["expiration"] = pd.to_datetime(big_search["expiration"]).dt.date
plays["expiration"] = pd.to_datetime(plays["expiration"]).dt.date
big_move["last_update"] = pd.to_datetime(big_move["last_update"]).dt.date
entry_table["dates"] = pd.to_datetime(entry_table["dates"]).dt.date

# =========================
# CLEAN COLUMNS
# =========================
def clean_columns(df):
    df = df.copy()
    df.columns = [c.replace("_", " ").title() for c in df.columns]
    return df

# =========================
# FILTERS
# =========================
st.sidebar.header("🎛️ Filters")

main_tickers = (
    big_search["ticker"]
    .value_counts()
    .head(10)
    .index
    .tolist()
)

selected_tickers = st.sidebar.multiselect(
    "Main Tickers (Top 10)",
    options=main_tickers,
    default=main_tickers
)

all_expirations = sorted(big_search["expiration"].dropna().unique())

selected_expirations = st.sidebar.multiselect(
    "Expiration Dates",
    options=all_expirations,
    default=all_expirations
)

# =========================
# FILTER DATA
# =========================
big_search_f = big_search[
    (big_search["ticker"].isin(selected_tickers)) &
    (big_search["expiration"].isin(selected_expirations))
]

big_move_f = big_move[big_move["Symbol"].isin(selected_tickers)]
plays_f = plays.copy()
money_flow_f = money_flow.copy()
entry_table_f = entry_table.copy()

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Big Search",
    "💸 Money Flow",
    "📅 Entry Table",
    "💰 Plays",
    "⚡ Big Moves"
])

# =========================
# TAB 1
# =========================
with tab1:
    st.subheader("Big Search Strategies")
    st.caption("Searching the market for options with an edge")

    df = big_search_f
    st.dataframe(clean_columns(df), use_container_width=True, hide_index=True)

    if "roi" in df.columns:
        col1, col2 = st.columns(2)

        mean_roi = df["roi"].mean()
        std_roi = df["roi"].std()

        with col1:
            st.markdown("### Avg ROI")
            st.markdown(f"## {round(mean_roi, 2)}")

        with col2:
            st.markdown("### Std Dev ROI")
            st.markdown(f"## {round(std_roi, 2)}")

        fig = px.histogram(df, x="roi", nbins=20)
        st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    st.subheader("Money Flow")
    st.caption("Industries where capital is actively flowing")

    st.dataframe(clean_columns(money_flow_f), use_container_width=True, hide_index=True)

# =========================
# TAB 3
# =========================
with tab3:
    st.subheader("Entry Signals")
    st.caption("Over-market and momentum-based signals")

    st.dataframe(clean_columns(entry_table_f), use_container_width=True, hide_index=True)

# =========================
# TAB 4
# =========================
with tab4:
    st.subheader("Plays")
    st.caption("Statistical arbitrage strategies generated internally")

    shares_df = plays_f[plays_f["strategy_choice"] == "shares"]
    other_df = plays_f[plays_f["strategy_choice"] != "shares"]

    shares_display = clean_columns(shares_df.drop(
        columns=["max_loss_dollars", "roi", "expiration", "buy_target"],
        errors="ignore"
    ))

    st.markdown("### Shares (Simplified View)")
    st.dataframe(shares_display, use_container_width=True, hide_index=True)

    st.markdown("### Other Strategies")
    st.dataframe(clean_columns(other_df), use_container_width=True, hide_index=True)

    st.markdown("""
    ---
    ### 🧠 Signal Definitions
    - **Signal 1** = Stat arbitrage signal  
    - **Signal 2** = Stat arbitrage + overall market signal  
    """)

# =========================
# TAB 5
# =========================
with tab5:
    st.subheader("Big Move Signals")
    st.caption("Price increases or decreases with abnormal volume over the last 7 days")

    df = big_move_f
    st.dataframe(clean_columns(df), use_container_width=True, hide_index=True)

    numeric_cols = df.select_dtypes(include="number")

    if len(numeric_cols.columns) > 0:
        col = numeric_cols.columns[0]

        mean_val = df[col].mean()
        std_val = df[col].std()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### Mean ({col})")
            st.markdown(f"## {round(mean_val, 2)}")

        with col2:
            st.markdown(f"### Std Dev ({col})")
            st.markdown(f"## {round(std_val, 2)}")

# =========================
# FOOTER
# =========================
runtime = round(time.time() - _start, 4)

st.markdown(f"""
---
### 🧠 System Notes
- **Run Start** = {run_start}
- **Run Time** = time it ran
""")
# in terminal: streamlit run app.py