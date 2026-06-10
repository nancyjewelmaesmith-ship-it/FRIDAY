import streamlit as st
import google.generativeai as genai
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# =====================================================================
# 1. CORE SYSTEM LAYOUT & LOCALIZATION
# =====================================================================
st.set_page_config(page_title="Enterprise Analytics Core", layout="wide")
st.title("📊 Quantitative Market Intelligence Platform")
st.write("Macroeconomic simulation suite calibrated for Qatar operations. Currency values scaled in PHP.")

# =====================================================================
# 2. SYSTEM ENGINE INITIALIZATION (MODERN PRODUCTION UPDATE)
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "FALLBACK_SECURE_VAULT"

genai.configure(api_key=api_key)

# We use Streamlit's resource cache so the model object doesn't recreate on every script rerun
@st.cache_resource
def load_generative_engine():
    try:
        # Shifted to gemini-2.0-flash-lite for maximum free-tier request headroom
        return genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite',
            system_instruction=(
                "You are a closed-loop proprietary financial logic system analyzing corporate data. "
                "Your function is to evaluate commercial ventures operating within the State of Qatar. "
                "All financial inputs and outputs are strictly denominated in Philippine Peso (PHP). "
                "Adopt an absolute, cold, data-dense, analytical corporate tone. "
                "Do not use conversational fillers. Output raw conclusions immediately."
            )
        )
    except Exception as e:
        return None

model = load_generative_engine()

# =====================================================================
# 3. EXPANDED SECTORIAL DATABASE (QATAR CONFIGURATION IN PHP)
# =====================================================================
INDUSTRIES = {
    "Food Industries": {
        "margin": 8.0, 
        "cac": 850.0, 
        "risk": "High cold-chain utility overhead during desert peak summers, extreme reliance on food import logistics, strict compliance with the Ministry of Public Health."
    },
    "Energy and Petrochemicals": {
        "margin": 18.0, 
        "cac": 28000.0, 
        "risk": "Heavy asset capital requirements, complex compliance with QatarEnergy distribution frameworks, high sensitivity to global LNG indexation changes."
    },
    "Real Estate & Property Management": {
        "margin": 25.0, 
        "cac": 55000.0, 
        "risk": "Localized oversupply mechanics in specific Lusail and The Pearl residential zones, sensitivity to shifts in foreign ownership residency thresholds."
    },
    "Construction & Contracting": {
        "margin": 6.0, 
        "cac": 12000.0, 
        "risk": "Raw material supply chain constraints, regulatory labor welfare framework costs, post-infrastructure pivot toward long-term maintenance contracts."
    },
    "Global Digital Media": {
        "margin": 35.0, 
        "cac": 1800.0, 
        "risk": "Compliance with the Qatar Media City regulatory framework, high expenditure for localized bilingual content (Arabic/English), reliance on global ad platform data."
    },
    "Hospitality & Luxury Tourism": {
        "margin": 15.0, 
        "cac": 9500.0, 
        "risk": "Significant seasonal demand drops during extreme summer heatwaves in Doha, high reliance on regional GCC tourism corridors and mega-events."
    },
    "Tech Consultancy & Cloud Services": {
        "margin": 40.0, 
        "cac": 4000.0, 
        "risk": "High compensation costs for certified bilingual software engineers, mandatory compliance with National Cyber Security Agency (NCSA) frameworks."
    },
    "Logistics & Import-Export": {
        "margin": 12.0, 
        "cac": 15000.0, 
        "risk": "Customs clearance timing variations at Hamad Port, high sensitivity to global marine freight price volatility affecting local distribution loops."
    }
}

# =====================================================================
# 4. TRANSPARENT DATA PERSISTENCE LAYER (EXPOSING LOGICAL ERRORS)
# =====================================================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(ttl="0d") 
    
    # Validation check for missing headers on completely empty sheets
    if existing_data.empty or len(existing_data.columns) < 3:
        st.sidebar.error("⚠️ Structural Error: Target Google Sheet lacks mandatory columns. Add 'Title', 'Type', and 'Amount' to Row 1.")
        is_cloud_connected = False
        ledger_records = []
    else:
        ledger_records = existing_data.to_dict(orient="records")
        is_cloud_connected = True
        st.sidebar.success("⚡ Connected to Google Drive Storage.")
