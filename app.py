import streamlit as st
import google.generativeai as genai

# 1. Web Page Setup
st.set_page_config(page_title="F.R.I.D.A.Y. Business Matrix", layout="centered")
st.title("💼 F.R.I.D.A.Y. Business Intelligence Core")
st.write("Compare localized venture variables against global industry baselines.")

# 2. Setup API Key (Use the same Gemini API key from your J.A.R.V.I.S. commands.py file)
API_KEY = "AQ.Ab8RN6IwPiqv5ksn8dLqrJ9KPMzzv2dW3nGG8sKv2CG1C0WBZA" 
genai.configure(api_key=API_KEY)

# 3. Industry Baseline Profiles (The Control Data)
INDUSTRIES = {
    "Retail Boutique": {"margin": 15.0, "cac": 40.0, "risk": "High physical rent overhead"},
    "E-Commerce Brands": {"margin": 20.0, "cac": 65.0, "risk": "Heavy dependency on ad platform spend"},
    "SaaS / Software": {"margin": 75.0, "cac": 120.0, "risk": "Long sales cycles, high initial dev costs"},
    "Logistics & Delivery": {"margin": 8.0, "cac": 30.0, "risk": "Fuel price volatility & asset maintenance"}
}

# 4. Web UI Component Input Layout
selected_industry = st.selectbox("Select Industry Sector:", list(INDUSTRIES.keys()))
baseline = INDUSTRIES[selected_industry]

st.subheader(f"📊 {selected_industry} Baseline Metrics")
col1, col2 = st.columns(2)
col1.metric("Avg Profit Margin", f"{baseline['margin']}%")
col2.metric("Customer Acquisition (CAC)", f"${baseline['cac']}")
st.warning(f"Standard Risk Factor: {baseline['risk']}")

# 5. Custom Data Inputs for calculations
st.subheader("📝 Enter Real-Time Venture Modifiers")
user_margin_mod = st.number_input("Profit Margin Modifier (+ or - %):", value=0.0, step=1.0)
user_cac_mod = st.number_input("CAC Cost Modifier (+ or - $):", value=0.0, step=1.0)
special_conditions = st.text_area("Input Unique Operational Traits (e.g., 'No rent because we work out of a home garage, organic TikTok reach'):")

# 6. Execute Mathematical & Cognitive Projection
if st.button("Generate Inverse Intelligence Projection"):
    
    # Calculate the exact mathematical delta (Baseline +- Personal Data)
    projected_margin = baseline["margin"] + user_margin_mod
    projected_cac = baseline["cac"] + user_cac_mod
    
    st.success("Mathematical Matrix Calculated!")
    
    # Build payload for evaluation
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
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            st.subheader("💡 F.R.I.D.A.Y. Strategic Conclusion")
            st.write(response.text)
        except Exception as e:
            st.error(f"Cognitive Engine offline: {e}")