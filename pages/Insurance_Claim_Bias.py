import streamlit as st
from groq import Groq
import json
import re
import os

st.set_page_config(
    page_title="FairHire · Insurance Claim Bias",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Epilogue:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] { background: #0d0d0d; color: #e2e0d8; font-family: 'Epilogue', sans-serif; }
[data-testid="stAppViewContainer"] { background: #0d0d0d; min-height: 100vh; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; display: none; }
.page-wrap { max-width: 1000px; margin: 0 auto; padding: 3rem 2rem 6rem; }
.top-nav { display: flex; align-items: center; gap: 1rem; margin-bottom: 3rem; padding-bottom: 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.07); }
.nav-back { font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #4a4a4a; text-decoration: none; border: 1px solid rgba(255,255,255,0.08); padding: 0.4rem 0.9rem; border-radius: 2px; }
.nav-breadcrumb { font-size: 0.75rem; color: #3a3a3a; letter-spacing: 0.08em; }
.nav-breadcrumb span { color: #c9a84c; }
.step-bar { display: flex; align-items: center; gap: 0; margin-bottom: 3rem; }
.step-item { display: flex; align-items: center; gap: 0.6rem; padding: 0.8rem 1.2rem; font-size: 0.78rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; color: #3a3a3a; border: 1px solid rgba(255,255,255,0.05); border-right: none; }
.step-item:last-child { border-right: 1px solid rgba(255,255,255,0.05); }
.step-item.active { color: #c9a84c; border-color: rgba(201,168,76,0.25); background: rgba(201,168,76,0.04); }
.step-item.done { color: #5a5a5a; }
.step-num { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 700; background: rgba(255,255,255,0.06); color: #4a4a4a; flex-shrink: 0; }
.step-item.active .step-num { background: rgba(201,168,76,0.2); color: #c9a84c; }
.page-title { font-family: 'Playfair Display', serif; font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; color: #f0ede4; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.page-sub { font-size: 0.9rem; color: #5a5855; line-height: 1.6; margin-bottom: 3rem; }
.field-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #4a4a4a; margin-bottom: 0.6rem; display: block; }
.section-div { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 2.5rem 0; }
.r-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); padding: 1.8rem; margin-bottom: 1rem; }
.r-card-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #4a4a4a; margin-bottom: 1rem; }
.big-score { font-family: 'Playfair Display', serif; font-size: 4.5rem; font-weight: 900; line-height: 1; }
.score-sub { font-size: 0.78rem; color: #4a4a4a; margin-top: 0.4rem; letter-spacing: 0.08em; }
.risk-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.9rem; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
.risk-HIGH { background: rgba(180,50,50,0.12); color: #e06666; border: 1px solid rgba(180,50,50,0.25); }
.risk-MEDIUM { background: rgba(180,130,40,0.12); color: #d4aa55; border: 1px solid rgba(180,130,40,0.25); }
.risk-LOW { background: rgba(60,140,80,0.12); color: #6daa7f; border: 1px solid rgba(60,140,80,0.2); }
.flag-row { display: flex; gap: 1rem; align-items: flex-start; padding: 1.2rem; border-left: 2px solid transparent; margin-bottom: 0.8rem; background: rgba(255,255,255,0.015); }
.flag-row.HIGH { border-color: #7a2a2a; }
.flag-row.MEDIUM { border-color: #7a6020; }
.flag-row.LOW { border-color: #3a6040; }
.flag-sev { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.2rem 0.5rem; flex-shrink: 0; margin-top: 0.1rem; }
.sev-HIGH { color: #e06666; background: rgba(180,50,50,0.1); }
.sev-MEDIUM { color: #d4aa55; background: rgba(180,130,40,0.1); }
.sev-LOW { color: #6daa7f; background: rgba(60,140,80,0.1); }
.flag-title { font-size: 0.9rem; font-weight: 600; color: #e2e0d8; margin-bottom: 0.3rem; }
.flag-desc { font-size: 0.82rem; color: #6b6960; line-height: 1.55; }
.sug-row { display: flex; gap: 1rem; align-items: flex-start; padding: 1.2rem; margin-bottom: 0.8rem; background: rgba(201,168,76,0.03); border: 1px solid rgba(201,168,76,0.1); }
.sug-dot { width: 6px; height: 6px; background: #c9a84c; border-radius: 50%; margin-top: 0.5rem; flex-shrink: 0; }
.sug-title { font-size: 0.9rem; font-weight: 600; color: #c9a84c; margin-bottom: 0.3rem; }
.sug-desc { font-size: 0.82rem; color: #6b6960; line-height: 1.55; }
.verdict-box { border: 1px solid rgba(201,168,76,0.2); background: rgba(201,168,76,0.04); padding: 2rem; margin-bottom: 2rem; }
.verdict-text { font-size: 1.05rem; color: #e2e0d8; line-height: 1.6; margin-bottom: 0.6rem; }
.verdict-sub { font-size: 0.85rem; color: #5a5855; line-height: 1.6; }
.stat-insight { border: 1px dashed rgba(255,255,255,0.07); padding: 1.5rem; margin-bottom: 1.5rem; }
.stat-insight p { font-size: 0.85rem; color: #5a5855; line-height: 1.7; }
.stat-insight strong { color: #c9a84c; }
.stTextArea textarea { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 2px !important; color: #e2e0d8 !important; font-family: 'Epilogue', sans-serif !important; font-size: 0.875rem !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 2px !important; color: #e2e0d8 !important; }
.stTextInput input { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 2px !important; color: #e2e0d8 !important; font-family: 'Epilogue', sans-serif !important; }
.stNumberInput input { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 2px !important; color: #e2e0d8 !important; }
label, .stSelectbox label, .stTextArea label, .stTextInput label, .stNumberInput label { color: #4a4a4a !important; font-size: 0.8rem !important; }
.stButton > button { width: 100% !important; background: rgba(201,168,76,0.1) !important; border: 1px solid rgba(201,168,76,0.4) !important; color: #c9a84c !important; font-family: 'Epilogue', sans-serif !important; font-weight: 600 !important; font-size: 0.82rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; padding: 0.85rem 2rem !important; border-radius: 2px !important; }
.stButton > button:hover { background: rgba(201,168,76,0.18) !important; }
</style>
"""

def get_client():
    api_key = os.getenv("GROQ_API_KEY", "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")
    return Groq(api_key=api_key)

def safe_parse_json(raw: str):
    raw = re.sub(r'^```(?:json)?\s*', '', raw.strip())
    raw = re.sub(r'\s*```$', '', raw).strip()
    try: return json.loads(raw)
    except: pass
    def extract_block(text, opener, closer):
        start = text.find(opener)
        if start == -1: return None
        depth, in_string, esc = 0, False, False
        for i, ch in enumerate(text[start:], start):
            if esc: esc = False; continue
            if ch == '\\' and in_string: esc = True; continue
            if ch == '"': in_string = not in_string
            if not in_string:
                if ch == opener: depth += 1
                elif ch == closer:
                    depth -= 1
                    if depth == 0: return text[start:i+1]
        return None
    block = extract_block(raw,'{','}') or extract_block(raw,'[',']')
    if block:
        try: return json.loads(block)
        except: pass
    fixed = re.sub(r',\s*([}\]])', r'\1', block or raw)
    try: return json.loads(fixed)
    except json.JSONDecodeError as e:
        raise ValueError(f"Parse error: {raw[:400]}") from e

def analyze_insurance_bias(data: dict) -> dict:
    client = get_client()
    prompt = f"""You are an expert in algorithmic insurance discrimination and actuarial fairness.
Analyze this insurance claim for potential bias in automated approval/denial systems.

CLAIM DATA:
- Claimant Name: {data.get('name','Not provided')}
- Insurance Type: {data.get('insurance_type','Not specified')}
- Claim Amount: ${data.get('claim_amount',0):,}
- Claim Reason: {data.get('claim_reason','Not specified')}
- Claim Outcome: {data.get('outcome','Not specified')}
- Policy Duration: {data.get('policy_duration','Not specified')}
- Region / State: {data.get('region','Not specified')}
- Policyholder Age: {data.get('age','Not specified')}
- Gender: {data.get('gender','Not specified')}
- Occupation: {data.get('occupation','Not specified')}
- Prior Claims: {data.get('prior_claims','None')}
- Additional Context: {data.get('context','None provided')}

Return ONLY valid JSON. No markdown. Straight double quotes. No trailing commas.
{{
  "bias_risk": "<HIGH|MEDIUM|LOW>",
  "bias_risk_score": <int 0-100>,
  "fairness_score": <int 0-100>,
  "outcome_verdict": "<1 sentence — blame the system if bias found>",
  "summary": "<2 sentences>",
  "bias_flags": [
    {{"title":"<title>","description":"<1 sentence blaming the system>","severity":"<HIGH|MEDIUM|LOW>","bias_type":"<NAME_BIAS|REGIONAL_BIAS|GENDER_BIAS|AGE_BIAS|OCCUPATION_BIAS|OTHER>"}}
  ],
  "suggestions": [
    {{"title":"<title>","description":"<1 actionable sentence>"}}
  ],
  "legal_options": [
    {{"title":"<legal avenue>","description":"<how to pursue it>"}}
  ],
  "fair_outcome_estimate": "<what a fair, unbiased system should likely have decided>"
}}

Bias signals to detect:
- Name-based ethnic discrimination in claim processing
- Regional/geographic discrimination
- Gender-based claim processing disparities
- Age discrimination in claim approval
- Occupation-based unfair flagging
- Claim amount triggers in automated systems
- Prior claim history used disproportionately against minorities
Always blame the SYSTEM, not the claimant."""
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], max_tokens=2000, temperature=0.2)
    return safe_parse_json(r.choices[0].message.content)

# STATE
if "ins_step" not in st.session_state: st.session_state.ins_step = 1
if "ins_result" not in st.session_state: st.session_state.ins_result = None
if "ins_data" not in st.session_state: st.session_state.ins_data = {}

st.markdown(STYLES, unsafe_allow_html=True)
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

nav_col, bread_col = st.columns([1, 4])
with nav_col:
    if st.button("← Home", key="home_nav"):
        st.switch_page("app.py")
st.markdown('<div class="nav-breadcrumb" style="margin-bottom:1.5rem;font-size:0.75rem;color:#3a3a3a;letter-spacing:0.08em">FairHire Suite → <span style="color:#c9a84c">Insurance Claim Bias</span></div>', unsafe_allow_html=True)

step = st.session_state.ins_step
def sc(n):
    if n < step: return "done"
    if n == step: return "active"
    return ""

st.markdown(f"""
<div class="step-bar">
    <div class="step-item {sc(1)}"><div class="step-num">{"✓" if step>1 else "1"}</div>Claim Details</div>
    <div class="step-item {sc(2)}"><div class="step-num">{"✓" if step>2 else "2"}</div>Personal Profile</div>
    <div class="step-item {sc(3)}"><div class="step-num">3</div>Bias Report</div>
</div>
""", unsafe_allow_html=True)

# ── STEP 1 ──
if step == 1:
    st.markdown('<h1 class="page-title">Insurance claim<br>details.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Tell us about your claim. We\'ll detect if automated insurance systems unfairly processed your case based on protected characteristics.</p>', unsafe_allow_html=True)

    st.markdown('<div class="stat-insight"><p><strong>Research finding:</strong> Studies show minority claimants face <strong>40% longer processing times</strong> and <strong>23% lower settlement amounts</strong> for identical claims. Automated fraud detection systems flag minority claims at <strong>2.5× the rate</strong> of comparable majority claims.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<span class="field-label">Insurance Type</span>', unsafe_allow_html=True)
        ins_type = st.selectbox("Type", ["Health Insurance","Home/Property","Auto Insurance","Life Insurance","Disability","Business Insurance","Travel Insurance","Other"], label_visibility="collapsed", key="ins_type")
        st.markdown('<span class="field-label">Claim Amount ($)</span>', unsafe_allow_html=True)
        amount = st.number_input("Amount", min_value=0, max_value=10000000, value=15000, step=500, label_visibility="collapsed", key="ins_amt")
    with c2:
        st.markdown('<span class="field-label">Claim Outcome</span>', unsafe_allow_html=True)
        outcome = st.selectbox("Outcome", ["Denied","Partially Approved","Approved but Delayed","Under Review","Settled for Less","No Response"], label_visibility="collapsed", key="ins_out")
        st.markdown('<span class="field-label">Reason for Claim</span>', unsafe_allow_html=True)
        reason = st.text_input("Reason", placeholder="e.g. Water damage, Medical procedure, Car accident", label_visibility="collapsed", key="ins_reason")

    st.markdown('<span class="field-label">Additional Context (optional)</span>', unsafe_allow_html=True)
    context = st.text_area("Context", placeholder="Describe any unusual aspects of how your claim was handled...", height=100, label_visibility="collapsed", key="ins_ctx")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue →"):
        if not reason:
            st.error("Please describe the reason for your claim.")
        else:
            st.session_state.ins_data.update({"insurance_type":ins_type,"claim_amount":amount,"outcome":outcome,"claim_reason":reason,"context":context})
            st.session_state.ins_step = 2
            st.rerun()

# ── STEP 2 ──
elif step == 2:
    st.markdown('<h1 class="page-title">Your personal<br>profile.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">These details help us detect if demographic factors unfairly influenced your claim decision.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<span class="field-label">Full Name (as on policy)</span>', unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Your name as on the policy", label_visibility="collapsed", key="ins_name")
        st.markdown('<span class="field-label">Age</span>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=18, max_value=100, value=35, label_visibility="collapsed", key="ins_age")
        st.markdown('<span class="field-label">Occupation</span>', unsafe_allow_html=True)
        occupation = st.text_input("Occupation", placeholder="e.g. Nurse, Delivery Driver, Teacher", label_visibility="collapsed", key="ins_occ")
    with c2:
        st.markdown('<span class="field-label">Gender (as on policy)</span>', unsafe_allow_html=True)
        gender = st.selectbox("Gender", ["Male","Female","Non-binary","Prefer not to say"], label_visibility="collapsed", key="ins_gen")
        st.markdown('<span class="field-label">Region / State</span>', unsafe_allow_html=True)
        region = st.text_input("Region", placeholder="e.g. Louisiana, South Bronx NY", label_visibility="collapsed", key="ins_reg")
        st.markdown('<span class="field-label">Policy Duration</span>', unsafe_allow_html=True)
        duration = st.selectbox("Duration", ["Less than 1 year","1-2 years","3-5 years","5-10 years","10+ years"], label_visibility="collapsed", key="ins_dur")

    st.markdown('<span class="field-label">Prior Claims (in last 5 years)</span>', unsafe_allow_html=True)
    prior = st.selectbox("Prior Claims", ["None","1 claim","2 claims","3+ claims"], label_visibility="collapsed", key="ins_prior")

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns([1,3])
    with ca:
        if st.button("← Back"):
            st.session_state.ins_step = 1
            st.rerun()
    with cb:
        if st.button("Analyze for Bias →"):
            if not name:
                st.error("Please enter the name as it appears on the policy.")
            else:
                st.session_state.ins_data.update({"name":name,"age":age,"gender":gender,"region":region,"policy_duration":duration,"occupation":occupation,"prior_claims":prior})
                with st.spinner("Analyzing claim for discriminatory patterns..."):
                    try:
                        result = analyze_insurance_bias(st.session_state.ins_data)
                        st.session_state.ins_result = result
                        st.session_state.ins_step = 3
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

# ── STEP 3 ──
elif step == 3:
    result = st.session_state.ins_result
    data = st.session_state.ins_data
    bias_risk = result.get("bias_risk","MEDIUM")

    st.markdown('<h1 class="page-title">Claim bias<br>report.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Here\'s what we found. If your claim was unfairly processed, you have legal options — and we\'ve outlined them below.</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="verdict-box">
        <div class="r-card-label">AI Verdict</div>
        <div class="verdict-text">{result.get('outcome_verdict','')}</div>
        <div class="verdict-sub">{result.get('summary','')}</div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="r-card"><div class="r-card-label">Bias Risk Score</div><div class="big-score" style="color:#e06666">{result.get("bias_risk_score",0)}<span style="font-size:1.5rem">%</span></div><div class="score-sub">Discrimination Probability</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="r-card"><div class="r-card-label">System Fairness</div><div class="big-score" style="color:#c9a84c">{result.get("fairness_score",0)}<span style="font-size:1.5rem">%</span></div><div class="score-sub">Fairness Index</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="r-card"><div class="r-card-label">Risk Level</div><div style="margin:1rem 0"><span class="risk-badge risk-{bias_risk}">{bias_risk} RISK</span></div><div class="score-sub">{len(result.get("bias_flags",[]))} flags found</div></div>', unsafe_allow_html=True)

    # Fair outcome estimate
    fair_est = result.get("fair_outcome_estimate","")
    if fair_est:
        st.markdown(f"""
        <div class="stat-insight" style="border-color:rgba(201,168,76,0.2);">
            <p><strong>What a fair system should have decided:</strong><br>{fair_est}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown('<div class="r-card-label">Bias Flags Detected</div>', unsafe_allow_html=True)
        for f in result.get("bias_flags",[]):
            sev = f.get("severity","MEDIUM")
            st.markdown(f"""
            <div class="flag-row {sev}">
                <span class="flag-sev sev-{sev}">{sev}</span>
                <div>
                    <div class="flag-title">{f.get('title','')}</div>
                    <div class="flag-desc">{f.get('description','')}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="r-card-label">Recommendations</div>', unsafe_allow_html=True)
        for s in result.get("suggestions",[]):
            st.markdown(f"""
            <div class="sug-row">
                <div class="sug-dot"></div>
                <div>
                    <div class="sug-title">{s.get('title','')}</div>
                    <div class="sug-desc">{s.get('description','')}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Legal options
    legal = result.get("legal_options",[])
    if legal:
        st.markdown("<hr class='section-div'>", unsafe_allow_html=True)
        st.markdown('<div class="r-card-label">Your Legal Options</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem;color:#4a4a4a;margin-bottom:1rem;letter-spacing:0.05em">Note: This is not legal advice. Consult a qualified attorney for your specific situation.</p>', unsafe_allow_html=True)
        for l in legal:
            st.markdown(f"""
            <div class="sug-row" style="border-color:rgba(100,100,180,0.2);background:rgba(80,80,160,0.04)">
                <div class="sug-dot" style="background:#8888dd"></div>
                <div>
                    <div class="sug-title" style="color:#aaaaee">{l.get('title','')}</div>
                    <div class="sug-desc">{l.get('description','')}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    report = f"FairHire Insurance Claim Bias Report\nClaimant: {data.get('name')}\nInsurance Type: {data.get('insurance_type')}\nClaim: ${data.get('claim_amount'):,} for {data.get('claim_reason')}\nOutcome: {data.get('outcome')}\nBias Risk: {bias_risk} ({result.get('bias_risk_score')}%)\nFairness Score: {result.get('fairness_score')}%\n\nVerdict: {result.get('outcome_verdict','')}\n\nFair Outcome Estimate: {result.get('fair_outcome_estimate','N/A')}\n\nFlags:\n" + "\n".join(f"- [{f['severity']}] {f['title']}: {f['description']}" for f in result.get("bias_flags",[]))

    col_dl, col_restart = st.columns([1,2])
    with col_dl:
        st.download_button("↓ Download Report", data=report, file_name="FairHire_Insurance_Analysis.txt", mime="text/plain")
    with col_restart:
        if st.button("Start New Analysis"):
            for k in ["ins_step","ins_result","ins_data"]:
                if k in st.session_state: del st.session_state[k]
            st.session_state.ins_step = 1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
