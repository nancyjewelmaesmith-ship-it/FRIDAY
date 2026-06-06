import streamlit as st
import google.generativeai as genai

# =====================================================================
# 1. WEB UI CORE & LAYOUT
# =====================================================================
st.set_page_config(page_title="F.R.I.D.A.Y. Business Matrix", layout="centered")
st.title("💼 F.R.I.D.A.Y. Business Intelligence Core")
st.write("Compare localized venture variables against global industry baselines.")

# =====================================================================
# 2. SECURE COGNITIVE INITIALIZATION
# =====================================================================
# Safe check for Streamlit Cloud secure secrets environment
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Safe fallback string for local offline syntax checks
    api_key = "FALLBACK_SECURE_VAULT"

genai.configure(api_key=api_key)

# Bind strictly to the stable 1.5 engine to completely eliminate 429 quota errors
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=(
            "You are F.R.I.D.A.Y., a highly sophisticated, crisp, responsive, and loyal autonomous AI matrix. "
            "Your personality is highly efficient, analytical, professional, and slightly sharp. "
            "Never adopt any other AI persona. Keep responses direct, dense, and strategic."
        )
    )
except Exception as e:
    st.error(f"F.R.I.D.A.Y. System Exception during initialization: {e}")
    model = None

# =====================================================================
# 3. CONTROL DATA MATRICES
# =====================================================================
INDUSTRIES = {
    "Retail Boutique": {"margin": 15.0, "cac": 40.0, "risk": "High physical rent overhead"},
    "E-Commerce Brands": {"margin": 20.0, "cac": 65.0, "risk": "Heavy dependency on ad platform spend"},
    "SaaS / Software": {"margin": 75.0, "cac": 120.0, "risk": "Long sales cycles, high initial dev costs"},
    "Logistics & Delivery": {"margin": 8.0, "cac": 30.0, "risk": "Fuel price volatility & asset maintenance"}
}

# =====================================================================
# 4. INTERACTIVE HUB INPUT LAYOUT
# =====================================================================
selected_industry = st.selectbox("Select Industry Sector:", list(INDUSTRIES.keys()))
baseline = INDUSTRIES[selected_industry]

st.subheader(f"📊 {selected_industry} Baseline Metrics")
col1, col2 = st.columns(2)
col1.metric("Avg Profit Margin", f"{baseline['margin']}%")
col2.metric("Customer Acquisition (CAC)", f"${baseline['cac']}")
st.warning(f"Standard Risk Factor: {baseline['risk']}")

st.subheader("📝 Enter Real-Time Venture Modifiers")
user_margin_mod = st.number_input("Profit Margin Modifier (+ or - %):", value=0.0, step=1.0)
user_cac_mod = st.number_input("CAC Cost Modifier (+ or - $):", value=0.0, step=1.0)
special_conditions = st.text_area(
    "Input Unique Operational Traits (e.g., 'No rent because we work out of a home garage, organic TikTok reach'):"
)

# =====================================================================
# 5. DYNAMIC CALCULATION & INVERSE PROJECTION
# =====================================================================
if st.button("Generate Inverse Intelligence Projection"):
    if not model or api_key == "FALLBACK_SECURE_VAULT":
        st.error("F.R.I.D.A.Y. Error: Cognitive core unmapped. Please check your Streamlit Secrets.")
    else:
        # Compute exact mathematical deltas
        projected_margin = baseline["margin"] + user_margin_mod
        projected_cac = baseline["cac"] + user_cac_mod
        
        st.success("Mathematical Matrix Calculated!")
        
        # Build prompt payload for F.R.I.D.A.Y. parsing
        prompt = f"""
        Evaluate this business plan deviation matrix for the industry: {selected_industry}.
        
        BASELINE PROTOCOLS:
        - Standard Industry Margin: {baseline['margin']}% | Our Projected Margin: {projected_margin}%
        - Standard Industry CAC: ${baseline['cac']} | Our Projected CAC: ${projected_cac}
        - Baseline Pitfalls: {baseline['risk']}
        
        OUR UNIQUE OPERATIONAL TRAITS:
        {special_conditions}
        
        Provide an objective, aggressive analytical business critique. Immerse into the strategy, outline the exact pros and cons of why this venture will either conquer the baseline industry projection or fall flat due to calculations. Keep it dense and strategic.
        """
        
        with st.spinner("F.R.I.D.A.Y. Brain Layer working..."):
            try:
                # FIXED: Calling the pre-configured global 1.5 model instead of trying to instantiate 2.0-flash here
                response = model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.6}
                )
                
                st.subheader("💡 F.R.I.D.A.Y. Strategic Conclusion")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"F.R.I.D.A.Y. Cognitive Engine Offline: {e}")
