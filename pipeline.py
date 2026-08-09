import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Macro Crisis Early Warning System", layout="wide")

st.title("🚨 Systemic Macroeconomic Early Warning System")
st.markdown("This dashboard leverages **Digital Signal Processing** and **Asymmetric Cost-Sensitive Learning** to predict financial crises.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_signals.csv")
    features = ['yield_curve_slope', 'credit_gdp', 'credit_gdp_diff2', 'credit_gdp_cycle', 'yield_curve_cycle', 'cpi', 'unemp', 'debtgdp']
    for col in features:
        df[col] = df[col].fillna(df[col].median())
    return df, features

df, features = load_data()

@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    model.load_model("models/xgboost_crisis_model.json")
    return model

model = load_model()

# --- Sidebar Configuration ---
st.sidebar.header("System Controls")
mode = st.sidebar.radio("Select Operating Mode:", [
    "Historical Backtesting", 
    "Live Data Forecasting",
    "Batch Upload (Future Projections)",
    "Auto-Forecast Future (AI Extension)"
])

st.sidebar.markdown("---")
sample_input = None
display_title = ""

# ==========================================
# MODE 1: HISTORICAL BACKTESTING
# ==========================================
if mode == "Historical Backtesting":
    st.sidebar.subheader("Historical Filters")
    country = st.sidebar.selectbox("Select Country:", sorted(df['country'].unique()))
    year = st.sidebar.slider("Select Year:", int(df['year'].min()), int(df['year'].max()), 2007)
    
    country_df = df[(df['country'] == country) & (df['year'] == year)]
    
    if not country_df.empty:
        sample_input = country_df[features]
        display_title = f"Historical Analysis: {country} ({year})"
        
        st.subheader("Historical Signal Processing Trends")
        chart_df = df[df['country'] == country].set_index('year')
        st.line_chart(chart_df[['credit_gdp', 'credit_gdp_cycle']])
        st.markdown("---")
    else:
        st.warning("No data available for the selected year and country.")

# ==========================================
# MODE 2: LIVE DATA FORECASTING
# ==========================================
elif mode == "Live Data Forecasting":
    st.sidebar.subheader("Manual Data Entry (Live Signals)")
    
    manual_ycs = st.sidebar.number_input("Yield Curve Slope (%)", value=0.5)
    manual_cg = st.sidebar.number_input("Credit-to-GDP (%)", value=100.0)
    manual_cgd2 = st.sidebar.number_input("2-Year Credit Shift", value=2.0)
    manual_cgc = st.sidebar.number_input("Credit Cycle (HP Filtered)", value=0.0)
    manual_ycc = st.sidebar.number_input("Yield Cycle (HP Filtered)", value=0.0)
    manual_cpi = st.sidebar.number_input("CPI (Inflation Level)", value=110.0)
    manual_unemp = st.sidebar.number_input("Unemployment Rate (%)", value=5.0)
    manual_debt = st.sidebar.number_input("Public Debt-to-GDP (%)", value=60.0)
    
    sample_input = pd.DataFrame([[
        manual_ycs, manual_cg, manual_cgd2, manual_cgc, 
        manual_ycc, manual_cpi, manual_unemp, manual_debt
    ]], columns=features)
    
    display_title = "Live Forecasting Analysis (Custom Data)"

# ==========================================
# MODE 3: BATCH UPLOAD
# ==========================================
elif mode == "Batch Upload (Future Projections)":
    st.sidebar.subheader("Upload Future Data")
    
    # Template Generator
    template_df = pd.DataFrame({
        'year': [2026, 2027, 2028, 2029, 2030],
        'country': ['MyCountry'] * 5,
        'yield_curve_slope': [0.5, 0.4, 0.1, -0.2, -1.0],
        'credit_gdp': [100.0, 102.0, 105.0, 110.0, 115.0],
        'credit_gdp_diff2': [2.0, 2.5, 3.5, 5.0, 7.0],
        'credit_gdp_cycle': [0.0, 0.2, 0.5, 1.2, 2.0],
        'yield_curve_cycle': [0.0, -0.1, -0.4, -0.8, -1.5],
        'cpi': [110.0, 112.0, 115.0, 120.0, 125.0],
        'unemp': [5.0, 5.1, 5.4, 6.0, 7.5],
        'debtgdp': [60.0, 62.0, 65.0, 70.0, 75.0]
    })
    csv_template = template_df.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button(label="📥 Download CSV Template", data=csv_template, file_name='future_template.csv', mime='text/csv')
    st.sidebar.markdown("---")
    
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            future_df = pd.read_csv(uploaded_file)
            st.write("### Future Projections Data (Uploaded)")
            st.dataframe(future_df)
            
            predictions = model.predict_proba(future_df[features])[:, 1]
            future_df['Predicted_Crisis_Probability'] = predictions * 100
            
            st.markdown("---")
            st.subheader("Future Crisis Risk Forecast")
            if 'year' in future_df.columns:
                st.line_chart(future_df.set_index('year')['Predicted_Crisis_Probability'])
            else:
                st.line_chart(future_df['Predicted_Crisis_Probability'])
        except Exception as e:
            st.error(f"Error reading file: {e}")

