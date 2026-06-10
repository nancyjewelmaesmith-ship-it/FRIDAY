import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# =====================================================================
# 1. WEB UI CORE & LAYOUT
# =====================================================================
st.set_page_config(page_title="F.R.I.D.A.Y. Business Matrix", layout="wide")
st.title("💼 F.R.I.D.A.Y. Business Intelligence Core")
st.write("Compare venture variables, manage ledgers, and receive CFO-level projections.")

# =====================================================================
# 2. SECURE COGNITIVE INITIALIZATION
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "FALLBACK_SECURE_VAULT"

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel(
        model_name='gemini-3.5-flash',
        system_instruction=(
            "You are F.R.I.D.A.Y., a highly sophisticated, crisp, responsive, and loyal autonomous AI matrix. "
            "Your personality is highly efficient, analytical, professional, and slightly sharp. "
            "When analyzing investments, act as a Chief Financial Officer (CFO). Keep responses direct, dense, and strategic."
        )
    )
except Exception as e:
    st.error(f"F.R.I.D.A.Y. System Exception: {e}")
    model = None

# =====================================================================
# 3. CONTROL DATA MATRICES
# =====================================================================
INDUSTRIES = {
    "Food Industries": {"margin": 12.0, "cac": 15.0, "risk": "Perishability, health regulations, high competition"},
    "Energy and Petrochemicals": {"margin": 15.0, "cac": 500.0, "risk": "Massive capital expenditure, regulatory compliance, price volatility"},
    "Real Estate": {"margin": 30.0, "cac": 1000.0, "risk": "Market illiquidity, interest rate sensitivity"},
    "Construction": {"margin": 10.0, "cac": 200.0, "risk": "Supply chain delays, labor shortages, project cost overruns"},
    "Global Digital Media": {"margin": 40.0, "cac": 50.0, "risk": "Rapid trend shifts, high content production costs, platform dependency"},
    "Retail Boutique": {"margin": 15.0, "cac": 40.0, "risk": "High physical rent overhead"},
    "E-Commerce Brands": {"margin": 20.0, "cac": 65.0, "risk": "Heavy dependency on ad platform spend"},
    "SaaS / Software": {"margin": 75.0, "cac": 120.0, "risk": "Long sales cycles, high initial dev costs"},
}

# =====================================================================
# 4. PERSISTENT STORAGE MANAGEMENT (CSV ENGINE)
# =====================================================================
LEDGER_FILE = "ledger.csv"

def load_ledger_from_disk():
    """Reads saved data back into memory if the container restarts or refreshes."""
    if os.path.exists(LEDGER_FILE):
        try:
            df = pd.read_csv(LEDGER_FILE)
            return df.to_dict(orient="records")
        except Exception:
            return []
    return []

def save_ledger_to_disk(data):
    """Permanently commits the memory matrix to the local container storage."""
    try:
        df = pd.DataFrame(data)
        df.to_csv(LEDGER_FILE, index=False)
    except Exception as e:
        st.error(f"F.R.I.D.A.Y. Hardware Exception writing ledger data: {e}")

# Initialize local system state using historical disk data
if 'ledger' not in st.session_state:
    st.session_state.ledger = load_ledger_from_disk()

# =====================================================================
# 5. F.R.I.D.A.Y. MULTI-TAB INTERFACE
# =====================================================================
tab1, tab2, tab3 = st.tabs(["📊 Matrix & Projection", "📈 CFO Capital Decisions", "📒 Bookkeeping Space"])

