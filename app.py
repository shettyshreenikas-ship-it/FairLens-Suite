import streamlit as st

st.set_page_config(
    page_title="FairLens · AI Bias Detection Suite",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

with st.sidebar:

    st.markdown("## ⚖️ FairHire Tools")

    st.markdown("### 📸 Quick Scan")

    if st.button("📸 Enable Camera", key="cam_btn_force"):
        photo = st.camera_input("Capture document", key="cam_force")
        if photo:
            st.image(photo)
            st.success("Scan captured")

    st.markdown("---")

    st.markdown("### 📞 Helpline")

    if st.button("☎ Report Bias", key="help_btn_force"):
        st.info("📧 support@fairhire.ai")
        st.info("📱 WhatsApp: +91-XXXXXXX")
        st.info("⏰ 24/7 Support")
    st.markdown("---")

    st.markdown("**🤖 AI Assistant**")

    if st.button("💬 Open AI Chat"):
        st.switch_page("pages/AI_Assistant.py")
    
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Epilogue:wght@300;400;500;600&display=swap');

section[data-testid="stSidebar"] {
    background: rgba(13,13,13,0.98) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.08) !important;
    width: 260px !important;
    padding: 1rem 1rem 2rem !important;
}

/* FIX SIDEBAR CONTENT VISIBILITY */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #e2e0d8 !important;
}

.sidebar-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #c9a84c !important;
    text-align: center !important;
    margin-bottom: 1.5rem !important;
    padding-bottom: 0.8rem !important;
    border-bottom: 1px solid rgba(201,168,76,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(201,168,76,0.12), rgba(201,168,76,0.06)) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    color: #c9a84c !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
}

.stButton > button:hover {
    background: rgba(201,168,76,0.08) !important;
    border-color: rgba(201,168,76,0.7) !important;
}

