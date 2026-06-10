import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import numpy as np

# =====================================================================
# 1. CORE SYSTEM LAYOUT & LOCALIZATION
# =====================================================================
st.set_page_config(page_title="Enterprise Analytics Core", layout="wide")
st.title("📊 Quantitative Market Intelligence Platform (Friday v2)")
st.write("Macroeconomic simulation suite calibrated for Qatar operations. Currency values scaled in PHP.")

# =====================================================================
# 2. LOCAL DATA STORAGE ENGINE (CSV BACKEND)
# =====================================================================
CSV_FILE_PATH = "ledger.csv"

if not os.path.exists(CSV_FILE_PATH):
    initial_df = pd.DataFrame(columns=["Title", "Type", "Amount"])
    initial_df.to_csv(CSV_FILE_PATH, index=False)

def read_local_ledger():
    try:
        return pd.read_csv(CSV_FILE_PATH)
    except Exception:
        return pd.DataFrame(columns=["Title", "Type", "Amount"])

def append_to_local_ledger(new_row_dict):
    current_df = read_local_ledger()
    new_row_df = pd.DataFrame([new_row_dict])
    updated_df = pd.concat([current_df, new_row_df], ignore_index=True)
    updated_df.to_csv(CSV_FILE_PATH, index=False)

ledger_df = read_local_ledger()
ledger_records = ledger_df.to_dict(orient="records")
net_balance_global = ledger_df['Amount'].sum() if not ledger_df.empty else 0.0
st.sidebar.success(f"💾 Local Database Online. Vault Pool: {net_balance_global:,.2f} PHP")

# =====================================================================
# 3. SYSTEM ENGINE INITIALIZATION (CACHED TO PROTECT QUOTA)
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "FALLBACK_SECURE_VAULT"

genai.configure(api_key=api_key)

@st.cache_resource
def load_generative_engine():
    try:
        return genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite',
            system_instruction=(
                "You are a closed-loop proprietary financial logic system analyzing corporate data. "
                "Your function is to evaluate commercial ventures operating within the State of Qatar. "
                "All financial inputs and outputs are strictly denominated in Philippine Peso (PHP). "
                "Adopt an absolute, cold, data-dense, analytical corporate tone. "
                "CRITICAL: Do not use any conversational fillers, greetings, or sign-offs. "
                "Output raw executive conclusions and numerical risk assessments immediately."
            )
        )
    except Exception:
        return None

model = load_generative_engine()

# =====================================================================
# 4. EXPANDED SECTORIAL DATABASE (QATAR CONFIGURATION IN PHP)
# =====================================================================
INDUSTRIES = {
    "Food Industries": {"margin": 8.0, "cac": 850.0, "risk": "High cold-chain utility overhead during desert peak summers, extreme reliance on food import logistics."},
    "Energy and Petrochemicals": {"margin": 18.0, "cac": 28000.0, "risk": "Heavy asset capital requirements, complex compliance with QatarEnergy distribution frameworks."},
    "Real Estate & Property Management": {"margin": 25.0, "cac": 55000.0, "risk": "Localized oversupply mechanics in specific Lusail and The Pearl residential zones."},
    "Construction & Contracting": {"margin": 6.0, "cac": 12000.0, "risk": "Raw material supply chain constraints, regulatory labor welfare framework costs."},
    "Global Digital Media": {"margin": 35.0, "cac": 1800.0, "risk": "Compliance with Qatar Media City regulatory framework, high expenditure for bilingual content."},
    "Hospitality & Luxury Tourism": {"margin": 15.0, "cac": 9500.0, "risk": "Significant seasonal demand drops during extreme summer heatwaves in Doha."},
    "Tech Consultancy & Cloud Services": {"margin": 40.0, "cac": 4000.0, "risk": "High compensation costs for software engineers, compliance with NCSA frameworks."},
    "Logistics & Import-Export": {"margin": 12.0, "cac": 15000.0, "risk": "Customs clearance timing variations at Hamad Port, high freight volatility."}
}

# =====================================================================
# 5. ENTERPRISE SUITE INTERFACE
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sector Modeling Matrix", 
    "📈 Capital Allocation Logic", 
    "📒 Internal Ledger Vault",
    "⏳ Burn Rate & Runway Analytics"
])

