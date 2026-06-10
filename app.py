import streamlit as st
import google.generativeai as genai
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# =====================================================================
# 1. ENTERPRISE APPLICATION CONFIGURATION & LOCALIZATION
# =====================================================================
st.set_page_config(page_title="F.R.I.D.A.Y. Market Engine", layout="wide")
st.title("📊 F.R.I.D.A.Y. Macroeconomic Intelligence Suite")
st.write("State-backed economic modeling calibrated for Doha and localized Qatari investment zones.")

# =====================================================================
# 2. DISCRETE INTELLIGENCE SYSTEM INITIALIZATION
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "FALLBACK_SECURE_VAULT"

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=(
            "You are the F.R.I.D.A.Y. Core Analytics Engine, a proprietary, quantitative financial logic system. "
            "You evaluate commercial data strictly within the legal and economic framework of the State of Qatar. "
            "Adopt a cold, ultra-professional, rigorous corporate tone. "
            "ABSOLUTELY PROHIBITED: Do not say 'Hello', 'Sure', 'Hope this helps', or use any conversational conversational filler. "
            "Do not sign off with a name. Output raw, deeply dense corporate strategy and bulletproof risk matrices immediately."
        )
    )
except Exception as e:
    st.error(f"System Link Interrupted: {e}")
    model = None

# =====================================================================
# 3. QATARI SECTORIAL SYSTEM DATA (ANALYTICAL BASELINES IN QAR)
# =====================================================================
# Calibrated against local industrial parameters, utility structures, and rent pricing metrics in Qatar
INDUSTRIES = {
    "Food Industries": {
        "margin": 8.0, 
        "cac": 55.0, 
        "risk": "High cold-chain utility overhead during desert peak summers, extreme reliance on food import logistics, compliance with the Ministry of Public Health."
    },
    "Energy and Petrochemicals": {
        "margin": 18.0, 
        "cac": 1800.0, 
        "risk": "Heavy asset capital requirements, complex compliance with QatarEnergy distribution frameworks, sensitivity to global LNG indexation changes."
    },
    "Real Estate": {
        "margin": 25.0, 
        "cac": 3500.0, 
        "risk": "Localized oversupply mechanics in specific Lusail/The Pearl residential zones, sensitivity to changes in foreign ownership residency laws."
    },
    "Construction": {
        "margin": 6.0, 
        "cac": 750.0, 
        "risk": "Raw material material supply constraints, regulatory labor welfare framework costs, post-infrastructure pivot toward maintenance contracts."
    },
    "Global Digital Media": {
        "margin": 35.0, 
        "cac": 110.0, 
        "risk": "Compliance with the Qatar Media City framework, high expenditure for localized bilingual content (Arabic/English), heavy reliance on global ad platform data."
    }
}

# =====================================================================
# 4. SECURE GOOGLE DRIVE/SHEETS REAL-TIME DATABASE PERSISTENCE
# =====================================================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Reads data live from the secure Google Sheet in your Drive
    existing_data = conn.read(ttl="0d") # Zero caching forces real-time reads
    ledger_records = existing_data.to_dict(orient="records")
except Exception:
    # Fail-safe local memory container fallback if cloud credentials aren't linked yet
    if 'fallback_ledger' not in st.session_state:
        st.session_state.fallback_ledger = []
    ledger_records = st.session_state.fallback_ledger

# =====================================================================
# 5. ENTERPRISE APPLICATION TABS
# =====================================================================
tab1, tab2, tab3 = st.tabs(["📊 Market Matrix Analysis", "📈 Executive Capital Advisory", "📒 Verified System Ledger"])