except Exception as gsheets_err:
    is_cloud_connected = False
    st.sidebar.error(f"❌ Cloud Storage Offline: {gsheets_err}")
    st.sidebar.info("Reverted to local session fallback data container.")
    if 'fallback_ledger' not in st.session_state:
        st.session_state.fallback_ledger = []
    ledger_records = st.session_state.fallback_ledger

# =====================================================================
# 5. ENTERPRISE SUITE INTERFACE
# =====================================================================
tab1, tab2, tab3 = st.tabs(["📊 Sector Modeling Matrix", "📈 Capital Allocation Logic", "📒 Internal Ledger Vault"])

# --- TAB 1: SECTOR MODELING MATRIX ---
with tab1:
    st.header("Operational Parameter Analysis")
    selected_industry = st.selectbox("Select Target Economic Sector (Qatar Framework):", list(INDUSTRIES.keys()))
    baseline = INDUSTRIES[selected_industry]

    st.subheader(f"{selected_industry} Performance Benchmarks")
    col1, col2 = st.columns(2)
    col1.metric("Sector Net Margin Baseline", f"{baseline['margin']}%")
    col2.metric("Target Acquisition Cost (CAC)", f"{baseline['cac']:,.2f} PHP")
    st.warning(f"Market Risk Vector: {baseline['risk']}")

    st.subheader("Venture Deviations")
    user_margin_mod = st.number_input("Net Margin Modifier Deviation (+/- %):", value=0.0, step=1.0)
    user_cac_mod = st.number_input("CAC Allocation Adjustment (+/- PHP):", value=0.0, step=100.0)
    special_conditions = st.text_area("Input Localized Variables:")

    st.subheader("⚠️ Stress Testing Metrics")
    supply_chain_stress = st.slider("Global Supply Chain Delay Factor (%)", 0, 100, 0)
    local_rent_stress = st.slider("Regional Commercial Rent Escalation (%)", 0, 50, 0)

    if st.button("Run Quantitative Strategy Brief"):
        if not model or api_key == "FALLBACK_SECURE_VAULT":
            st.error("System Core Error: Authentication vector unmapped.")
        else:
            projected_margin = baseline["margin"] + user_margin_mod - (supply_chain_stress * 0.1)
            projected_cac = baseline["cac"] + user_cac_mod + (local_rent_stress * 30)
            
            prompt = f"""
            Execute financial audit for Qatar-based sector: {selected_industry}.
            OPERATIONAL DATA MATRICES (DENOMINATED IN PHP):
            - Benchmark Margin: {baseline['margin']}% | Modeled Margin: {projected_margin}%
            - Benchmark CAC: {baseline['cac']} PHP | Modeled CAC: {projected_cac} PHP
            - Stress Testing Parameters: Supply Chain Friction at {supply_chain_stress}%, Local Rent Hikes at {local_rent_stress}%
            - Local Target Variables: {special_conditions}
            
            Generate a brutal, completely objective appraisal of financial viability under these parameters. Format strictly using headers: [VIABILITY EVALUATION], [CAPITAL EFFICIENCY ASSESSMENT], [RISK MITIGATION DIRECTIVES].
            """
            with st.spinner("Processing Operational Matrices..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.1})
                    st.subheader("📋 Executive Strategic Briefing")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Audit Interrupted: {e}")

# --- TAB 2: CAPITAL ALLOCATION LOGIC ---
with tab2:
    st.header("Executive Asset Allocation Engine")
    st.write("Calculates structured investment deployment boundaries based on exact liquidity configurations.")
    
    current_investment = st.number_input("Liquid Capital Invested/Available (PHP):", min_value=0.0, value=800000.0, step=50000.0)
    current_earnings = st.number_input("Gross Retained Capital Earnings (PHP):", min_value=0.0, value=240000.0, step=10000.0)
    future_goal = st.text_input("Operational Scaling Milestone Target:")
    
    st.subheader("🛡️ Algorithmic Allocation Thresholds")
    if current_investment < 1500000:
        bracket = "Micro-Venture Preservation Mode"
        max_recommended_deployment = current_earnings * 0.25
        strategy_summary = "High liquidity reservation mandatory. Avoid long-term capital lockdowns."
    elif 1500000 <= current_investment <= 7500000:
        bracket = "Mid-Tier Scaling Growth Mode"
        max_recommended_deployment = current_earnings * 0.50
        strategy_summary = "Balanced re-investment viable. Expansion to secondary industrial zones allowed."
    else:
        bracket = "Macro Enterprise Dominance Mode"
        max_recommended_deployment = current_earnings * 0.75
        strategy_summary = "Aggressive capital deployment recommended. Capitalize on industrial scale efficiencies."

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Asset Bracket Classification", bracket)
    kpi2.metric("Max Calculated Capital Re-investment Cap", f"{max_recommended_deployment:,.2f} PHP")
    kpi3.metric("Liquidity Safety Margin Profile", f"{(current_investment + current_earnings - max_recommended_deployment):,.2f} PHP")
    st.info(f"System Baseline Directive: {strategy_summary}")

    if st.button("Generate Asset Directive"):
        if model and future_goal:
            prompt = f"""
            Analyze this corporate asset framework for a business operating in Qatar.
            PORTFOLIO DATA CONFIGURATION (PHP VALUES):
            - Asset Category: {bracket}
            - Current Pool Liquidity: {current_investment} PHP
            - Liquid Retained Earnings: {current_earnings} PHP
            - Calculated Re-investment Boundary: {max_recommended_deployment} PHP
            - Target Operational Objective: {future_goal}
            
            Deliver a direct, numbers-focused capital allocation decree. Specify precisely how much of the retained capital to lock down as protective operational runway versus how much to allocate directly toward achieving the '{future_goal}'. Do not use casual or descriptive language.
            """
            with st.spinner("Processing Portfolio Matrix..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.1})
                    st.subheader("📋 Capital Allocation Directive")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Portfolio Engine Failure: {e}")

# --- TAB 3: INTERNAL LEDGER VAULT ---
with tab3:
    st.header("Financial Transaction System Ledger")
    st.write("All entries register directly to the secure cloud storage layer.")
    
    with st.form("ledger_secure_form", clear_on_submit=True):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            entry_title = st.text_input("Transaction Line Item Nomenclature")
        with col_t2:
            entry_type = st.selectbox("Accounting Allocation Class", ["Revenue", "Expense"])
        with col_t3:
            entry_amount = st.number_input("Transaction Financial Value (PHP)", min_value=0.0, value=0.0, step=500.0)
        
        submitted = st.form_submit_button("Commit Transaction to Cloud Storage")
        if submitted and entry_title:
            new_entry = {
                "Title": entry_title,
                "Type": entry_type,
                "Amount": entry_amount if entry_type == "Revenue" else -entry_amount
            }
            
            if not is_cloud_connected:
                st.session_state.fallback_ledger.append(new_entry)
                st.warning("Storage is operating locally. Data committed to volatile session memory.")
                st.rerun()
            else:
                try:
                    current_df = conn.read(ttl="0d")
                    new_row_df = pd.DataFrame([new_entry])
                    updated_df = pd.concat([current_df, new_row_df], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Transaction successfully transmitted to cloud file array.")
                    st.rerun()
                except Exception as write_err:
                    st.error(f"Write Transaction Rejected by Target Storage Host: {write_err}")

    if ledger_records:
        df_active = pd.DataFrame(ledger_records)
        df_display = df_active.copy()
        df_display['Amount'] = df_display['Amount'].map(lambda val: f"{val:,.2f} PHP")
        st.dataframe(df_display, use_container_width=True)
        
        net_balance = df_active['Amount'].sum()
        if net_balance >= 0:
            st.success(f"📈 **Net Balance Profile: {net_balance:,.2f} PHP**")
        else:
            st.error(f"📉 **Net Deficit Position: {net_balance:,.2f} PHP**")
