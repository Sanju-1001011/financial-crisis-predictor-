import streamlit as st
import pandas as pd
from datetime import datetime
import backend
import frontend
import os # Make sure to add this at the very top with your other imports!

# 1. System Initialization
st.set_page_config(page_title="AI Risk Monitor", layout="wide", initial_sidebar_state="expanded")
frontend.apply_custom_css()
frontend.render_ticker()



# 2. Data Logger (Persistent Local Storage)
HISTORY_FILE = "prediction_history.csv"

if 'history' not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        # Load previous history if the file exists
        st.session_state.history = pd.read_csv(HISTORY_FILE)
    else:
        # Create a blank slate if it's the first time running
        st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Country', 'Forecast Year', 'Risk Score', 'Status'])
# 3. Load Cores
@st.cache_data
def fetch_data(): return backend.load_data()
@st.cache_resource
def fetch_model(): return backend.load_model()

try:
    df, features = fetch_data()
    model = fetch_model()
except Exception as e:
    st.error("SYSTEM ERROR: Core components offline. Run notebooks first.")
    st.stop()

# ==========================================
# SIDEBAR CONTROL PANEL
# ==========================================

st.sidebar.markdown("<h2 style='text-align: center;'>⚡ COMMAND MENU</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Initialize default page selection if not present
if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = "1 ▸ Main Dashboard (Global View)"

navigation = st.sidebar.radio(
    "SELECT DISPLAY MODE:",
    [
        "🏠 Home",
        "0 ▸ Financial Crisis",
        "1 ▸ Main Dashboard (Global View)",
        "2 ▸ Prediction Terminal (Diagnostics)",
        "3 ▸ History & Reports"
    ],
    key="nav_radio"
)

st.sidebar.markdown("---")

# Visual Alarm Trigger (Reads from latest history)
if not st.session_state.history.empty:
    latest_risk = st.session_state.history.iloc[-1]['Risk Score']
    if latest_risk >= 60:
        st.sidebar.markdown("""
        <div style='background-color: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 0 15px #ef4444;'>
            <span class='pulse-red' style='margin:0 auto;'></span><br>
            <b style='color: #ef4444; font-size: 20px; text-shadow: 0 0 5px #ef4444;'>CRITICAL ALARM ACTIVE</b><br>
            <span style='color: white; font-size: 12px;'>High systemic risk detected in recent scan.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div style='text-align: center;'><span class='solid-green'></span><b style='color: #10b981;'>SYSTEM SECURE</b></div>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="system-status-card">
  <div class="system-status-label">SYSTEM STATUS</div>
  <div class="system-status-line"><span></span>All Systems Operational</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# ROUTING LOGIC (MULTIPLEXER)
# ==========================================
# --- MODE HOME: CINEMATIC LANDING PAGE (natural background + hero title) ---
if navigation == "🏠 Home":
    frontend.apply_home_style()
    st.markdown("""
    <div class="home-hero">
        <div class="home-title">
            <span>FINANCIAL</span>
            <span>CRISIS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MODE 0: FINANCIAL CRISIS ---
if "Financial Crisis" in navigation:
    # Custom HTML Header with a Flashing "LIVE" indicator simulating a real-time feed
    st.markdown("""<div style="position: relative; padding-top: 1rem; margin-bottom: 2.5rem; z-index: 2;">
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
    <h1 style="font-family: 'Inter', sans-serif; font-size: 42px; font-weight: 700; color: #FFFFFF; margin: 0; padding: 0;">
        Financial Crisis Overview
    </h1>
    <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #ef4444; padding: 4px 12px; border-radius: 20px; font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 11px; letter-spacing: 1px; animation: livePulse 1.5s infinite;">
        <span style="display: inline-block; width: 6px; height: 6px; background: #ef4444; border-radius: 50%; margin-right: 5px; margin-bottom: 1px;"></span>
        LIVE TELEMETRY
    </div>
</div>
<div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
    <p style="font-family: 'Inter', sans-serif; font-size: 16px; color: rgba(220, 225, 240, 0.85); margin: 0;">
        Real-time macro stress signals monitored across global markets.
    </p>
    <p style="font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #10b981; margin: 0;">
        [ SYSTEM AUTO-REFRESHING: EVERY 60s ]
    </p>
</div>
<div style="width: 55px; height: 4px; background: #8B5CFF; border-radius: 2px; margin-bottom: 25px;"></div>
<div style="font-family: 'Inter', 'Segoe UI', sans-serif; font-size: clamp(50px, 5vw, 85px); font-weight: 900; letter-spacing: 5px; text-transform: uppercase; color: rgba(230, 232, 255, 0.10); line-height: 1; pointer-events: none;">
    FINANCIAL CRISIS
</div>
<style>
    @keyframes livePulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
</style>
</div>""", unsafe_allow_html=True)

    live_data = backend.fetch_live_telemetry()
    frontend.render_financial_crisis(live_data)
  
# --- MODE 1: MAIN DASHBOARD ---
elif "Main Dashboard" in navigation:
    st.markdown(
        "<div class='hud-section-label' style='margin-bottom:0.5rem;'>Global Macroeconomic Stability Overview</div>",
        unsafe_allow_html=True
    )
    st.title("Main Command Dashboard")
    
    # Calculate global risk
    global_risk_df = backend.calculate_global_risk(df, model, features)
    
    # Extract and render the Top 3 Highest Risk Economies Threat Matrix
    top_3_risks = global_risk_df.sort_values(by="Risk Score", ascending=False).head(3)
    frontend.render_threat_matrix(top_3_risks)
    
    # Render the global map directly below the threat matrix
    frontend.render_world_map(global_risk_df)
    
    st.info("System Online. Select 'Prediction Terminal' from the sidebar to run isolated stress tests on specific economies.")

# --- MODE 2: PREDICTION TERMINAL ---
elif "Prediction Terminal" in navigation:
    st.markdown(
        "<div class='hud-section-label' style='margin-bottom:0.5rem;'>AI Crisis Prediction System — Diagnostic Mode</div>",
        unsafe_allow_html=True
    )
    st.title("AI Crisis Prediction Terminal")
    st.markdown(
        "<p style='color:rgba(174,181,201,0.72);font-size:14px;margin-top:-0.4rem;margin-bottom:1.6rem;'>"
        "Isolated economy stress-testing and diagnostic telemetry.</p>",
        unsafe_allow_html=True
    )

    # ── Economy selector + forecast year ─────────────────────────────────────
    st.markdown(
        "<div class='hud-section-label'>Target Economy &amp; Projection Window</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='pt-glass-panel'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.4, 1])
    with col1:
        countries_list = sorted(df['country'].unique())
        
        # Check if we arrived here by clicking a Threat Matrix button
        default_index = 0
        if 'target_country' in st.session_state and st.session_state.target_country in countries_list:
            default_index = countries_list.index(st.session_state.target_country)
            
        country = st.selectbox("Select Target Economy:", countries_list, index=default_index)
    with col2:
        future_year = st.slider("Forecast Year:", 2025, 2060, 2030)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Data feed status panel ────────────────────────────────────────────────
    country_history = df[df['country'] == country].sort_values('year')
    latest_year = int(country_history['year'].max())
    baseline_data = country_history.iloc[-1]
    frontend.render_data_feed_panel(latest_year, future_year)

    # ── Economic Health Sliders (4×2 grid of individual glass cards) ─────────
    frontend.render_slider_section_label()

    slider_specs = [
        ("Interest Rate Gap",              -10.0, 10.0,  float(baseline_data['yield_curve_slope']), 0.1),
        ("Total Debt vs Economy (%)",        0.0, 300.0, float(baseline_data['credit_gdp']),        1.0),
        ("Debt Growth Speed",              -50.0, 50.0,  float(baseline_data['credit_gdp_diff2']),  0.5),
        ("Abnormal Debt Spikes",           -50.0, 50.0,  float(baseline_data['credit_gdp_cycle']),  0.5),
        ("Abnormal Interest Rate Shifts",  -10.0, 10.0,  float(baseline_data['yield_curve_cycle']), 0.1),
        ("Inflation (Prices)",               0.0, 500.0, float(baseline_data['cpi']),              1.0),
        ("Unemployment Rate (%)",             0.0, 40.0,  float(baseline_data['unemp']),            0.1),
        ("Government Debt (%)",               0.0, 300.0, float(baseline_data['debtgdp']),          1.0),
    ]

    slider_values = []
    for row in range(2):
        grid_cols = st.columns(4)
        for i in range(4):
            label, mn, mx, val, step = slider_specs[row * 4 + i]
            with grid_cols[i]:
                st.markdown("<div class='slider-card'>", unsafe_allow_html=True)
                slider_values.append(st.slider(label, mn, mx, val, step))
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Run button ────────────────────────────────────────────────────────────
    st.markdown(
        "<div class='hud-section-label' style='margin-bottom:0.8rem; margin-top:1.5rem;'>Execute Stress Simulation</div>",
        unsafe_allow_html=True
    )
    run_prediction = st.button("RUN AI PREDICTION", type="primary", use_container_width=True)

    if run_prediction:
        input_df = pd.DataFrame([slider_values], columns=features)
        risk_score = backend.predict_risk(model, input_df)
        shap_vals  = backend.generate_shap_values(model, input_df)

        risk_label, gauge_color, alert_html = frontend.determine_risk_level(risk_score)

       # LOG TO HISTORY
        new_entry = pd.DataFrame([{
            'Timestamp':   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Country':     country,
            'Forecast Year': future_year,
            'Risk Score':  round(risk_score, 2),
            'Status':      risk_label
        }])
        
        st.session_state.history = pd.concat(
            [st.session_state.history, new_entry], ignore_index=True
        )
        
        # Save to hard drive immediately so it never gets lost
        st.session_state.history.to_csv(HISTORY_FILE, index=False)

        st.markdown(alert_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='pt-glass-panel'>", unsafe_allow_html=True)
        frontend.render_gauge(risk_score, gauge_color, risk_label)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div class='pt-glass-panel'>", unsafe_allow_html=True)
        frontend.render_shap(shap_vals)
        st.markdown("</div>", unsafe_allow_html=True)

# --- MODE 3: HISTORY & REPORTS ---
elif "History & Reports" in navigation:
    st.title("Telemetry History & Data Export")
    st.markdown("Review previous stress-test simulations and export official reports.")
    
    if st.session_state.history.empty:
        frontend.render_warning_no_data()
    else:
        st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
        
        # Convert History to CSV for Download
        csv = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ DOWNLOAD OFFICIAL CSV REPORT",
            data=csv,
            file_name=f"macro_risk_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            type="primary"
        )