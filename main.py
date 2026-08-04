from app import port_volatility
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import json
from replit.object_storage import Client #Offical Replit Database SDK

#Intiatize the Replit Database Cloud Client
db_client =  Client()

# --- STEP 1: PERFORMING DATA CACHING ---
@st.cache_data(ttl=3600) #Caches stock data for 1 hour to prevent API rate-limiting
def fetch_marketdata(tickers):
  """Downloads adjusted close data dynamically from Yahoo Finance"""
  raw_data = yf.download(tickers, period="1y", auto_adjust=False)
  return raw_data['Adj.Close']

# --- STEP 2: STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Pro Quant Dashboard", layout="wide")
st.title("Quatitative Portfolio Optimization Dashboard")

# --- STEP 3: DATABASE HELPERS ---
def save_portfolio(profile_name, ticker_string):
  """Saves raw user input tickers directly into the cloud bucket."""
  try:
    db_client.upload_from_text(f"profile_{profile_name}", ticker_string)
    return True
  except Exception as e:
    st.error(f"Database Save Error:{e}")
    return False

def load_portfolio(profile_name):
  """Retrieves saved tickers combinations from the cloud bucket."""
  try:
    return db_client.download_as_text(f"profile_{profile_name}")
  except Exception:
    return None

# --- STEP 4: USER INTERFACE SIDEBAR ---
st.sidebar.header("Dashboard Configuration")
st.sidebar.subheader("Portfolio Database Profiles")
profile_name = st.sidebar.text_input("Save/Load Profile Name","My_Tech_Growth")

# Default ticker state string
current_tickers = "AAPL, MSFT, GOOG, AMZN"

# Database profile loader trigger
if sidebar.button("Load Profile From DB"):
  loaded_data = load_portfolio(profile_name)
  if loaded_data:
    st.sidebar.success(f"No profile found matching '{profile_name}' !")
    current_tickers = loaded_data
  else: 
    st.sidebar.error(f"No profile found matching '{profile_name}'.")

# Primary input textbox
ticker_input = st.sidebar.text_input("Enter Tickers (separated by commas)", current_tickers)

#Database profile saver trigger
if st.sidebar.button("Save Current Tickers to DB"):
  if ticker_input and save_portfolio(profile_name, ticker_input):
    st.sidebar.success(f"Saved configuration to profile: '{profile_name}'!")

#Convert raw input string into a clean Python array
tickers_list = [t.strip().upper() for t in ticker_input.split(",")]

# --- STEP 5: CORE SIMULATION ENGINE ---
if st.button("Run Portfolio Simulation Optimization"):
  # Matrix  edge case safety catch
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

    #Accelerated Simulation Loop
    for index in range(num_portfolios):
      # Dynamically weights asset arrays without hardcoding vector lengths
      weights = np.random.random(num_assets)
      weights =  weights / np.sum(weights)
      all_weights.append(weights)

      # Portfolio Return Math
      p_return = np.sum(average_returns * weights) * 252
      portfolio_returns.append(p_return)

      # Portfolio Volaility (Risk Matrix Math)
      p_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
      portfolio_volatilities.append(port_volatility)

      # Sharpe Ratio Logic  (Ultilizing a baseline 2% risk-free rate)
      s_ratio = (p_return - 0.02) / p_volatility
      sharpe_ratios.append(s_ratio)

# Find the index of the absolute highest Sharpe Ratio
best_index = np.argmax(sharpe_ratios)

# --- STEP 6: DYNAMIC ASSET ALLOCATION MAPPING ---
optimal_allocation = {
  ticker: round(float(all_weights[best_index][i]* 100, 2))
  for i, ticker in enumerate(tickers_list)
}

# Assemble production-ready layout structure
dashboard_data = {
  "totalValue": 10000.00,
  "totalReturns": round(float(portfolio_returns[best_index]* 100),2),
  "riskMetric": round(float(portfolio_volatilities[best_index] * 100), 2),
  "sharpeRatio": round(float(sharpe_ratios[best_index]),2),
  "allocations": optimal_allocation
}

# Save the analytical results cleanly to your Replit cloud storage instance
serialized_data = json.dumps(dashboard_data)
db_client.upload_from_text(f"results_{profile_name}", serialized_data)

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

# --- LEVEL 5 CAPSTONE: EFFICIENT FRONTIER VISUALIZATION ---
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

except Exception as e:
st.error(f"Execution Error running quantitative models: {e}")