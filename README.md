# finance-dashboard
# 📈 Quantitative Portfolio Optimization Dashboard

A professional-grade financial analytics dashboard built with Python and Streamlit. This application utilizes modern portfolio theory and Monte Carlo simulations to calculate optimal asset allocation based on historical market risk and returns.

## ✨ Core Features
* **Live Market Sync:** Dynamically extracts real-time adjusted closing price data directly from the Yahoo Finance API (`yfinance`).
* **Monte Carlo Engine:** Simulates 5,000 randomized asset weight vectors to model potential portfolio distributions.
* **Risk & Reward Analytics:** Automatically calculates annualized expected returns, expected volatility risk metrics, and determines the maximum **Sharpe Ratio**.
* **Local Persistence Layer:** Integrated with a local JSON transaction file saver to seamlessly log, store, and reload custom ticker profiles.
* **Interactive Charting:** Maps out an automated efficient frontier visualization using responsive scatter plotting.

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **Data Processing & Analytics:** Pandas, NumPy
* **Financial Data Engine:** yfinance
* **Storage:** Python JSON System