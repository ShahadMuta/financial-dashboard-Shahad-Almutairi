 KSA Market Intelligence Dashboard (TASI + Major Saudi Equities)

## Project Overview
This project delivers a live, interactive dashboard that summarizes market performance and risk for the Saudi market. The goal is to provide a clear, stakeholder-friendly snapshot that can support high-level investment discussions—without requiring deep technical knowledge.

Instead of presenting charts in isolation, the dashboard is structured the way an investment team would typically review a market: start with an executive view (performance comparison and signals), then drill into trend behavior, and finally review risk characteristics such as volatility, drawdowns, and return distributions.

## Data Source
The dashboard uses publicly available market data retrieved through Yahoo Finance using the `yfinance` Python library.  
The primary instrument can be TASI (`^TASI`) when available, and major Saudi equities (e.g., `2222.SR`, `1120.SR`, `2010.SR`) are included to enable practical comparison and to ensure the dashboard remains usable if index data is temporarily unavailable.

Fields used include time series prices (Open/High/Low/Close) and, when available, volume. These are sufficient to compute returns and risk indicators commonly used in market monitoring.

## Steps & Methodology
The workflow mirrors a simple analytics pipeline:
1. **Data extraction:** download time-series prices for a selected lookback window and sampling frequency.
2. **Preparation:** remove missing values and create time features (monthly buckets) to support aggregated views.
3. **Metrics:** compute return-based indicators such as annualized volatility, a Sharpe estimate (with a configurable risk-free rate), and maximum drawdown (peak-to-trough loss).
4. **Dashboard design:** keep the UI readable for non-technical stakeholders by using KPI cards, labeled sections, and a logical narrative flow (Executive → Trend → Risk → Data Appendix).

The goal is not to predict prices, but to provide a consistent, explainable monitoring view.

## Dashboard Screenshots
Add screenshots of the final dashboard here:

![Dashboard Screenshot 1](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\Dashbord6.png)  
![Dashboard Screenshot 2](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\Dashbord1.png)
![Dashboard Screenshot 1](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\dashbord2.png)  
![Dashboard Screenshot 2](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\Dashbord3.png)
![Dashboard Screenshot 2](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\Dashbord4.png)
![Dashboard Screenshot 2](C:\Users\shaha\OneDrive - Etec.gov.sa\سطح المكتب\financial-dashboard-tasi\Dashbord5.png)

## Key Insights 
From a stakeholder perspective, the dashboard helps answer practical questions:
- Is the market (or asset) trending positively over the lookback period?
- How unstable is the price behavior (risk regime), and does volatility change over time?
- What is the “worst-case feel” during the period (maximum drawdown)?
- How do major names compare in relative momentum when normalized to the same starting point?

These insights support framing discussions around allocation, hedging, or timing—while acknowledging that this is a monitoring tool rather than a trading system.

## Live Dashboard Link
**Live App:** [PASTE STREAMLIT LINK HERE]

## Assumptions & Limitations
- Metrics are estimates based on historical prices and depend on the selected sampling frequency.
- Sharpe ratio is simplified and uses a user-selected risk-free rate.
- Yahoo Finance availability may vary by ticker and time window. For robustness, the dashboard supports switching assets and comparing major equities.
- This dashboard is designed for monitoring and communication, not as financial advice or a trading recommendation.