# --- TAB 1: Industry Projection Matrix ---
with tab1:
    st.header("Industry Projection Matrix")
    selected_industry = st.selectbox("Select Industry Sector:", list(INDUSTRIES.keys()), key="ind_sel")
    baseline = INDUSTRIES[selected_industry]

    st.subheader(f"{selected_industry} Baseline Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Avg Profit Margin", f"{baseline['margin']}%")
    col2.metric("Customer Acquisition (CAC)", f"${baseline['cac']}")
    st.warning(f"Standard Risk Factor: {baseline['risk']}")

    st.subheader("📝 Enter Real-Time Venture Modifiers")
    user_margin_mod = st.number_input("Profit Margin Modifier (+ or - %):", value=0.0, step=1.0)
    user_cac_mod = st.number_input("CAC Cost Modifier (+ or - $):", value=0.0, step=1.0)
    special_conditions = st.text_area("Input Unique Operational Traits:", key="special_cond")

    if st.button("Generate Inverse Intelligence Projection", key="proj_btn"):
        if not model or api_key == "FALLBACK_SECURE_VAULT":
            st.error("F.R.I.D.A.Y. Error: Cognitive core unmapped.")
        else:
            projected_margin = baseline["margin"] + user_margin_mod
            projected_cac = baseline["cac"] + user_cac_mod
            
            prompt = f"""
            Evaluate this business plan for {selected_industry}.
            BASELINE PROTOCOLS: Margin: {baseline['margin']}% | CAC: ${baseline['cac']} | Risk: {baseline['risk']}
            OUR PROJECTED: Margin: {projected_margin}% | CAC: ${projected_cac}
            TRAITS: {special_conditions}
            Provide an objective, aggressive analytical business critique.
            """
            with st.spinner("F.R.I.D.A.Y. Brain Layer working..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.6})
                    st.subheader("💡 F.R.I.D.A.Y. Strategic Conclusion")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Engine Offline: {e}")

# --- TAB 2: CFO Financial Analysis ---
with tab2:
    st.header("CFO Investment & Capital Decision")
    st.write("Input current financials to receive capital allocation and future investment recommendations.")
    
    current_investment = st.number_input("Current Capital Invested ($):", min_value=0.0, value=10000.0, step=1000.0)
    current_earnings = st.number_input("Current Revenue/Earnings ($):", min_value=0.0, value=2500.0, step=500.0)
    future_goal = st.text_input("Future Business Goal (e.g., Expansion to new city, buying heavy machinery):")
    
    if st.button("Execute CFO Capital Analysis"):
        if model and future_goal:
            prompt = f"""
            As CFO F.R.I.D.A.Y., analyze the following financial standing:
            - Current Capital Invested: ${current_investment}
            - Current Earnings/Revenue: ${current_earnings}
            - Future Objective: {future_goal}
            
            Provide:
            1. An assessment of current ROI and capital efficiency.
            2. A strict recommendation on what to do with current earnings (e.g., reinvest exactly X amount, hold as runway, or withdraw).
            3. A projected recommended investment amount required to realistically achieve the '{future_goal}'.
            Keep it sharp, numerical, and strictly advisory.
            """
            with st.spinner("Calculating Capital Efficiency..."):
                try:
                    response = model.generate_content(prompt, generation_config={"temperature": 0.5})
                    st.subheader("💡 F.R.I.D.A.Y. CFO Directive")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Engine Offline: {e}")

# --- TAB 3: Live Bookkeeping Space ---
with tab3:
    st.header("Internal Persistent Ledger")
    st.write("Record expenses and revenue. Data persists through web refreshes.")
    
    # SYSTEM CONTROLS: Hard Backup Utility Zone
    col_back1, col_back2 = st.columns(2)
    with col_back1:
        uploaded_file = st.file_uploader("📥 Import/Restore Ledger File (.csv)", type=["csv"])
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                if all(col in uploaded_df.columns for col in ["Title", "Type", "Amount"]):
                    st.session_state.ledger = uploaded_df.to_dict(orient="records")
                    save_ledger_to_disk(st.session_state.ledger)
                    st.success("Ledger database successfully synchronized from backup file.")
                else:
                    st.error("Structure Error: Uploaded file missing mandatory ledger tracking headers.")
            except Exception as e:
                st.error(f"System failure processing structural load: {e}")
                
    with col_back2:
        st.write("📤 Export System Security Backup")
        if st.session_state.ledger:
            df_export = pd.DataFrame(st.session_state.ledger)
            csv_binary = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Download Data Backup (.csv)",
                data=csv_binary,
                file_name="friday_ledger_matrix.csv",
                mime="text/csv"
            )
        else:
            st.info("System ledger contains 0 active matrices to backup.")

    st.markdown("---")

    # Entry Submission Form
    with st.form("bookkeeping_form", clear_on_submit=True):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            entry_title = st.text_input("Transaction Line Item Description (e.g., Office Rent, Client Payment)")
        with col_t2:
            entry_type = st.selectbox("Accounting Class", ["Revenue", "Expense"])
        with col_t3:
            entry_amount = st.number_input("Financial Float Value ($)", min_value=0.0, value=0.0, step=10.0)
        
        submitted = st.form_submit_button("Commit Data Entry")
        if submitted and entry_title:
            new_record = {
                "Title": entry_title,
                "Type": entry_type,
                "Amount": entry_amount if entry_type == "Revenue" else -entry_amount
            }
            st.session_state.ledger.append(new_record)
            save_ledger_to_disk(st.session_state.ledger)
            st.success(f"Committed record entry: {entry_title}")
            st.rerun()
            
    # Rendering Interface Layout
    if st.session_state.ledger:
        df_active = pd.DataFrame(st.session_state.ledger)
        
        # Human-readable absolute currency mapping
        df_display = df_active.copy()
        df_display['Amount'] = df_display['Amount'].map(lambda val: f"${abs(val):,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        net_balance = df_active['Amount'].sum()
        if net_balance >= 0:
            st.success(f"📈 **System Net Valuation Balance: ${net_balance:,.2f}**")
        else:
            st.error(f"📉 **System Net Valuation Deficit: ${net_balance:,.2f}**")
            
        with st.expander("⚠️ System Clear Operations"):
            if st.button("🔴 Purge Cloud Server History"):
                st.session_state.ledger = []
                save_ledger_to_disk([])
                st.warning("Server instance data history deleted completely.")
                st.rerun()
