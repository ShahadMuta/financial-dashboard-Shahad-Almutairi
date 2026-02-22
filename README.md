# KSA Market Intelligence Dashboard  
*(TASI + Major Saudi Equities)*

## Project Overview

This project presents a live, interactive market intelligence dashboard designed to analyze performance dynamics and risk characteristics within the Saudi equity market. The objective is to provide a clear, stakeholder-friendly analytical view that supports strategic investment discussions without requiring deep technical expertise.

Rather than presenting isolated charts, the dashboard follows a structured narrative similar to how an investment committee might review markets. It begins with a high-level executive performance comparison, then explores trend behavior across selected assets, and finally evaluates key risk indicators such as volatility, maximum drawdown, and return distribution. The focus throughout the design is clarity, interpretability, and decision support rather than price prediction or algorithmic trading.

The dashboard is built using **Streamlit** and deployed via **Streamlit Community Cloud**, ensuring real-time interactivity and online accessibility.

---

## Data Source

Market data is retrieved using publicly available price data from Yahoo Finance through the **yfinance** Python library. The dashboard supports the TASI index (^TASI) when available, alongside major Saudi equities including:

- 2222.SR (Saudi Aramco)  
- 1120.SR (Al Rajhi Bank)  
- 2010.SR (SABIC)  
- 7010.SR (STC)  

Historical Open, High, Low, Close, and (when available) Volume data are used to compute return-based performance measures and risk indicators.

Representative CSV exports of the analyzed instruments are included in the `/datasets` folder to ensure transparency and reproducibility.

---

## Methodology

The analytical workflow follows a structured financial analytics pipeline.

First, historical time-series data are extracted for a selected lookback window and sampling frequency. The data are then cleaned to remove missing observations and transformed into return series to enable risk and performance analysis.

Next, core performance and risk metrics are computed, including:

- Annualized volatility  
- Maximum drawdown (peak-to-trough decline)  
- Simplified Sharpe ratio using a configurable risk-free rate  
- Normalized relative performance for cross-asset comparison  

Relative performance is normalized to a common base value to allow assets with different price levels to be compared on equal footing.

The dashboard interface is structured using KPI cards, clearly labeled sections, and interactive filters to maintain accessibility for non-technical stakeholders while preserving analytical depth.

The purpose of this dashboard is structured market monitoring and communication rather than forecasting or investment recommendation.

---

## Dashboard Screenshots

### Executive Overview
![Executive Overview](Dashboard1.png)

### Price Trend Analysis
![Price Trend](Dashboard4.png)

### Risk & Drawdown Analysis
![Risk](Dashboard5.png)

### Data Appendix
![Data View](Dashboard6.png)

---

## Key Insights

From a stakeholder perspective, the dashboard enables structured interpretation of Saudi market behavior. It supports evaluation of relative performance between major equities, identification of prevailing volatility regimes, and understanding of worst-case drawdown experiences over selected periods.

By combining normalized performance views with risk-adjusted metrics, the dashboard helps frame allocation discussions and risk awareness conversations while acknowledging that historical performance does not guarantee future results.

---

## Live Dashboard Link

**Live App:**  
https://financial-dashboard-shahad-almutairi-b4sfm3nfupscukamtsjjnr.streamlit.app/

---

## Assumptions and Limitations

All metrics presented are derived from historical price data and are therefore backward-looking in nature.

The Sharpe ratio is a simplified estimate and depends on the user-selected risk-free rate.

Yahoo Finance data availability may vary across tickers and time windows.

This dashboard is intended strictly for analytical and educational purposes and does not constitute financial advice or an investment recommendation.
