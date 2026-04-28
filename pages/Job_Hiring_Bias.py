import streamlit as st
from groq import Groq
import pdfplumber
import json
import re
import html
import os

st.set_page_config(
    page_title="FairHire · Job Hiring Bias",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Epilogue:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d;
    color: #e2e0d8;
    font-family: 'Epilogue', sans-serif;
}
[data-testid="stAppViewContainer"] { background: #0d0d0d; min-height: 100vh; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; display: none; }

.page-wrap { max-width: 1000px; margin: 0 auto; padding: 3rem 2rem 6rem; }

/* NAV */
.top-nav {
    display: flex; align-items: center; gap: 1rem;
    margin-bottom: 3rem; padding-bottom: 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.nav-back {
    font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: #4a4a4a; text-decoration: none;
    border: 1px solid rgba(255,255,255,0.08); padding: 0.4rem 0.9rem;
    border-radius: 2px; transition: color 0.2s, border-color 0.2s;
}
.nav-back:hover { color: #c9a84c; border-color: rgba(201,168,76,0.4); }
.nav-breadcrumb { font-size: 0.75rem; color: #3a3a3a; letter-spacing: 0.08em; }
.nav-breadcrumb span { color: #c9a84c; }

/* STEP INDICATOR */
.step-bar {
    display: flex; align-items: center; gap: 0; margin-bottom: 3rem;
}
.step-item {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.8rem 1.2rem; font-size: 0.78rem; font-weight: 500;
    letter-spacing: 0.06em; text-transform: uppercase; color: #3a3a3a;
    border: 1px solid rgba(255,255,255,0.05); border-right: none;
    position: relative; cursor: default;
}
.step-item:last-child { border-right: 1px solid rgba(255,255,255,0.05); }
.step-item.active { color: #c9a84c; border-color: rgba(201,168,76,0.25); background: rgba(201,168,76,0.04); }
.step-item.done { color: #5a5a5a; }
.step-num {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 700;
    background: rgba(255,255,255,0.06); color: #4a4a4a;
    flex-shrink: 0;
}
.step-item.active .step-num { background: rgba(201,168,76,0.2); color: #c9a84c; }
.step-item.done .step-num { background: rgba(255,255,255,0.04); color: #4a4a4a; }

/* PAGE TITLE */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 900; color: #f0ede4; line-height: 1.1;
    letter-spacing: -0.02em; margin-bottom: 0.5rem;
}
.page-sub { font-size: 0.9rem; color: #5a5855; line-height: 1.6; margin-bottom: 3rem; }

/* FIELD LABEL */
.field-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: #4a4a4a; margin-bottom: 0.6rem;
    display: block;
}

/* SECTION DIVIDER */
.section-div {
    border: none; border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2.5rem 0;
}

/* RESULT CARD */
.r-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 1.8rem; margin-bottom: 1rem;
}
.r-card-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: #4a4a4a; margin-bottom: 1rem;
}

/* BIG SCORE */
.big-score {
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem; font-weight: 900; line-height: 1;
}
.score-sub { font-size: 0.78rem; color: #4a4a4a; margin-top: 0.4rem; letter-spacing: 0.08em; }

/* RISK BADGE */
.risk-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.35rem 0.9rem; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
}
.risk-HIGH { background: rgba(180,50,50,0.12); color: #e06666; border: 1px solid rgba(180,50,50,0.25); }
.risk-MEDIUM { background: rgba(180,130,40,0.12); color: #d4aa55; border: 1px solid rgba(180,130,40,0.25); }
.risk-LOW { background: rgba(60,140,80,0.12); color: #6daa7f; border: 1px solid rgba(60,140,80,0.25); }

/* FLAG */
.flag-row {
    display: flex; gap: 1rem; align-items: flex-start;
    padding: 1.2rem; border-left: 2px solid transparent;
    margin-bottom: 0.8rem; background: rgba(255,255,255,0.015);
}
.flag-row.HIGH { border-color: #7a2a2a; }
.flag-row.MEDIUM { border-color: #7a6020; }
.flag-row.LOW { border-color: #3a6040; }
.flag-sev {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 0.2rem 0.5rem; flex-shrink: 0; margin-top: 0.1rem;
}
.sev-HIGH { color: #e06666; background: rgba(180,50,50,0.1); }
.sev-MEDIUM { color: #d4aa55; background: rgba(180,130,40,0.1); }
.sev-LOW { color: #6daa7f; background: rgba(60,140,80,0.1); }
.flag-title { font-size: 0.9rem; font-weight: 600; color: #e2e0d8; margin-bottom: 0.3rem; }
.flag-desc { font-size: 0.82rem; color: #6b6960; line-height: 1.55; }

/* SUGGESTION */
.sug-row {
    display: flex; gap: 1rem; align-items: flex-start;
    padding: 1.2rem; margin-bottom: 0.8rem;
    background: rgba(201,168,76,0.03);
    border: 1px solid rgba(201,168,76,0.1);
}
.sug-dot { width: 6px; height: 6px; background: #c9a84c; border-radius: 50%; margin-top: 0.5rem; flex-shrink: 0; }
.sug-title { font-size: 0.9rem; font-weight: 600; color: #c9a84c; margin-bottom: 0.3rem; }
.sug-desc { font-size: 0.82rem; color: #6b6960; line-height: 1.55; }

/* TAG */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.tag { font-size: 0.72rem; padding: 0.2rem 0.6rem; font-weight: 500; letter-spacing: 0.05em; }
.tag-match { background: rgba(60,140,80,0.1); color: #6daa7f; border: 1px solid rgba(60,140,80,0.2); }
.tag-miss { background: rgba(180,50,50,0.1); color: #e06666; border: 1px solid rgba(180,50,50,0.2); }

/* HEATMAP */
.heatmap-box {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
    padding: 1.8rem; font-size: 0.875rem; line-height: 2;
    color: #b8b5aa; white-space: pre-wrap; max-height: 480px;
    overflow-y: auto; font-family: 'Epilogue', sans-serif;
}
.hm-high { background: rgba(180,50,50,0.28); color: #f0a0a0; padding: 1px 5px; border-bottom: 2px solid #7a2a2a; font-weight: 600; cursor: help; }
.hm-med  { background: rgba(180,130,40,0.28); color: #f0d090; padding: 1px 5px; border-bottom: 2px solid #8a7020; font-weight: 500; cursor: help; }
.hm-low  { background: rgba(60,120,80,0.2);   color: #90d0a0; padding: 1px 5px; border-bottom: 2px solid #3a6040; cursor: help; }
.legend { display: flex; gap: 1.5rem; margin-bottom: 0.8rem; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.72rem; color: #4a4a4a; letter-spacing: 0.08em; text-transform: uppercase; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; }

/* VERDICT */
.verdict-box {
    border: 1px solid rgba(201,168,76,0.2);
    background: rgba(201,168,76,0.04);
    padding: 2rem; margin-bottom: 2rem;
}
.verdict-text { font-size: 1.05rem; color: #e2e0d8; line-height: 1.6; margin-bottom: 0.6rem; }
.verdict-sub { font-size: 0.85rem; color: #5a5855; line-height: 1.6; }

/* METRIC BAR */
.metric-bar-wrap { margin: 0.5rem 0 1.2rem; }
.metric-bar-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: #4a4a4a; letter-spacing: 0.06em; margin-bottom: 0.4rem; }
.metric-bar-bg { background: rgba(255,255,255,0.05); height: 3px; }
.metric-bar-fill { height: 3px; }

/* STREAMLIT OVERRIDES */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(255,255,255,0.12) !important;
    border-radius: 2px !important;
}
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 2px !important;
    color: #e2e0d8 !important;
    font-family: 'Epilogue', sans-serif !important;
    font-size: 0.875rem !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 2px !important;
    color: #e2e0d8 !important;
}
.stTextInput input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 2px !important;
    color: #e2e0d8 !important;
    font-family: 'Epilogue', sans-serif !important;
}
label, .stSelectbox label, .stTextArea label, .stTextInput label { color: #4a4a4a !important; font-size: 0.8rem !important; }
.stButton > button {
    width: 100% !important;
    background: rgba(201,168,76,0.1) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    color: #c9a84c !important;
    font-family: 'Epilogue', sans-serif !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    padding: 0.85rem 2rem !important; border-radius: 2px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: rgba(201,168,76,0.18) !important; }
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #5a5855 !important; font-family: 'Epilogue', sans-serif !important;
    font-size: 0.75rem !important; letter-spacing: 0.08em !important;
    text-transform: uppercase !important; padding: 0.6rem 1.2rem !important;
    border-radius: 2px !important; width: auto !important;
}
</style>
"""

def get_client():
    api_key = os.getenv("GROQ_API_KEY", "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")
    return Groq(api_key=api_key)

def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text.strip()

def safe_parse_json(raw: str):
    raw = re.sub(r'^```(?:json)?\s*', '', raw.strip())
    raw = re.sub(r'\s*```$', '', raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    def extract_json_block(text, opener, closer):
        start = text.find(opener)
        if start == -1: return None
        depth, in_string, escape_next = 0, False, False
        for i, ch in enumerate(text[start:], start):
            if escape_next: escape_next = False; continue
            if ch == '\\' and in_string: escape_next = True; continue
            if ch == '"': in_string = not in_string
            if not in_string:
                if ch == opener: depth += 1
                elif ch == closer:
                    depth -= 1
                    if depth == 0: return text[start:i+1]
        return None
    block = extract_json_block(raw, '{', '}') or extract_json_block(raw, '[', ']')
    if block:
        try: return json.loads(block)
        except: pass
    fixed = re.sub(r',\s*([}\]])', r'\1', block or raw)
    try: return json.loads(fixed)
    except: pass
    truncated = re.sub(r',?\s*"[^"]*"\s*:\s*[^,}\]]*$', '', fixed).strip()
    opens = truncated.count('{') - truncated.count('}')
    aopens = truncated.count('[') - truncated.count(']')
    truncated += ']' * max(0, aopens) + '}' * max(0, opens)
    try: return json.loads(truncated)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON.\nRaw:\n{raw[:500]}") from e

def analyze_with_groq(resume_text, job_desc, outcome, company):
    client = get_client()
    prompt = f"""You are an expert in AI hiring bias, HR fairness, and algorithmic discrimination.
Candidate outcome: "{outcome}" | Company/Role: "{company or 'Not specified'}"
RESUME TEXT: {resume_text[:3000]}
JOB DESCRIPTION: {job_desc or 'Not provided'}
Return ONLY a valid JSON object. No markdown, no explanation. Straight double quotes. No trailing commas.
{{"match_score":<int 0-100>,"bias_risk":"<HIGH|MEDIUM|LOW>","bias_risk_score":<int 0-100>,"outcome_verdict":"<1 short sentence>","matched_skills":["skill1"],"missing_skills":["skill1"],"bias_flags":[{{"title":"<title>","description":"<one sentence, blame the system not candidate>","severity":"<HIGH|MEDIUM|LOW>"}}],"suggestions":[{{"title":"<title>","description":"<one sentence fix>"}}],"summary":"<2 short sentences>"}}
Bias signals: name ethnicity, employment gaps, college prestige, location/zip, gendered language, age signals (graduation year), non-linear career, freelance gaps, cultural/religious indicators. Never blame candidate."""
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], max_tokens=2000, temperature=0.2)
    return safe_parse_json(r.choices[0].message.content)

def ats_simulation(resume_text, job_desc):
    if not job_desc: return None
    jd_words = set(job_desc.lower().split())
    resume_words = set(resume_text.lower().split())
    matched = jd_words.intersection(resume_words)
    score = len(matched) / max(len(jd_words), 1)
    return {"keyword_match": int(score*100), "rejection_probability": int((1-score)*100),
            "stage": "PASS" if score > 0.3 else "REJECTED at Stage 1", "matched_keywords": list(matched)[:10]}

def explain_result(result):
    reasons = []
    if result.get("match_score", 0) < 50: reasons.append("Low keyword alignment with the job description")
    if len(result.get("missing_skills", [])) > 3: reasons.append("Several important skills missing from resume")
    if result.get("bias_risk") == "HIGH": reasons.append("Multiple bias-triggering patterns detected in resume")
    if not reasons: reasons.append("Strong alignment — outcome may be purely bias-driven")
    return reasons

def build_bias_heatmap(resume_text, bias_flags):
    client = get_client()
    flag_summary = "\n".join(f'- [{f.get("severity","LOW")}] {f.get("title","")}: {f.get("description","")}' for f in bias_flags)
    prompt = f"""Given this resume and bias flags, find EXACT short phrases (1-4 words) from the resume that triggered each flag.
RESUME (first 2500 chars): {resume_text[:2500]}
BIAS FLAGS: {flag_summary}
RULES: NEVER highlight names. Only highlight: employment gaps, graduation years, gendered words, college names, location, religious/cultural orgs. Tooltip must blame SYSTEM not candidate.
Return ONLY a JSON array. No markdown. No trailing commas. Max 12 items. Phrases must literally appear in the resume.
[{{"phrase":"exact words","severity":"HIGH","reason":"system-blaming reason under 8 words"}}]"""
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], max_tokens=600, temperature=0.1)
    try:
        phrases = safe_parse_json(r.choices[0].message.content)
        if not isinstance(phrases, list): phrases = []
    except: return html.escape(resume_text), 0
    phrases.sort(key=lambda x: len(x.get("phrase","")), reverse=True)
    highlighted = html.escape(resume_text)
    matched_count, seen = 0, set()
    for item in phrases:
        phrase = item.get("phrase","").strip()
        if not phrase or phrase in seen: continue
        seen.add(phrase)
        sev = item.get("severity","LOW").upper()
        reason = html.escape(item.get("reason","Bias signal detected"))
        cls = {"HIGH":"hm-high","MEDIUM":"hm-med","LOW":"hm-low"}.get(sev,"hm-low")
        esc = html.escape(phrase)
        if esc in highlighted:
            highlighted = highlighted.replace(esc, f'<span class="{cls}" title="{reason}">{esc}</span>', 1)
            matched_count += 1
    return highlighted, matched_count

# ── STATE MANAGEMENT ──
if "step" not in st.session_state: st.session_state.step = 1
if "result" not in st.session_state: st.session_state.result = None
if "resume_text" not in st.session_state: st.session_state.resume_text = None
if "history" not in st.session_state: st.session_state.history = []

# ── RENDER ──
st.markdown(STYLES, unsafe_allow_html=True)
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# Nav
nav_col, bread_col = st.columns([1, 4])
with nav_col:
    if st.button("← Home", key="home_nav"):
        st.switch_page("app.py")
st.markdown('<div class="nav-breadcrumb" style="margin-bottom:1.5rem;font-size:0.75rem;color:#3a3a3a;letter-spacing:0.08em">FairHire Suite → <span style="color:#c9a84c">Job Hiring Bias</span></div>', unsafe_allow_html=True)

# Step indicator
step = st.session_state.step
def step_cls(n):
    if n < step: return "done"
    if n == step: return "active"
    return ""

st.markdown(f"""
<div class="step-bar">
    <div class="step-item {step_cls(1)}">
        <div class="step-num">{"✓" if step>1 else "1"}</div>Upload Resume
    </div>
    <div class="step-item {step_cls(2)}">
        <div class="step-num">{"✓" if step>2 else "2"}</div>Job Context
    </div>
    <div class="step-item {step_cls(3)}">
        <div class="step-num">{"✓" if step>3 else "3"}</div>Bias Analysis
    </div>
    <div class="step-item {step_cls(4)}">
        <div class="step-num">4</div>Heatmap & ATS
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# STEP 1 — Upload Resume
# ══════════════════════════════════════════
if step == 1:
    st.markdown('<h1 class="page-title">Upload your<br>resume.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">We\'ll extract the text and analyze it for bias triggers used by automated hiring systems.</p>', unsafe_allow_html=True)

    st.markdown('<span class="field-label">Resume PDF</span>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue →"):
        if not resume_file:
            st.error("Please upload your resume PDF.")
        else:
            st.session_state.resume_text = extract_pdf_text(resume_file)
            st.session_state.step = 2
            st.rerun()

# ══════════════════════════════════════════
# STEP 2 — Job Context
# ══════════════════════════════════════════
elif step == 2:
    st.markdown('<h1 class="page-title">Tell us about<br>the role.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Provide the job description and outcome. The more detail, the more precise our bias detection.</p>', unsafe_allow_html=True)

    st.markdown('<span class="field-label">Job Description</span>', unsafe_allow_html=True)
    job_desc = st.text_area("Paste full job description", height=180, placeholder="Paste the full job description you applied for...", label_visibility="collapsed", key="jd_input")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="field-label">Application Outcome</span>', unsafe_allow_html=True)
        outcome = st.selectbox("Outcome", ["I was Rejected", "I was Accepted", "No response / Ghosted"], label_visibility="collapsed", key="outcome_input")
    with col2:
        st.markdown('<span class="field-label">Company / Role (optional)</span>', unsafe_allow_html=True)
        company = st.text_input("Company name", placeholder="e.g. Google — Software Engineer", label_visibility="collapsed", key="company_input")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col_b:
        if st.button("Run Bias Analysis →"):
            with st.spinner("Analyzing resume against bias signals..."):
                try:
                    result = analyze_with_groq(
                        st.session_state.resume_text,
                        st.session_state.get("jd_input", ""),
                        outcome, company
                    )
                    st.session_state.result = result
                    st.session_state.job_desc = job_desc
                    st.session_state.outcome = outcome
                    st.session_state.company = company
                    st.session_state.history.append(result)
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

# ══════════════════════════════════════════
# STEP 3 — Bias Analysis Results
# ══════════════════════════════════════════
elif step == 3:
    result = st.session_state.result
    bias_risk = result.get("bias_risk", "MEDIUM")

    st.markdown('<h1 class="page-title">Your bias<br>analysis.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Here\'s what automated hiring systems may have flagged — and why the system is the problem, not you.</p>', unsafe_allow_html=True)

    # Verdict
    st.markdown(f"""
    <div class="verdict-box">
        <div class="r-card-label">AI Verdict</div>
        <div class="verdict-text">{result.get('outcome_verdict','')}</div>
        <div class="verdict-sub">{result.get('summary','')}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3 metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="r-card">
            <div class="r-card-label">Resume Match</div>
            <div class="big-score" style="color:#c9a84c">{result.get('match_score',0)}<span style="font-size:1.5rem">%</span></div>
            <div class="score-sub">Resume ↔ JD Alignment</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="r-card">
            <div class="r-card-label">Bias Risk Score</div>
            <div class="big-score" style="color:#e06666">{result.get('bias_risk_score',0)}<span style="font-size:1.5rem">%</span></div>
            <div class="score-sub">Discrimination Probability</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="r-card">
            <div class="r-card-label">Overall Risk Level</div>
            <div style="margin: 1rem 0"><span class="risk-badge risk-{bias_risk}">{bias_risk} RISK</span></div>
            <div class="score-sub">{len(result.get('bias_flags',[]))} flags detected</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    # Why this result
    st.markdown('<div class="r-card-label">Why this result?</div>', unsafe_allow_html=True)
    for r in explain_result(result):
        st.markdown(f'<div style="font-size:0.85rem;color:#6b6960;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04)">→ {r}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    # Flags + Suggestions
    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        st.markdown('<div class="r-card-label">Bias Flags Detected</div>', unsafe_allow_html=True)
        flags = result.get("bias_flags", [])
        if flags:
            for f in flags:
                sev = f.get("severity","MEDIUM")
                st.markdown(f"""
                <div class="flag-row {sev}">
                    <span class="flag-sev sev-{sev}">{sev}</span>
                    <div>
                        <div class="flag-title">{f.get('title','')}</div>
                        <div class="flag-desc">{f.get('description','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="sug-row"><div class="sug-dot"></div><div><div class="sug-title">No major bias flags</div><div class="sug-desc">Resume appears clean from common ATS bias triggers.</div></div></div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="r-card-label">Recommendations</div>', unsafe_allow_html=True)
        for s in result.get("suggestions", []):
            st.markdown(f"""
            <div class="sug-row">
                <div class="sug-dot"></div>
                <div>
                    <div class="sug-title">{s.get('title','')}</div>
                    <div class="sug-desc">{s.get('description','')}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        matched = result.get("matched_skills",[])
        missing = result.get("missing_skills",[])
        if matched or missing:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="r-card-label">Skill Gap Analysis</div>', unsafe_allow_html=True)
            if matched:
                tags = "".join(f'<span class="tag tag-match">{s}</span>' for s in matched)
                st.markdown(f'<div style="font-size:0.68rem;color:#4a4a4a;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem">Matched</div><div class="tag-row">{tags}</div>', unsafe_allow_html=True)
            if missing:
                tags = "".join(f'<span class="tag tag-miss">{s}</span>' for s in missing)
                st.markdown(f'<div style="font-size:0.68rem;color:#4a4a4a;letter-spacing:0.1em;text-transform:uppercase;margin:0.8rem 0 0.4rem">Missing</div><div class="tag-row">{tags}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    # Download + nav
    report_text = f"FairHire Analysis Report\nRole: {st.session_state.get('company','')}\nMatch Score: {result.get('match_score')}%\nBias Risk: {bias_risk}\n\nVerdict: {result.get('outcome_verdict','')}\n\nSummary: {result.get('summary','')}\n\nBias Flags:\n" + "\n".join(f"- [{f['severity']}] {f['title']}: {f['description']}" for f in result.get("bias_flags",[]))
    col_dl, col_next = st.columns([1,2])
    with col_dl:
        st.download_button("↓ Download Report", data=report_text, file_name="FairHire_Job_Analysis.txt", mime="text/plain")
    with col_next:
        if st.button("Continue to Heatmap & ATS →"):
            st.session_state.step = 4
            st.rerun()

# ══════════════════════════════════════════
# STEP 4 — Heatmap & ATS + Improve
# ══════════════════════════════════════════
elif step == 4:
    result = st.session_state.result
    resume_text = st.session_state.resume_text
    job_desc = st.session_state.get("job_desc","")

    st.markdown('<h1 class="page-title">Heatmap &<br>ATS simulation.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">See exactly where bias lives in your resume. Hover highlighted phrases to understand why they trigger automated systems.</p>', unsafe_allow_html=True)

    flags = result.get("bias_flags",[])
    if flags:
        with st.spinner("Mapping bias phrases onto resume..."):
            heatmap_html, phrase_count = build_bias_heatmap(resume_text, flags)

        st.markdown(f"""
        <div class="legend">
            <div class="legend-item"><div class="leg-dot" style="background:#7a2a2a"></div>High</div>
            <div class="legend-item"><div class="leg-dot" style="background:#8a7020"></div>Medium</div>
            <div class="legend-item"><div class="leg-dot" style="background:#3a6040"></div>Low</div>
            <div style="margin-left:auto;font-size:0.72rem;color:#4a4a4a;letter-spacing:0.08em">{phrase_count} phrase{"s" if phrase_count!=1 else ""} detected</div>
        </div>
        <div class="heatmap-box">{heatmap_html}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="sug-row"><div class="sug-dot"></div><div><div class="sug-title">No bias phrases detected</div><div class="sug-desc">Resume text appears free of common automated bias triggers.</div></div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    # ATS Simulation
    st.markdown('<div class="r-card-label">ATS Simulation</div>', unsafe_allow_html=True)
    ats = ats_simulation(resume_text, job_desc)
    if ats:
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            st.markdown(f'<div class="r-card"><div class="r-card-label">Keyword Match</div><div class="big-score" style="color:#c9a84c">{ats["keyword_match"]}<span style="font-size:1.5rem">%</span></div></div>', unsafe_allow_html=True)
        with ac2:
            st.markdown(f'<div class="r-card"><div class="r-card-label">Rejection Probability</div><div class="big-score" style="color:#e06666">{ats["rejection_probability"]}<span style="font-size:1.5rem">%</span></div></div>', unsafe_allow_html=True)
        with ac3:
            color = "#e06666" if "REJECTED" in ats["stage"] else "#6daa7f"
            st.markdown(f'<div class="r-card"><div class="r-card-label">ATS Verdict</div><div style="margin-top:0.8rem;font-size:0.9rem;font-weight:600;color:{color}">{ats["stage"]}</div><div class="score-sub" style="margin-top:0.4rem">Top keywords: {", ".join(ats["matched_keywords"][:5])}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.85rem;color:#4a4a4a;padding:1rem 0">Add a job description to enable ATS simulation.</div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    # Resume improvement simulator
    st.markdown('<div class="r-card-label">Resume Improvement Simulator</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub" style="margin-bottom:1rem">Edit your resume below and recalculate to see how changes affect your bias risk and match score.</p>', unsafe_allow_html=True)

    edited = st.text_area("Edit Resume", value=resume_text, height=220, label_visibility="collapsed")
    if st.button("↻ Recalculate Scores"):
        with st.spinner("Re-analyzing..."):
            new_result = analyze_with_groq(edited, job_desc, st.session_state.get("outcome",""), st.session_state.get("company",""))
        rc1, rc2 = st.columns(2)
        with rc1:
            delta = new_result.get("match_score",0) - result.get("match_score",0)
            st.metric("Match Score", f"{new_result.get('match_score',0)}%", delta=f"{delta:+d}%")
        with rc2:
            delta2 = new_result.get("bias_risk_score",0) - result.get("bias_risk_score",0)
            st.metric("Bias Risk Score", f"{new_result.get('bias_risk_score',0)}%", delta=f"{delta2:+d}%")

    st.markdown("<hr class='section-div'>", unsafe_allow_html=True)

    col_b, col_r = st.columns([1,2])
    with col_b:
        if st.button("← Back to Analysis"):
            st.session_state.step = 3
            st.rerun()
    with col_r:
        if st.button("Start Over"):
            for k in ["step","result","resume_text","job_desc","outcome","company"]:
                if k in st.session_state: del st.session_state[k]
            st.session_state.step = 1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
