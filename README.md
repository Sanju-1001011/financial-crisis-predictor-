# ⚡ Systemic Macroeconomic Early Warning System (EWS)

A production-grade, interactive financial telemetry dashboard and machine learning early warning system designed to detect systemic macroeconomic risks across global economies. 

---

## 🚀 System Architecture & Key Features

* **Advanced Signal Processing:** Integrates historical datasets (such as the Jordà-Schularick-Taylor Macrohistory Database) processed via Hodrick-Prescott filters to strip out noise and isolate structural imbalances.
* **Cost-Sensitive Machine Learning:** Powered by **XGBoost** utilizing custom class weighting (`scale_pos_weight`) to overcome extreme class imbalance and aggressively penalize missed crisis events. Evaluated using **PR-AUC** rather than misleading baseline accuracy metrics.
* **Explainable AI (XAI):** Features transparent, custom-styled **TreeSHAP** waterfall charts embedded directly into the UI to break down feature contributions and eliminate the economic "black-box" problem.
* **Real-Time Market Telemetry:** Dynamically streams live global market data (VIX, 10-Year US Treasury Yields, Brent Crude Oil, and FX rates) via the **Yahoo Finance API (`yfinance`)**.
* **Interactive HUD Interface:** Built using **Streamlit**, featuring high-contrast tactical design elements, global risk heatmaps, interactive threat matrices with callback routing, and scenario stress-testing tools.

---

## 🛠️ Project Structure

```text
├── 01_Raw_Data.ipynb             # Raw JST macrohistory data ingestion
├── 02_Preprocessing.ipynb        # Signal processing & Hodrick-Prescott filtering
├── 03_Algorithm_Training.ipynb   # XGBoost training, cost-tuning & PR-AUC evaluation
├── 04_Explainable_AI.ipynb       # SHAP value extraction & interpretability logic
├── app.py                        # Main Streamlit application entry point & routing
├── backend.py                    # Data pipelines, ML predictions & Yahoo Finance API
├── frontend.py                   # HUD custom CSS, charts, and interactive UI views
└── requirements.txt              # Project dependencies


Installation & Execution
Clone the repository and navigate to the project  directory:

Bash
cd brand-new-folder
Install the required dependencies:

Bash
pip install -r requirements.txt
Launch the live Streamlit command terminal:

Bash
streamlit run app.py
or 
python -m streamlit run app.py

if you found error then install requirements.txt :
pip install -r requirements.txt

or missing yfinance then:
pip install yfinance

again :



Bash
streamlit run app.py
or 
python -m streamlit run app.py


Save both files, and your project is fully documented, polished, and ready for deployment or presentation!
https://github.com/Sanju-1001011/financial-crisis-predictor-/blob/92219a5385aa0e5ceecad81e8b0c8c449fbb9a4b/financial%20crisis.png