section[data-testid="stSidebar"] .stCamera {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(201,168,76,0.4) !important;
    border-radius: 4px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(""" 
<style> 
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Epilogue:wght@300;400;500;600&display=swap'); 
 
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; } 
 
html, body, [data-testid="stAppViewContainer"] { 
    background: #0d0d0d; 
    color: #e2e0d8; 
    font-family: 'Epilogue', sans-serif; 
} 
 
[data-testid="stAppViewContainer"] { 
background: #0d0d0d; 
height: 100vh;
overflow: auto;
} 

[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
 
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { 
    visibility: hidden; display: none; 
} 
 
/* ── NOISE OVERLAY ── */ 
    section[data-testid="stSidebar"] {
    position: relative;
    z-index: 9999;
}
/* FIX BACKGROUND OVERLAY */
[data-testid="stAppViewContainer"]::before {
    z-index: -1 !important;
    pointer-events: none;
}
 
.main-wrap { 
    max-width: 1100px; 
    margin: 0 auto; 
    padding: 1rem 2rem 0.5rem;
    position: relative; 
    z-index: 1; 
} 
 
/* ── HEADER ── */ 
.site-header { 
    display: flex; 
    justify-content: center;
    align-items: center; 
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.07); 
    position: relative;
} 
.logo { 
    font-family: 'Playfair Display', serif; 
    font-size: 1.3rem; 
    font-weight: 700; 
    color: #e2e0d8; 
    letter-spacing: -0.01em; 
    text-align: center;
} 
.logo span { color: #c9a84c; } 
.header-tag { 
    font-size: 0.72rem; 
    font-weight: 500; 
    letter-spacing: 0.2em; 
    text-transform: uppercase; 
    color: #5a5a5a;
    position: absolute;
    right: 0;
} 
 
/* ── HERO SECTION ── */ 
.hero-section { 
    margin-bottom: 1rem;
    justify-content: center;
    text-align: center;
} 
.hero-eyebrow { 
    font-size: 0.72rem; 
    font-weight: 600; 
    letter-spacing: 0.25em; 
    text-transform: uppercase; 
    color: #c9a84c; 
    margin-bottom: 0.5rem;
} 
.hero-title { 
    font-family: 'Playfair Display', serif; 
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    font-weight: 900; 
    line-height: 1.05;
    letter-spacing: -0.03em; 
    color: #f0ede4; 
    margin-bottom: 0.4rem;
} 
.hero-title em { 
    font-style: italic; 
    color: #c9a84c; 
} 
.hero-subtitle { 
    font-size: 0.92rem;
    color: #6b6960; 
    max-width: 600px; 
    line-height: 1.4;
    margin: 0 auto 0.8rem;
    font-weight: 400; 
} 
 
/* ── SECTION LABEL ── */ 
.section-label { 
    font-size: 0.68rem; 
    font-weight: 600; 
    letter-spacing: 0.2em; 
    text-transform: uppercase; 
    color: #4a4a4a; 
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06); 
} 
 
/* ── MODULE CARDS ── */ 
.modules-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
    gap: 1.5px; 
    background: rgba(255,255,255,0.05); 
    border: 1px solid rgba(255,255,255,0.05); 
    border-radius: 2px; 
    overflow: hidden; 
    margin-bottom: 1rem;
} 
.module-card { 
    background: #0d0d0d; 
    padding: 1.2rem 1.5rem;
    position: relative; 
    cursor: pointer; 
    transition: background 0.25s ease; 
    text-decoration: none; 
    display: block; 
} 
.module-card:hover { 
    background: #141414; 
} 
.module-card::after { 
    content: ""; 
    position: absolute; 
    bottom: 0; 
    left: 0; 
    right: 0; 
    height: 2px; 
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0), transparent); 
    transition: background 0.3s; 
} 
.module-card:hover::after { 
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.5), transparent); 
} 
.module-number { 
    font-family: 'Playfair Display', serif; 
    font-size: 0.75rem; 
    font-weight: 400; 
    color: #3a3a3a; 
    letter-spacing: 0.1em; 
    margin-bottom: 0.5rem;
} 
.module-icon { 
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    display: block; 
} 
.module-title { 
    font-family: 'Playfair Display', serif; 
    font-size: 1.2rem;
    font-weight: 700; 
    color: #e2e0d8; 
    margin-bottom: 0.4rem;
    line-height: 1.2; 
} 
.module-desc { 
    font-size: 0.8rem;
    color: #5a5855; 
    line-height: 1.5;
    margin-bottom: 0.8rem;
} 
.module-tags { 
    display: flex; 
    flex-wrap: wrap; 
    gap: 0.4rem; 
    margin-bottom: 0.8rem;
} 
.module-tag { 
    font-size: 0.68rem; 
    font-weight: 500; 
    letter-spacing: 0.08em; 
    text-transform: uppercase; 
    padding: 0.2rem 0.5rem;
    border: 1px solid rgba(255,255,255,0.1); 
    border-radius: 2px; 
    color: #5a5855; 
} 
.module-cta { 
    display: flex; 
    align-items: center; 
    gap: 0.5rem; 
    font-size: 0.82rem; 
    font-weight: 600; 
    letter-spacing: 0.08em; 
    text-transform: uppercase; 
    color: #c9a84c; 
} 
.module-cta-arrow { 
    transition: transform 0.2s; 
} 
.module-card:hover .module-cta-arrow { 
    transform: translateX(4px); 
} 
.module-card.coming-soon { 
    opacity: 0.4; 
    cursor: not-allowed; 
} 
.module-card.coming-soon:hover { background: #0d0d0d; } 
.coming-soon-badge { 
    font-size: 0.65rem; 
    font-weight: 600; 
    letter-spacing: 0.15em; 
    text-transform: uppercase; 
    color: #5a5855; 
    background: rgba(255,255,255,0.05); 
    border: 1px solid rgba(255,255,255,0.08); 
    padding: 0.2rem 0.6rem; 
    border-radius: 2px; 
    display: inline-block; 
    margin-top: 0.5rem;
} 
 
/* ── STATS ROW ── */ 
.stats-row { 
    display: grid; 
    grid-template-columns: repeat(3, 1fr); 
    gap: 0; 
    border: 1px solid rgba(255,255,255,0.06); 
    margin-bottom: 1.2rem;
} 
.stat-item { 
    padding: 1rem;
    border-right: 1px solid rgba(255,255,255,0.06); 
    text-align: center; 
} 
.stat-item:last-child { border-right: none; } 
.stat-number { 
    font-family: 'Playfair Display', serif; 
    font-size: 1.8rem;
    font-weight: 900; 
    color: #c9a84c; 
    display: block; 
} 
.stat-label { 
    font-size: 0.72rem;
    color: #4a4a4a; 
    letter-spacing: 0.1em; 
    text-transform: uppercase; 
    margin-top: 0.2rem;
} 
 
/* ── FOOTER ── */ 
.site-footer { 
    border-top: 1px solid rgba(255,255,255,0.06); 
    padding-top: 0.8rem;
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    flex-wrap: wrap; 
    gap: 0.5rem;
} 
.footer-text { 
    font-size: 0.72rem;
    color: #3a3a3a; 
    letter-spacing: 0.05em; 
} 
.footer-link { 
    font-size: 0.72rem;
    color: #5a5855; 
    text-decoration: none; 
    letter-spacing: 0.05em; 
    border-bottom: 1px solid #3a3a3a; 
    padding-bottom: 1px; 
} 
 
/* Streamlit button override */ 
.stButton > button { 
    background: transparent !important; 
    border: 1px solid rgba(201,168,76,0.4) !important; 
    color: #c9a84c !important; 
    font-family: 'Epilogue', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important; 
    text-transform: uppercase !important; 
    padding: 0.5rem 1.5rem !important;
    border-radius: 2px !important; 
    transition: all 0.2s !important; 
    width: 100% !important;
} 
.stButton > button:hover { 
    background: rgba(201,168,76,0.08) !important; 
    border-color: rgba(201,168,76,0.7) !important; 
}

/* Remove extra gap between columns */
[data-testid="stHorizontalBlock"] {
    gap: 0.5rem !important;
}

/* Tighten column padding */
[data-testid="stColumn"] {
    padding: 0 !important;
}
</style> 
""", unsafe_allow_html=True) 
 
st.markdown('<div class="main-wrap">', unsafe_allow_html=True) 
 
# Header — logo centered, tag on right
st.markdown(""" 
<div class="site-header"> 
    <div class="logo">Fair<span>Lens</span> · Suite</div> 
    <div class="header-tag">AI Bias Detection · 2026</div> 
</div> 
""", unsafe_allow_html=True) 
 
# Hero 
st.markdown(""" 
<div class="hero-section"> 
    <div class="hero-eyebrow">Algorithmic Fairness Intelligence</div> 
    <h1 class="hero-title">Where does <em>bias</em> hide in your data?</h1> 
</div> 
""", unsafe_allow_html=True) 
 
# Modules 
st.markdown('<div class="section-label">Select a module to begin</div>', unsafe_allow_html=True) 
 
col1, col2, col3 = st.columns(3, gap="small") 
 
with col1: 
    st.markdown(""" 
    <div class="module-card"> 
        <div class="module-number">Module 01</div> 
        <span class="module-icon">💼</span> 
        <div class="module-title">Job Hiring Bias</div> 
        <div class="module-desc">Upload your resume and a job description. Our AI detects ATS discrimination patterns, flags bias triggers, and maps them directly onto your resume with an interactive heatmap.</div> 
        <div class="module-tags"> 
            <span class="module-tag">Resume Analysis</span> 
            <span class="module-tag">ATS Simulation</span> 
            <span class="module-tag">Bias Heatmap</span> 
        </div> 
    </div> 
    """, unsafe_allow_html=True) 
    if st.button("Launch Module →", key="btn_job"): 
        st.switch_page("pages/Job_Hiring_Bias.py") 
 
with col2: 
    st.markdown(""" 
    <div class="module-card"> 
        <div class="module-number">Module 02</div> 
        <span class="module-icon">🏦</span> 
        <div class="module-title">Loan Approval Bias</div> 
        <div class="module-desc">Enter your loan application details. Detect if your name, region, or income pattern unfairly triggered automated rejection — with real-world disparity statistics.</div> 
        <div class="module-tags"> 
            <span class="module-tag">Name Analysis</span> 
            <span class="module-tag">Regional Bias</span> 
            <span class="module-tag">Income Patterns</span> 
        </div> 
    </div> 
    """, unsafe_allow_html=True) 
    if st.button("Launch Module →", key="btn_loan"): 
        st.switch_page("pages/Loan_Approval_Bias.py") 
 
with col3: 
    st.markdown(""" 
    <div class="module-card"> 
        <div class="module-number">Module 03</div> 
        <span class="module-icon">🛡️</span> 
        <div class="module-title">Insurance Claim Bias</div> 
        <div class="module-desc">Analyze your insurance claim for discriminatory patterns. Identify if automated systems unfairly flagged your claim based on protected characteristics.</div> 
        <div class="module-tags"> 
            <span class="module-tag">Claim Analysis</span> 
            <span class="module-tag">Fair Decisions</span> 
            <span class="module-tag">Pattern Detection</span> 
        </div> 
    </div> 
    """, unsafe_allow_html=True) 
    if st.button("Launch Module →", key="btn_ins"): 
        st.switch_page("pages/Insurance_Claim_Bias.py") 
 
# Footer 
st.markdown(""" 
<div class="site-footer"> 
    <div class="footer-text">FairLens Suite · Built for Hack2Skill · Unbiased AI Challenge 2026</div> 
    <a href="https://github.com/shreyamokshanatha-hue/fairhire-bias-detector" target="_blank" class="footer-link">View Source on GitHub ↗</a> 
</div> 
""", unsafe_allow_html=True) 
 
st.markdown('</div>', unsafe_allow_html=True)