# --- TAB 1: QATAR MARKET MATRIX ANALYSIS ---
with tab1:
    st.header("Strategic Operational Modeling")
    selected_industry = st.selectbox("Select Target Economic Sector (Qatar Framework):", list(INDUSTRIES.keys()))
    baseline = INDUSTRIES[selected_industry]

    st.subheader(f"{selected_industry} Baseline Benchmarks")
    col1, col2 = st.columns(2)
    col1.metric("Average Sector Net Margin", f"{baseline['margin']}%")
    col2.metric("Target Acquisition Cost (CAC)", f"{baseline['cac']} QAR")
    st.warning(f"Qatar Risk Vector: {baseline['risk']}")

    st.subheader("Venture Operational Adjustments")
    user_margin_mod = st.number_input("Net Margin Modifier Deviation (+/- %):", value=0.0, step=1.0)
    user_cac_mod = st.number_input("CAC Allocation Adjustment (+/- QAR):", value=0.0, step=10.0)
    special_conditions = st.text_area("Input Localized Variables (e.g., 'Utilizing state-subsidized warehousing, targeting Ashghal corporate contracts'):")

    # What-If Market Stress Sliders
    st.subheader("⚠️ Market Stress Test Simulator")
    supply_chain_stress = st.slider("Global Supply Chain Delay Factor (%)", 0, 100, 0)
    local_rent_stress = st.slider("Regional Commercial Rent Escalation (%)", 0, 50, 0)

    if st.button("Run Quantitative Strategy Brief"):
        if not model or api_key == "FALLBACK_SECURE_VAULT":
            st.error("System Core Error: Authentication vector unmapped.")
        else:
            projected_margin = baseline["margin"] + user_margin_mod - (supply_chain_stress * 0.1)
            projected_cac = baseline["cac"] + user_cac_mod + (local_rent_stress * 2)
            
            prompt = f"""
            Execute rigorous corporate financial audit for sector: {selected_industry}.
            QATAR ECONOMIC DATA:
            - Benchmark Margin: {baseline['margin']}% | Modeled Margin: {projected_margin}%
            - Benchmark CAC: {baseline['cac']} QAR | Modeled CAC: {projected_cac} QAR
            - System Stress Modifiers: Supply Chain Friction at {supply_chain_stress}%, Local Rent Hikes at {local_rent_stress}%
            - Local Directives: {special_conditions}
            
            Generate a concise, brutal, completely objective corporate appraisal detailing whether these metrics hold financial viability under current Qatari monetary conditions. Format purely as sections: [VIABILITY RATING], [CAPITAL EFFICIENCY REVIEWS], [STRATEGIC PITFALLS].
            """
            with st.spinner("Processing Qatar Macrofinancial Vectors..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.2})
                    st.subheader("📋 Executive Strategic Briefing")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Audit Interrupted: {e}")

# --- TAB 2: EXECUTIVE CAPITAL ADVISORY (DETERMINISTIC & BRACKETED) ---
with tab2:
    st.header("Executive Capital Allocation Logic")
    st.write("Calculates structured investment deployment strategies based on exact capital configurations.")
    
    current_investment = st.number_input("Liquid Capital Invested/Available (QAR):", min_value=0.0, value=50000.0, step=5000.0)
    current_earnings = st.number_input("Gross Retained Capital Earnings (QAR):", min_value=0.0, value=15000.0, step=1000.0)
    future_goal = st.text_input("Operational Scaling Milestone Target (e.g., Procurement of Doha commercial site):")
    
    # 1. Deterministic Rule-Based Capital Allocation Bracket Logic (Math First)
    st.subheader("🛡️ Algorithmic Asset Allocation Thresholds")
    if current_investment < 100000:
        bracket = "Micro-Venture Preservation Mode"
        max_recommended_deployment = current_earnings * 0.25
        strategy_summary = "High liquidity reservation mandatory. Avoid long-term capital lockdowns."
    elif 100000 <= current_investment <= 500000:
        bracket = "Mid-Tier Scaling Growth Mode"
        max_recommended_deployment = current_earnings * 0.50
        strategy_summary = "Balanced re-investment viable. Expansion to secondary zones allowed."
    else:
        bracket = "Macro Enterprise Dominance Mode"
        max_recommended_deployment = current_earnings * 0.75
        strategy_summary = "Aggressive capital deployment recommended. Capitalize on industrial scale efficiencies."

    # Render clean analytical metrics card display
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Current Asset Bracket Status", bracket)
    kpi2.metric("Max Calculated Capital Re-investment Cap", f"{max_recommended_deployment:,.2f} QAR")
    kpi3.metric("Liquidity Safety Margin Profile", f"{(current_investment + current_earnings - max_recommended_deployment):,.2f} QAR")
    st.info(f"System Baseline Directive: {strategy_summary}")

    if st.button("Generate CFO Asset Directive"):
        if model and future_goal:
            prompt = f"""
            Analyze this corporate asset framework as a seasoned Chief Financial Officer within Qatar.
            DATA CONFIGURATION:
            - System Asset Class Category: {bracket}
            - Current Pool Liquidity: {current_investment} QAR
            - Liquid Retained Earnings: {current_earnings} QAR
            - Mathematically Capped Re-investment Bound: {max_recommended_deployment} QAR
            - Targeted Strategic Milestone: {future_goal}
            
            Deliver a direct, numbers-focused capital allocation decree. Specify precisely how much of the retained capital to lock down as protective operational runway versus how much to allocate directly toward achieving the '{future_goal}'. Do not use casual language.
            """
            with st.spinner("Processing Portfolio Matrix..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.3})
                    st.subheader("📋 CFO Technical Directive")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Portfolio Engine Failure: {e}")

# --- TAB 3: VERIFIED SYSTEM LEDGER (REAL-TIME CLOUD RECORDING) ---
with tab3:
    st.header("Real-Time Financial System Ledger")
    st.write("All transactions register directly to your secure Google Drive/Sheets architecture.")
    
    with st.form("ledger_secure_form", clear_on_submit=True):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            entry_title = st.text_input("Transaction Line Item Nomenclature (e.g., Al Wakrah Facility Lease)")
        with col_t2:
            entry_type = st.selectbox("Accounting Allocation Class", ["Revenue", "Expense"])
        with col_t3:
            entry_amount = st.number_input("Transaction Financial Value (QAR)", min_value=0.0, value=0.0, step=50.0)
        
        submitted = st.form_submit_button("Commit Transaction to Cloud Storage")
        if submitted and entry_title:
            new_entry = {
                "Title": entry_title,
                "Type": entry_type,
                "Amount": entry_amount if entry_type == "Revenue" else -entry_amount
            }
            
            # Commit processing pipeline
            if 'fallback_ledger' in st.session_state:
                st.session_state.fallback_ledger.append(new_entry)
                ledger_records = st.session_state.fallback_ledger
            else:
                # Append live to the loaded DataFrame and upload via the connection engine
                current_df = pd.DataFrame(ledger_records)
                new_row_df = pd.DataFrame([new_entry])
                updated_df = pd.concat([current_df, new_row_df], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Transaction committed directly to Cloud Google Sheet.")
                st.rerun()

    # Data visualization module
    if ledger_records:
        df_active = pd.DataFrame(ledger_records)
        
        # Format the table display cleanly for executive review
        df_display = df_active.copy()
        df_display['Amount'] = df_display['Amount'].map(lambda val: f"{val:,.2f} QAR")
        st.dataframe(df_display, use_container_width=True)
        
        net_balance = df_active['Amount'].sum()
        if net_balance >= 0:
            st.success(f"📈 **Verified Net Balance Profile: {net_balance:,.2f} QAR**")
        else:
            st.error(f"📉 **Verified Net Deficit Position: {net_balance:,.2f} QAR**")
            
        # Hard Purge Mechanism
        with st.expander("System Administration Protocols"):
            if st.button("🔴 Purge Data Archive"):
                empty_df = pd.DataFrame(columns=["Title", "Type", "Amount"])
                if 'fallback_ledger' in st.session_state:
                    st.session_state.fallback_ledger = []
                else:
                    conn.update(data=empty_df)
                st.warning("Database records entirely wiped.")
                st.rerun()
    else:
        st.info("System Ledger currently reads zero active transaction matrices.")
