import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="KSA Market Intelligence Dashboard", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2.2rem; max-width: 1450px;}
footer {visibility: hidden;}
.kpi-card{
  background: linear-gradient(145deg, rgba(16,26,43,0.92), rgba(11,18,32,0.92));
  border: 1px solid rgba(148,163,184,0.14);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 12px 26px rgba(0,0,0,0.22);
  height: 120px;
}
.kpi-label{font-size: 12px; color: rgba(229,231,235,0.72); margin-bottom: 7px;}
.kpi-value{font-size: 26px; font-weight: 760; color: #E5E7EB; line-height: 1.12;}
.kpi-sub{font-size: 12px; color: rgba(229,231,235,0.60); margin-top: 9px;}
.badge{
  display:inline-block; padding: 4px 10px; border-radius: 999px;
  border: 1px solid rgba(148,163,184,0.18);
  background: rgba(16,26,43,0.6);
  font-size: 12px; color: rgba(229,231,235,0.72);
  margin-right: 6px;
}
.section{
  background: rgba(16,26,43,0.62);
  border: 1px solid rgba(148,163,184,0.12);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.16);
}
.small-note{
  font-size: 13px;
  color: #000000;   /* أسود */
  font-weight: 500;
}
hr {border: none; border-top: 1px solid rgba(148,163,184,0.12); margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
header_left, header_right = st.columns([3, 1])

with header_left:
    st.title("KSA Market Intelligence Dashboard")
    st.markdown(
        "<span class='badge'>Live and interactive</span>"
        "<span class='badge'>Stakeholder-ready</span>"
        "<span class='badge'>Data source: Yahoo Finance</span>",
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        "<div class='section'>"
        "<div style='font-size:12px; color:rgba(229,231,235,0.7)'>Purpose</div>"
        "<div style='font-size:16px; font-weight:800; margin-top:4px'>Performance and risk snapshot</div>"
        "<div class='small-note' style='margin-top:8px'>A compact view to support market discussions.</div>"
        "</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

assets = {
    "TASI Index": "^TASI",
    "Saudi Aramco": "2222.SR",
    "Al Rajhi Bank": "1120.SR",
    "SABIC": "2010.SR",
    "STC": "7010.SR",
    "Alinma Bank": "1150.SR",
}

selected_name = st.sidebar.selectbox("Asset", list(assets.keys()), index=1)
selected_ticker = assets[selected_name]

compare_mode = st.sidebar.checkbox("Compare assets", value=True)
default_compare = ["Al Rajhi Bank", "SABIC", "STC"]
compare_names = st.sidebar.multiselect(
    "Assets to compare",
    [k for k in assets.keys() if k != selected_name],
    default=[n for n in default_compare if n in assets and n != selected_name] if compare_mode else []
)

time_range = st.sidebar.selectbox("Time range", ["1y", "2y", "5y", "10y"], index=2)
data_frequency = st.sidebar.selectbox("Data frequency", ["1d", "1wk", "1mo"], index=0)

st.sidebar.markdown("---")
risk_free_rate = st.sidebar.slider("Risk-free rate (annual %)", 0.0, 10.0, 4.0, 0.5)
show_trend_lines = st.sidebar.checkbox("Show trend lines", value=True)

st.sidebar.markdown("---")
st.sidebar.caption("If an asset returns no data, switch the asset or reduce the time range.")

# -----------------------------
# Data helpers
# -----------------------------
@st.cache_data(ttl=3600)
def fetch_prices(ticker: str, period: str, interval: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    except Exception:
        return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.reset_index()
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    if "Close" not in df.columns:
        return pd.DataFrame()

    return df.dropna(subset=["Close"]).copy()

def periods_per_year(interval: str) -> int:
    return 252 if interval == "1d" else 52 if interval == "1wk" else 12

def compute_metrics(df: pd.DataFrame, interval: str, rf_pct: float) -> dict:
    tmp = df.copy()
    tmp["Return"] = tmp["Close"].pct_change()

    latest = float(tmp["Close"].iloc[-1])
    prev = float(tmp["Close"].iloc[-2]) if len(tmp) > 1 else latest
    last_move = (latest / prev - 1) * 100 if prev else 0

    ppy = periods_per_year(interval)
    annual_return = float(tmp["Return"].mean() * ppy)
    annual_vol = float(tmp["Return"].std() * np.sqrt(ppy))

    rf = rf_pct / 100
    sharpe = (annual_return - rf) / annual_vol if annual_vol else np.nan

    peak = tmp["Close"].cummax()
    drawdown = (tmp["Close"] / peak) - 1.0
    max_drawdown = float(drawdown.min())

    year_df = tmp[tmp["Date"].dt.year == tmp["Date"].dt.year.max()]
    ytd = ((year_df["Close"].iloc[-1] / year_df["Close"].iloc[0]) - 1) if len(year_df) > 1 else np.nan

    return {
        "latest": latest,
        "last_move_pct": last_move,
        "annual_return": annual_return,
        "annual_vol": annual_vol,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "ytd": ytd,
    }

# -----------------------------
# Load data
# -----------------------------
df_main = fetch_prices(selected_ticker, time_range, data_frequency)

if df_main.empty and selected_ticker == "^TASI":
    st.warning("TASI data is not available right now. Continuing with Saudi Aramco as a proxy.")
    selected_name = "Saudi Aramco"
    selected_ticker = "2222.SR"
    df_main = fetch_prices(selected_ticker, time_range, data_frequency)

if df_main.empty:
    st.error(
        "No market data was returned.\n\n"
        "Try:\n"
        "- Switch the asset\n"
        "- Reduce the time range\n"
        "- Use daily frequency"
    )
    st.stop()

metrics = compute_metrics(df_main, data_frequency, risk_free_rate)

# -----------------------------
# KPI cards
# -----------------------------
def kpi(col, label, value, sub=""):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi(k1, "Selected Asset", selected_name, f"Symbol: {selected_ticker} • {time_range} • {data_frequency}")
kpi(k2, "Latest Price", f"{metrics['latest']:,.2f}", f"Last move: {metrics['last_move_pct']:+.2f}%")
kpi(k3, "Year-to-Date Return", f"{metrics['ytd']*100:.2f}%" if not np.isnan(metrics["ytd"]) else "N/A", "Simple year-to-date change")
kpi(k4, "Volatility", f"{metrics['annual_vol']*100:.2f}%", "Annualized estimate")
kpi(k5, "Maximum Drawdown", f"{metrics['max_drawdown']*100:.2f}%", "Worst peak-to-trough decline")
kpi(k6, "Sharpe Ratio", f"{metrics['sharpe']:.2f}" if not np.isnan(metrics["sharpe"]) else "N/A", f"Risk-free rate: {risk_free_rate:.1f}%")

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trend", "Risk", "Data"])

# -----------------------------
# Overview
# -----------------------------
with tab1:
    col_left, col_right = st.columns([2.1, 1])

    with col_left:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("Relative Performance")

        series = []
        base = df_main[["Date", "Close"]].copy()
        base["Name"] = selected_name
        series.append(base)

        if compare_mode:
            for name in compare_names:
                d = fetch_prices(assets[name], time_range, data_frequency)
                if not d.empty:
                    tmp = d[["Date", "Close"]].copy()
                    tmp["Name"] = name
                    series.append(tmp)

        combined = pd.concat(series, ignore_index=True).sort_values(["Name", "Date"])
        combined["Relative"] = combined.groupby("Name")["Close"].transform(lambda s: (s / s.iloc[0]) * 100)

        fig = px.line(combined, x="Date", y="Relative", color="Name", height=460)
        fig.update_layout(
            margin=dict(l=10, r=10, t=60, b=10),
            hovermode="x unified",
            yaxis_title="Relative performance (start = 100)",
            xaxis_title="Date"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2.1, 1])
    with col2:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("Stakeholder Notes")

        best_date = df_main.loc[df_main["Close"].idxmax(), "Date"].date()
        worst_date = df_main.loc[df_main["Close"].idxmin(), "Date"].date()

        vol_pct = metrics["annual_vol"] * 100
        risk_label = "Volatile" if vol_pct >= 25 else "Stable"
        dd_label = "Significant" if metrics["max_drawdown"] <= -0.2 else "Limited"

        st.markdown(
            f"""
            <div class="small-note">
            <b>Market behavior:</b> {risk_label}<br/>
            <b>Drawdown:</b> {dd_label}<br/><br/>
            <b>Best point in range:</b> {best_date}<br/>
            <b>Worst point in range:</b> {worst_date}<br/><br/>
            <b>How to use:</b><br/>
            Compare momentum across selected assets, then drill down into trend and risk views.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Trend
# -----------------------------
with tab2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Price Trend")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_main["Date"], y=df_main["Close"], mode="lines", name="Price"))

    if show_trend_lines and data_frequency == "1d":
        tmp = df_main.copy()
        tmp["Trend 50"] = tmp["Close"].rolling(50).mean()
        tmp["Trend 200"] = tmp["Close"].rolling(200).mean()
        fig.add_trace(go.Scatter(x=tmp["Date"], y=tmp["Trend 50"], mode="lines", name="Trend 50"))
        fig.add_trace(go.Scatter(x=tmp["Date"], y=tmp["Trend 200"], mode="lines", name="Trend 200"))

    fig.update_layout(
        height=520,
        hovermode="x unified",
        margin=dict(l=10, r=10, t=60, b=10),
        xaxis_title="Date",
        yaxis_title="Price"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='small-note'>Trend lines are most meaningful using daily frequency.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Risk
# -----------------------------
with tab3:
    left, right = st.columns(2)

    with left:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("Monthly Returns")

        tmp = df_main.copy()
        tmp["Month"] = tmp["Date"].dt.to_period("M").astype(str)
        monthly = tmp.groupby("Month", as_index=False).agg({"Close": "last"})
        monthly["Monthly return"] = monthly["Close"].pct_change() * 100

        fig_m = px.bar(monthly.dropna(), x="Month", y="Monthly return", height=420)
        fig_m.update_layout(margin=dict(l=10, r=10, t=60, b=10), yaxis_title="Return (%)")
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("Volatility Over Time")

        ppy = periods_per_year(data_frequency)
        window = 30 if data_frequency == "1d" else 10 if data_frequency == "1wk" else 6

        tmp = df_main.copy()
        tmp["Return"] = tmp["Close"].pct_change()
        tmp["Volatility"] = tmp["Return"].rolling(window).std() * np.sqrt(ppy) * 100

        fig_v = px.line(tmp.dropna(), x="Date", y="Volatility", height=420)
        fig_v.update_layout(margin=dict(l=10, r=10, t=60, b=10), yaxis_title="Volatility (%)")
        st.plotly_chart(fig_v, use_container_width=True)

        st.markdown(f"<div class='small-note'>Rolling window: {window} periods.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Return Distribution")

    tmp = df_main.copy()
    tmp["Return"] = tmp["Close"].pct_change()
    dist = px.histogram(tmp.dropna(), x="Return", nbins=55, height=380)
    dist.update_layout(margin=dict(l=10, r=10, t=60, b=10), xaxis_title="Return", yaxis_title="Count")
    st.plotly_chart(dist, use_container_width=True)

    st.markdown("<div class='small-note'>This helps explain normal days versus extreme days.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Data
# -----------------------------
with tab4:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Data Preview")

    st.dataframe(df_main.tail(60), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        "<div class='small-note'>Export a CSV file</div>",
        unsafe_allow_html=True
    )

    csv_bytes = df_main.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Export CSV",
        data=csv_bytes,
        file_name=f"{selected_ticker.replace('^','')}_{time_range}_{data_frequency}.csv",
        mime="text/csv"
    )
    st.markdown("</div>", unsafe_allow_html=True)