# finance-dashboard
# Quantitative Portfolio Optimization Dashboard

This is a professional-grade financial analytics dashboard built with Python and Streamlit. The application specifically utilizes modern portfolio theory and Monte Carlo simulations to calculate optimal asset allocation based on historical market risk and returns.

## Core Features
* **Live Market Sync:** It dynamically extracts real-time adjusted closing price data directly from the Yahoo Finance API (`yfinance`).
* **Monte Carlo Engine:** It simulates 5,000 randomized asset weight vectors to model potential portfolio distributions.
* **Risk & Reward Analytics:** It automatically calculates annualized expected returns, expected volatility risk metrics, and determines the maximum **Sharpe Ratio**.
* **Local Persistence Layer:** It is integrated with a local JSON transaction file saver to seamlessly log, store, and reload custom ticker profiles.
* **Interactive Charting:** It maps out an automated efficient frontier visualization using responsive scatter plotting.

## Tech Stack
* **Frontend/UI:** Streamlit
* **Data Processing & Analytics:** Pandas, NumPy
* **Financial Data Engine:** yfinance
* **Storage:** Python JSON System