# --- TAB 1: SECTOR MODELING MATRIX ---
with tab1:
    st.header("Operational Parameter Analysis")
    selected_industry = st.selectbox("Select Target Economic Sector (Qatar Framework):", list(INDUSTRIES.keys()))
    baseline = INDUSTRIES[selected_industry]

    col1, col2 = st.columns(2)
    col1.metric("Sector Net Margin Baseline", f"{baseline['margin']}%")
    col2.metric("Target Acquisition Cost (CAC)", f"{baseline['cac']:,.2f} PHP")
    st.warning(f"Market Risk Vector: {baseline['risk']}")

    user_margin_mod = st.number_input("Net Margin Modifier Deviation (+/- %):", value=0.0, step=1.0)
    user_cac_mod = st.number_input("CAC Allocation Adjustment (+/- PHP):", value=0.0, step=100.0)
    special_conditions = st.text_area("Input Localized Variables:")
    supply_chain_stress = st.slider("Global Supply Chain Delay Factor (%)", 0, 100, 0)
    local_rent_stress = st.slider("Regional Commercial Rent Escalation (%)", 0, 50, 0)

    if st.button("Run Quantitative Strategy Brief"):
        if not model or api_key == "FALLBACK_SECURE_VAULT":
            st.error("⚠️ AI Engine Offline. Form-based modeling calculations above remain fully operational.")
        else:
            projected_margin = baseline["margin"] + user_margin_mod - (supply_chain_stress * 0.1)
            projected_cac = baseline["cac"] + user_cac_mod + (local_rent_stress * 30)
            
            prompt = f"Execute financial audit for Qatar-based sector: {selected_industry}. Data: Margin {projected_margin}%, CAC {projected_cac} PHP. Conditions: {special_conditions}."
            with St.spinner("Processing Operational Matrices..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.1})
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Quota Limit Hit: {e}")

# --- TAB 2: CAPITAL ALLOCATION LOGIC ---
with tab2:
    st.header("Executive Asset Allocation Engine")
    current_investment = st.number_input("Liquid Capital Invested/Available (PHP):", min_value=0.0, value=800000.0, step=50000.0)
    current_earnings = st.number_input("Gross Retained Capital Earnings (PHP):", min_value=0.0, value=240000.0, step=10000.0)
    future_goal = st.text_input("Operational Scaling Milestone Target:")
    
    if current_investment < 1500000:
        bracket, max_deployment = "Micro-Venture Preservation Mode", current_earnings * 0.25
    elif 1500000 <= current_investment <= 7500000:
        bracket, max_deployment = "Mid-Tier Scaling Growth Mode", current_earnings * 0.50
    else:
        bracket, max_deployment = "Macro Enterprise Dominance Mode", current_earnings * 0.75

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Asset Bracket Classification", bracket)
    kpi2.metric("Max Recommended Deployment", f"{max_deployment:,.2f} PHP")
    kpi3.metric("Liquidity Safety Margin Profile", f"{(current_investment + current_earnings - max_deployment):,.2f} PHP")

# --- TAB 3: INTERNAL LEDGER VAULT ---
with tab3:
    st.header("Financial Transaction System Ledger")
    with st.form("ledger_secure_form", clear_on_submit=True):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1: entry_title = st.text_input("Transaction Line Item Nomenclature")
        with col_t2: entry_type = st.selectbox("Accounting Allocation Class", ["Revenue", "Expense"])
        with col_t3: entry_amount = st.number_input("Transaction Financial Value (PHP)", min_value=0.0, value=0.0, step=500.0)
        
        if st.form_submit_button("Commit Transaction to CSV Storage") and entry_title:
            new_entry = {"Title": entry_title, "Type": entry_type, "Amount": entry_amount if entry_type == "Revenue" else -entry_amount}
            append_to_local_ledger(new_entry)
            st.rerun()

    if ledger_records:
        df_active = pd.DataFrame(ledger_records)
        st.dataframe(df_active, use_container_width=True)

# --- TAB 4: NEW RUNWAY & BURN RATE ANALYTICS (0% API USAGE) ---
with tab4:
    st.header("⏳ Local Runway & Burn Rate Analytics")
    st.write("Calculates working capital survival metrics without querying cloud architectures.")
    
    # 1. Input parameters
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        monthly_rent = st.number_input("Monthly Office/Infrastructure Rent (PHP):", value=15000.0, step=1000.0)
    with col_r2:
        monthly_payroll = st.number_input("Monthly Operations/Contractor Payroll (PHP):", value=45000.0, step=5000.0)
    with col_r3:
        monthly_marketing = st.number_input("Monthly Customer Acquisition Spend (PHP):", value=10000.0, step=1000.0)
        
    total_monthly_burn = monthly_rent + monthly_payroll + monthly_marketing
    
    # 2. Mathematical Calculations
    st.subheader("Runway Allocation Summary")
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Total Monthly Operating Burn", f"{total_monthly_burn:,.2f} PHP")
    rc2.metric("Available Capital Reserves (From Ledger)", f"{net_balance_global:,.2f} PHP")
    
    if net_balance_global <= 0:
        rc3.metric("Calculated Lifespan Runway", "0.0 Months", delta="CRITICAL DEFICIT", delta_color="inverse")
        st.error("⚠️ System alert: Capital pool exhausted or in deficit position. Immediate cash injection required.")
    elif total_monthly_burn == 0:
        rc3.metric("Calculated Lifespan Runway", "Infinite", delta="Zero Burn", delta_color="normal")
    else:
        months_runway = net_balance_global / total_monthly_burn
        delta_label = "Healthy Profile" if months_runway >= 6 else "High Capital Exhaustion Risk"
        rc3.metric("Calculated Lifespan Runway", f"{months_runway:.1f} Months", delta=delta_label, delta_color="normal" if months_runway >= 6 else "inverse")
        
        # 3. Dynamic Forecasting Line Chart
        st.subheader("Capital Depletion Timeline Simulation")
        projection_months = max(int(np.ceil(months_runway * 1.5)), 6)
        timeline = list(range(0, projection_months + 1))
        
        balances = []
        for m in timeline:
            current_projected = net_balance_global - (m * total_monthly_burn)
            balances.append(max(current_projected, 0.0))
            
        chart_df = pd.DataFrame({"Month": timeline, "Projected Capital Pool (PHP)": balances})
        st.line_chart(chart_df.set_index("Month"))
