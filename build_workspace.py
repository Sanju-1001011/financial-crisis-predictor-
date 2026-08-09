import os
import json

print("Initializing Project Scaffolding...")

# 1. Create Directories
directories = ['data', 'models']
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"📁 Created directory: {directory}/")

# 2. Define standard text and Python files
files_to_create = {
    "requirements.txt": """pandas
xgboost
shap
streamlit
plotly
matplotlib
scikit-learn
statsmodels
jupyter
""",

    ".gitignore": """# Python cache
__pycache__/
*.pyc

# Virtual environments
.env
.venv/
env/

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Datasets & Models (Uncomment below if you don't want to push data to GitHub)
# data/
# models/
""",

    "README.md": """# Systemic Macroeconomic Early Warning System
An interactive, machine-learning-powered Early Warning System (EWS) designed to predict systemic financial crises using historical macroeconomic data. 

## Architecture
* **Signal Processing:** Hodrick-Prescott (HP) filtering to isolate long-term credit cycles.
* **Algorithm:** Extreme Gradient Boosting (XGBoost) with Asymmetric Cost-Sensitive Learning.
* **Explainability:** SHAP (SHapley Additive exPlanations) for transparent diagnostic telemetry.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Launch the terminal: `python -m streamlit run app.py`
""",

    "backend.py": """import pandas as pd
import xgboost as xgb
import shap

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
""",

    "frontend.py": """import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import shap

def apply_custom_css():
    st.markdown('''
    <style>
        .ticker-wrap { width: 100%; background-color: #0e1117; border-top: 1px solid #333; border-bottom: 1px solid #333; overflow: hidden; white-space: nowrap; box-sizing: border-box; padding: 5px 0; margin-bottom: 20px; }
        .ticker { display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; font-family: 'Courier New', Courier, monospace; color: #f59e0b; font-size: 14px; font-weight: bold; }
        @keyframes ticker { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }
        .pulse-red { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #ef4444; box-shadow: 0 0 0 rgba(239, 68, 68, 0.4); animation: pulse-red 1.5s infinite; margin-right: 8px; }
        @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); } 70% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
        .solid-green { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #10b981; margin-right: 8px; }
    </style>
    ''', unsafe_allow_html=True)

def render_ticker():
    st.markdown('''
    <div class="ticker-wrap"><div class="ticker">
        ⚠️ GLOBAL MACRO MONITOR ONLINE | VIX Volatility: 18.4 (+1.2%) | US Treasury 10Y Yield: 4.12% | Brent Crude: $84.50 | SYSTEM MESSAGE: Scanning Historical Credit Cycles... ⚠️
    </div></div>
    ''', unsafe_allow_html=True)

def determine_risk_level(risk_score):
    if risk_score >= 60:
        return "CRITICAL SYSTEMIC RISK", "#ef4444", "<div style='background-color: rgba(239, 68, 68, 0.1); border-left: 5px solid #ef4444; padding: 10px;'><span class='pulse-red'></span><b style='color: #ef4444; font-size: 18px;'>WARNING: HIGH PROBABILITY OF IMPENDING FINANCIAL COLLAPSE DETECTED</b></div>"
    elif risk_score >= 30:
        return "ELEVATED RISK DETECTED", "#f59e0b", "<div style='background-color: rgba(245, 158, 11, 0.1); border-left: 5px solid #f59e0b; padding: 10px;'><span class='solid-green' style='background: #f59e0b;'></span><b style='color: #f59e0b; font-size: 18px;'>CAUTION: MACROECONOMIC INSTABILITY RISING</b></div>"
    else:
        return "ECONOMY STABLE", "#10b981", "<div style='background-color: rgba(16, 185, 129, 0.1); border-left: 5px solid #10b981; padding: 10px;'><span class='solid-green'></span><b style='color: #10b981; font-size: 18px;'>STATUS NORMAL: METRICS WITHIN STABLE OPERATING RANGES</b></div>"

def render_gauge(risk_score, gauge_color, risk_label):
    st.markdown("<h4 style='text-align: center; font-family: monospace;'>PROBABILITY GAUGE</h4>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = risk_score,
        number = {'suffix': "%", 'font': {'size': 50, 'family': 'monospace'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': gauge_color}, 'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2, 'bordercolor': "#333",
            'steps': [
                {'range': [0, 30], 'color': "rgba(16, 185, 129, 0.1)"},
                {'range': [30, 60], 'color': "rgba(245, 158, 11, 0.1)"},
                {'range': [60, 100], 'color': "rgba(239, 68, 68, 0.1)"}
            ],
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<h3 style='text-align: center; color: {gauge_color}; font-family: monospace;'>{risk_label}</h3>", unsafe_allow_html=True)

def render_shap(shap_values):
    st.markdown("<h4 style='font-family: monospace;'>DIAGNOSTIC TELEMETRY (SHAP)</h4>", unsafe_allow_html=True)
    st.caption("Forces pushing the needle. Red pushes toward crisis, Blue pushes toward stability.")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 5))
    shap.plots.waterfall(shap_values[0], show=False)
    plt.gcf().patch.set_facecolor('none')
    plt.gca().patch.set_facecolor('none')
    st.pyplot(fig)
""",

    "app.py": """import streamlit as st
import pandas as pd
import backend
import frontend

st.set_page_config(page_title="AI Risk Monitor", layout="wide", initial_sidebar_state="collapsed")
frontend.apply_custom_css()
frontend.render_ticker()

@st.cache_data
def fetch_data(): return backend.load_data()

@st.cache_resource
def fetch_model(): return backend.load_model()

try:
    df, features = fetch_data()
    model = fetch_model()
except Exception as e:
    st.error("SYSTEM ERROR: Data or Model files missing. Please run Jupyter Notebooks 01-03 first to generate the required files.")
    st.stop()

col_title, col_status = st.columns([4, 1])
with col_title: st.title("AI Crisis Prediction Terminal")
with col_status: st.markdown("<br><div style='text-align: right;'><span class='solid-green'></span><b>System Online</b></div>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)
with col1: country = st.selectbox("Select Target Economy:", sorted(df['country'].unique()))
with col2: future_year = st.slider("Forecast Year:", 2025, 2060, 2030)

country_history = df[df['country'] == country].sort_values('year')
latest_year = int(country_history['year'].max())
baseline_data = country_history.iloc[-1]
st.info(f"**DATA FEED LOCKED:** Using {latest_year} closing data as the base vector for the {future_year} simulation.")

st.markdown("### Terminal Input Parameters")
sl_col1, sl_col2 = st.columns(2)

with sl_col1:
    val_ycs = st.slider("Yield Curve Slope (%)", -10.0, 10.0, float(baseline_data['yield_curve_slope']), step=0.1)
    val_cg = st.slider("Credit-to-GDP (%)", 0.0, 300.0, float(baseline_data['credit_gdp']), step=1.0)
    val_cgd2 = st.slider("2-Year Credit Velocity", -50.0, 50.0, float(baseline_data['credit_gdp_diff2']), step=0.5)
    val_cgc = st.slider("Credit Cycle Deviation", -50.0, 50.0, float(baseline_data['credit_gdp_cycle']), step=0.5)

with sl_col2:
    val_ycc = st.slider("Yield Cycle Deviation", -10.0, 10.0, float(baseline_data['yield_curve_cycle']), step=0.1)
    val_cpi = st.slider("Inflation Index (CPI)", 0.0, 500.0, float(baseline_data['cpi']), step=1.0)
    val_unemp = st.slider("Unemployment Rate (%)", 0.0, 40.0, float(baseline_data['unemp']), step=0.1)
    val_debt = st.slider("Public Debt-to-GDP (%)", 0.0, 300.0, float(baseline_data['debtgdp']), step=1.0)

st.markdown("---")
run_prediction = st.button("EXECUTE AI PREDICTION PROTOCOL", type="primary", use_container_width=True)

if run_prediction:
    input_df = pd.DataFrame([[val_ycs, val_cg, val_cgd2, val_cgc, val_ycc, val_cpi, val_unemp, val_debt]], columns=features)
    risk_score = backend.predict_risk(model, input_df)
    shap_vals = backend.generate_shap_values(model, input_df)
    
    risk_label, gauge_color, alert_html = frontend.determine_risk_level(risk_score)
    st.markdown(alert_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns([1.2, 1])
    with res_col1: frontend.render_gauge(risk_score, gauge_color, risk_label)
    with res_col2: frontend.render_shap(shap_vals)
"""
}

# Write standard files
for filename, content in files_to_create.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"📄 Generated file: {filename}")

# 3. Generate Valid, Empty Jupyter Notebooks
# This JSON structure is required for VS Code to recognize the file as a valid notebook
notebook_template = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["*Paste the code for this stage of the pipeline here.*"]
        }
    ],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 5
}

notebooks = [
    "01_Raw_Data.ipynb",
    "02_Preprocessing.ipynb",
    "03_Algorithm_Training.ipynb",
    "04_Explainable_AI.ipynb"
]

for nb in notebooks:
    with open(nb, 'w', encoding='utf-8') as f:
        json.dump(notebook_template, f, indent=4)
    print(f"📓 Generated Notebook: {nb}")

print("\n✅ SUCCESS: Project workspace is fully built and assembled!")