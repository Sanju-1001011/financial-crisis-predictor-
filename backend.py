import pandas as pd
import xgboost as xgb
import shap

import yfinance as yf
import streamlit as st

@st.cache_data(ttl=60)  # Caches the data for 60 seconds to prevent API rate-limiting
def fetch_live_telemetry():
    """Fetches real-time market data from the Yahoo Finance API."""
    live_data = {}
    
    try:
        # 1. VIX (Market Fear Index)
        vix = yf.Ticker("^VIX").history(period="1d")
        live_data['VIX'] = round(vix['Close'].iloc[-1], 2) if not vix.empty else 18.40
        
        # 2. US 10-Year Treasury Yield
        tnx = yf.Ticker("^TNX").history(period="1d")
        live_data['US_10Y'] = round(tnx['Close'].iloc[-1], 3) if not tnx.empty else 4.120
        
        # 3. Brent Crude Oil
        brent = yf.Ticker("BZ=F").history(period="1d")
        live_data['BRENT'] = round(brent['Close'].iloc[-1], 2) if not brent.empty else 84.50
        
        # 4. EUR/USD Exchange Rate
        eurusd = yf.Ticker("EURUSD=X").history(period="1d")
        live_data['EUR_USD'] = round(eurusd['Close'].iloc[-1], 4) if not eurusd.empty else 1.0820
        
    except Exception as e:
        # Failsafe: Falls back to baseline numbers if the internet drops
        live_data = {'VIX': 18.40, 'US_10Y': 4.120, 'BRENT': 84.50, 'EUR_USD': 1.0820}
        
    return live_data

def load_data(filepath="data/processed_signals.csv"):
    df = pd.read_csv(filepath)
    features = [
        'yield_curve_slope', 'credit_gdp', 'credit_gdp_diff2', 
        'credit_gdp_cycle', 'yield_curve_cycle', 'cpi', 'unemp', 'debtgdp'
    ]
    for col in features:
        df[col] = df[col].fillna(df[col].median())
    return df, features

def load_model(filepath="models/xgboost_crisis_model.json"):
    model = xgb.XGBClassifier()
    model.load_model(filepath)
    return model

def predict_risk(model, input_df):
    prob = model.predict_proba(input_df)[0][1]
    return prob * 100

def generate_shap_values(model, input_df):
    explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")
    return explainer(input_df)
def calculate_global_risk(df, model, features):
    """Scans the latest available data for all countries and calculates current risk."""
    # Grab the most recent year for each country
    latest_data = df.loc[df.groupby('country')['year'].idxmax()].copy()
    
    # Run the AI prediction on all of them at once
    X = latest_data[features]
    latest_data['Risk Score'] = model.predict_proba(X)[:, 1] * 100
    
    return latest_data[['country', 'year', 'Risk Score']]

def calculate_global_risk(df, model, features):
    """Scans the latest available data for all countries and calculates current risk."""
    # Grab the most recent year for each country
    latest_data = df.loc[df.groupby('country')['year'].idxmax()].copy()
    
    # Run the AI prediction on all of them at once
    X = latest_data[features]
    latest_data['Risk Score'] = model.predict_proba(X)[:, 1] * 100
    
    return latest_data[['country', 'year', 'Risk Score']]