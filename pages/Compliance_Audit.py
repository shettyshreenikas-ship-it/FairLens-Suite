import streamlit as st

st.set_page_config(page_title="Compliance Audit", layout="wide")

st.markdown("<h1 style='font-family: serif; color: #c9a84c;'>⚖️ Regulatory Risk Scorecard</h1>", unsafe_allow_html=True)

# Create a 4-column row for "At-a-glance" status
m1, m2, m3, m4 = st.columns(4)
m1.metric("EU AI Act Status", "FAIL", "Article 10")
m2.metric("NYC Law 144", "CRITICAL", "-42% Disparity")
m3.metric("Bias Variance", "High", "Action Req.")
m4.metric("Adverse Impact", "detected")

st.write("---")

# Use an expander for "Detailed Legal Findings"
with st.expander("📄 View EU AI Act Compliance Mapping"):
    st.write("""
    - **Data Governance (Art. 10):** FAILED. Training data shows historical bias in geographical filtering.
    - **Technical Documentation (Art. 11):** PASSED. Model weights are logged.
    - **Human Oversight (Art. 14):** WARNING. Automation bias detected in final stage.
    """)

with st.expander("📄 View NYC Local Law 144 (AEDT) Results"):
    st.error("Calculated Impact Ratio for protected groups is below the 0.8 legal threshold.")

if st.button("← Back to Suite"):
    st.switch_page("app.py")