# ==========================================
# MODE 4: AI AUTO-FORECAST (NEW EXTENSION)
# ==========================================
elif mode == "Auto-Forecast Future (AI Extension)":
    st.sidebar.subheader("AI Time-Series Extension")
    st.sidebar.markdown("Automatically forecast economic signals into the future using historical dataset trends.")
    
    country = st.sidebar.selectbox("Select Country to Forecast:", sorted(df['country'].unique()))
    future_years = st.sidebar.slider("Forecast Horizon (Years into future):", 1, 30, 10)
    
    if st.sidebar.button("Generate AI Future Forecast"):
        country_df = df[df['country'] == country].sort_values('year')
        
        if not country_df.empty:
            last_year = int(country_df['year'].max())
            st.subheader(f"AI Automated Forecast: {country} ({last_year + 1} - {last_year + future_years})")
            
            with st.spinner('Training time-series models on historical data...'):
                future_dates = list(range(last_year + 1, last_year + future_years + 1))
                forecast_df = pd.DataFrame({'year': future_dates, 'country': country})
                
                # 1. Forecast every economic feature independently
                for col in features:
                    ts_data = country_df[col].values
                    try:
                        # Holt-Winters Exponential Smoothing to extract and project the trend
                        hw_model = ExponentialSmoothing(ts_data, trend='add', initialization_method="estimated").fit()
                        forecast_df[col] = hw_model.forecast(future_years)
                    except:
                        forecast_df[col] = [ts_data[-1]] * future_years
                
                st.write("### AI-Generated Macroeconomic Projections")
                st.dataframe(forecast_df.set_index('year')[features])
                
                # 2. Feed the forecasted signals into the XGBoost classifier
                predictions = model.predict_proba(forecast_df[features])[:, 1]
                forecast_df['Predicted_Crisis_Probability'] = predictions * 100
                
                st.markdown("---")
                st.subheader("Crisis Risk Forecast (Historical + Future Projection)")
                
                # 3. Combine Historical and Future predictions into one seamless timeline chart
                historical_probs = model.predict_proba(country_df[features])[:, 1] * 100
                hist_plot_df = pd.DataFrame({'Year': country_df['year'], 'Risk Probability (%)': historical_probs})
                fut_plot_df = pd.DataFrame({'Year': forecast_df['year'], 'Risk Probability (%)': forecast_df['Predicted_Crisis_Probability']})
                
                combined_plot = pd.concat([hist_plot_df, fut_plot_df]).set_index('Year')
                st.line_chart(combined_plot['Risk Probability (%)'])
                
                # 4. Crisis Warning Trigger
                max_risk = forecast_df['Predicted_Crisis_Probability'].max()
                peak_year = forecast_df.loc[forecast_df['Predicted_Crisis_Probability'].idxmax(), 'year']
                
                if max_risk > 50:
                    st.error(f"⚠️ HIGH RISK ALERT: The AI forecasts a systemic crisis peaking around {int(peak_year)} with a {max_risk:.1f}% probability based on current historical trajectories!")
                else:
                    st.success(f"✅ LOW RISK: The automated forecast predicts economic stability for {country} through {last_year + future_years}.")

# ==========================================
# RENDER SINGLE-ROW MODES (Modes 1 & 2)
# ==========================================
if sample_input is not None:
    st.subheader(display_title)
    
    prob = model.predict_proba(sample_input)[0][1]
    col1, col2 = st.columns(2)
    col1.metric("System Status", "ONLINE")
    col2.metric("Predicted Systemic Crisis Risk", f"{prob*100:.1f}%")
    
    if prob > 0.5:
        st.error("⚠️ HIGH RISK ALERT: System detects high probability of impending instability!")
    else:
        st.success("✅ LOW RISK: Economic signals remain within stable operating parameters.")
        
    st.markdown("---")
    st.subheader("AI Decision Logic (SHAP Feature Importance)")
    
    explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")
    shap_val = explainer(sample_input)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    shap.plots.waterfall(shap_val[0], show=False)
    st.pyplot(fig)