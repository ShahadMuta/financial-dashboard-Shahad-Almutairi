# KSA Market Intelligence Dashboard  
*(TASI + Major Saudi Equities)*

## Project Overview

This project delivers a live, interactive dashboard designed to summarize market performance and risk dynamics in the Saudi equity market. The primary objective is to provide a clear, stakeholder-friendly view that supports strategic investment discussions without requiring deep technical expertise.

The dashboard follows a structured narrative similar to how an investment committee would review markets: beginning with an executive performance comparison, then drilling into trend behavior, and finally analyzing risk characteristics such as volatility, drawdowns, and return distribution. The focus is on clarity, interpretability, and decision-support rather than price prediction.

---

## Data Source

Market data is retrieved using the **Yahoo Finance API via the yfinance Python library**. The dashboard supports the TASI index (^TASI) when available, as well as major Saudi equities including:

- 2222.SR (Saudi Aramco)  
- 1120.SR (Al Rajhi Bank)  
- 2010.SR (SABIC)  
- 7010.SR (STC)  

Historical Open, High, Low, Close, and (when available) Volume data are used to compute return-based indicators and risk metrics.

---

## Methodology

The analytical workflow follows a simplified financial analytics pipeline:

1. **Data Extraction** – Download historical time-series data for a selected lookback window and frequency.
2. **Data Preparation** – Remove missing observations and generate time-based aggregations.
3. **Metric Computation** – Calculate annualized volatility, maximum drawdown, Sharpe ratio (using a configurable risk-free rate), and normalized relative performance.
4. **Dashboard Design** – Present outputs using KPI cards, structured sections, and interactive filters to ensure accessibility for non-technical stakeholders.

The purpose of the dashboard is monitoring and structured communication of market behavior rather than forecasting or algorithmic trading.

---

## Dashboard Screenshots

![Dashboard Overview](Dashboard1.png)
![Trend Analysis](dashboard2.png)
![Risk View](Dashboard3.png)
![Volatility](Dashboard4.png)
![Distribution](Dashboard5.png)
![Data View](Dashboard6.png)

---

## Key Insights

From a stakeholder perspective, the dashboard enables practical market interpretation:

- Assessment of relative performance between major Saudi equities.
- Identification of prevailing volatility regimes.
- Understanding of worst peak-to-trough declines.
- Contextual interpretation of return distribution patterns.
- Framing allocation discussions based on risk-adjusted performance metrics.

The dashboard supports informed discussion and monitoring, while recognizing that market behavior is inherently uncertain.

---

## Live Dashboard Link

**Live App:**  
https://financial-dashboard-shahad-almutairi-b4sfm3nfupscukamtsjjnr.streamlit.app/

---

## Assumptions & Limitations

All metrics are derived from historical price data and are therefore backward-looking.

The Sharpe ratio is a simplified estimate using a user-defined risk-free rate.

Yahoo Finance data availability may vary by ticker or time window.

This dashboard is intended strictly for analytical and educational purposes and does not constitute financial advice.
