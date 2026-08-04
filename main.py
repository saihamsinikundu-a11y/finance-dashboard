import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import json
import os
from replit.object_storage import Client #Offical Replit Database SDK

# --- STEP 1: PERFORMING DATA CACHING ---
@st.cache_data(ttl=3600) #Caches stock data for 1 hour to prevent API rate-limiting
def fetch_marketdata(tickers):
  """Downloads adjusted close data dynamically from Yahoo Finance"""
  raw_data = yf.download(tickers, period="1y", auto_adjust=False)
  return raw_data['Adj Close']

# --- STEP 2: STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Pro Quant Dashboard", layout="wide")
st.title("Quatitative Portfolio Optimization Dashboard")

# Intiatize native Streamlit session state memory for profile persistence
if "saved_profiles" not in st.session_state:
  st.session_state["saved_profiles"] = {}

# --- STEP 3: DATABASE HELPERS (LOCAL JSON EDITION) ---
DB_FILE = "portfolio_db.json"

def _load_all_profiles():
  """Internal helper to read the JSON file securely"""
  if not os.path.exists(DB_FILE):
    return {}
  try:
    with open(DB_FILE, "r") as f:
      return json.load(f)
  except Exception:
    return {}

def save_portfolio(profile_name, ticker_string):
  """Saves user input tickers directly into a local JSON file."""
  profiles = _load_all_profiles()
  profiles[profile_name] = ticker_string
  try:
    with open(DB_FILE, "w") as f:
      json.dump(profiles, f, indent=4)
    return True
  except Exception as e:
    st.sidebar.error(f"Save failed: {e}")
    return False

def load_portfolio(profile_name):
  """Retrieves saved tickers combinations from the local JSON file."""
  profiles = _load_all_profiles()
  return profiles.get(profile_name, None)

# --- STEP 4: USER INTERFACE SIDEBAR ---
st.sidebar.header("Dashboard Configuration")
# 👇 ADD YOUR CUSTOM AUTHOR CREDITS HERE 👇
st.sidebar.markdown("---")
st.sidebar.markdown("### ✍️ App Author")
st.sidebar.caption("Created by **Sai Hamsini Kundu**")
st.sidebar.markdown("[🐙 GitHub](https://github.com/saihamsinikundu-a11y/finance-dashboard)")
st.sidebar.markdown("---")

st.sidebar.subheader("Portfolio Database Profiles")
profile_name = st.sidebar.text_input("Save/Load Profile Name", "My_Tech_Growth")

# Default ticker state string fallback
current_tickers = "AAPL, MSFT, GOOG, AMZN"

# Database profile loader trigger
if st.sidebar.button("Load Profile From DB"):
  loaded_data = load_portfolio(profile_name)
  if loaded_data:
    st.sidebar.success(f"Loaded profile matching '{profile_name}'!")
    current_tickers = loaded_data
  else: 
    st.sidebar.error(f"No profile found matching '{profile_name}'.")

# Primary input textbox (bound to our variable)
ticker_input = st.sidebar.text_input("Enter Tickers (separated by commas)", current_tickers)

# Database profile saver trigger
if st.sidebar.button("Save Current Tickers to DB"):
  if ticker_input and save_portfolio(profile_name, ticker_input):
    st.sidebar.success(f"Saved configuration to profile: '{profile_name}'!")

 # Convert raw input string into a clean Python array
tickers_list = [t.strip().upper() for t in ticker_input.split(",")]   

# --- STEP 5: CORE SIMULATION ENGINE ---
if st.button("Run Portfolio Simulation Optimization"):
    # Matrix edge case safety catch
    if len(tickers_list) < 2:
        st.error("Please enter at least 2 tickers to calculate a multi-asset matrix.")
        st.stop()

    with st.spinner("Processing quantitative metrics optimization..."):
        try:
            # Dynamic data extraction
            historical_prices = fetch_marketdata(tickers_list)
            daily_returns = historical_prices.pct_change().dropna()
            average_returns = daily_returns.mean()
            covariance_matrix = daily_returns.cov() * 252

            # Monte Carlo Simulation Variables
            num_portfolios = 5000
            all_weights = []
            portfolio_returns = []
            portfolio_volatilities = []
            sharpe_ratios = []

            num_assets = len(tickers_list)

            # Accelerated Simulation Loop
            for index in range(num_portfolios):
                # Dynamically weights asset arrays without hardcoding vector lengths
                weights = np.random.random(num_assets)
                weights = weights / np.sum(weights)
                all_weights.append(weights)

                # Portfolio Return Math
                p_return = np.sum(average_returns * weights) * 252
                portfolio_returns.append(p_return)

                # Portfolio Volaility (Risk Matrix Math)
                p_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
                portfolio_volatilities.append(p_volatility)

                # Sharpe Ratio Logic (Utilizing a baseline 2% risk-free rate)
                s_ratio = (p_return - 0.02) / p_volatility
                sharpe_ratios.append(s_ratio)

            # Find the index of the absolute highest Sharpe Ratio
            best_index = np.argmax(sharpe_ratios)

        except Exception as e:
            st.error(f"Error calculating portfolio metrics: {e}")
            st.stop()

    # --- STEP 6: DYNAMIC ASSET ALLOCATION MAPPING ---
    optimal_allocation = {
        ticker: round(float(all_weights[best_index][i] * 100), 2)
        for i, ticker in enumerate(tickers_list)
    }

    # Assemble production-ready layout structure
    dashboard_data = {
        "totalValue": 10000.00,
        "totalReturns": round(float(portfolio_returns[best_index] * 100), 2),
        "riskMetric": round(float(portfolio_volatilities[best_index] * 100), 2),
        "sharpeRatio": round(float(sharpe_ratios[best_index]), 2),
        "allocations": optimal_allocation
    }

    # -- STEP 7: STREAMLIT UI CAR METRICS ---
    st.success(f"Dashboard data successfully optimized and synced to profile: {profile_name}!")

    st.subheader("Optimal Portfolio Matrix Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Max Sharpe Ratio", f"{dashboard_data['sharpeRatio']:.2f}")
    col2.metric("Expected Annual Return", f"{dashboard_data['totalReturns']}%")
    col3.metric("Expected Volatility Risk", f"{dashboard_data['riskMetric']}%")

    # Render asset allocation breakdown table
    st.subheader("Target Asset Weights Allocation")
    allocation_df = pd.DataFrame(list(optimal_allocation.items()), columns=["Ticker", "Weight (%)"])
    st.dataframe(allocation_df, use_container_width=True)

    # --- EFFICIENT FRONTIER VISUALIZATION ---
    st.subheader("Efficient Frontier Simulation Mapping")
    chart_df = pd.DataFrame({
        "Risk (Volatility)": portfolio_volatilities,
        "Return": portfolio_returns,
        "Sharpe Ratio": sharpe_ratios
    })
    st.scatter_chart(
        chart_df,
        x="Risk (Volatility)",
        y="Return",
        color="Sharpe Ratio",
        use_container_width=True
    )