import streamlit as st
import random

st.set_page_config(page_title="Counterfactual Engine", layout="wide")

st.markdown("""
<style>
    .reportview-container { background: #0d0d0d; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #c9a84c , #f0ede4); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-family: serif; color: #c9a84c;'>🔄 Algorithmic Sensitivity Lab</h1>", unsafe_allow_html=True)
st.write("Test how small changes in 'Protected Attributes' cause massive shifts in AI decision-making.")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("🛠️ Adjust Identity Variables")
    
    # Generic attribute testing instead of specific names
    ethnicity_proxy = st.select_slider("Ethnicity Proxy (Name Association)", options=["Group A", "Group B", "Group C", "Neutral"])
    gender_proxy = st.radio("Gender Association", ["Masculine-Coded", "Feminine-Coded", "Neutral"])
    age_slider = st.slider("Age Variable", 18, 65, 25)
    zip_code_tier = st.selectbox("Socio-economic Proxy (Zip Code)", ["Tier 1 (High Income)", "Tier 2 (Mid)", "Tier 3 (Low)"])

with col2:
    st.subheader("📊 Bias Impact Analysis")
    
    # Simulate a dynamic score based on the inputs
    base_score = 85
    if ethnicity_proxy != "Neutral": base_score -= random.randint(10, 20)
    if gender_proxy == "Feminine-Coded": base_score -= random.randint(5, 12)
    if zip_code_tier == "Tier 3 (Low)": base_score -= 15
    
    st.metric("Approval Probability", f"{base_score}%", delta=f"{base_score-85}% vs Baseline")
    st.progress(base_score / 100)
    
    st.write("---")
    st.write("### 🔍 Model Interpretability (LIME/SHAP)")
    st.info(f"The model is currently placing **{random.randint(40, 60)}% weight** on variables linked to your '{zip_code_tier}' selection, indicating a high risk of proxy discrimination.")

if st.button("← Back to Suite"):
    st.switch_page("app.py")