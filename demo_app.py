"""
ResearchPilot — Streamlit Demo App
Fully self-contained demo — no API keys needed.
Amazon Nova AI Hackathon 2026 | Team Debug Thugs
"""
import streamlit as st
import time

st.set_page_config(
    page_title="ResearchPilot — Amazon Nova",
    page_icon="🔬",
    layout="wide",
)

st.markdown("""
<style>
body { background: #0f172a; }
.main { background: #0f172a; }
.block-container { padding-top: 1.5rem; }

.hero {
    background: linear-gradient(135deg, #0A1628 0%, #0D3259 100%);
    border: 1px solid #22D3EE33;
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.hero h1 { color: #22D3EE; font-size: 2.8rem; margin: 0 0 0.3rem 0; }
.hero p  { color: #94A3B8; font-size: 1.05rem; margin: 0 0 1rem 0; }
.badge {
    display: inline-block;
    background: #22D3EE22;
    border: 1px solid #22D3EE66;
    color: #22D3EE;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px;
}
.step-card {
    background: #0D2144;
    border: 1px solid #1E3A6B;
    border-left: 4px solid #22D3EE;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin: 0.4rem 0;
    font-size: 0.95rem;
    color: #E2E8F0;
}
.step-card.done  { border-left-color: #10B981; background: #0A2E1E; }
.step-card.active{ border-left-color: #F59E0B; background: #1E1A00; animation: pulse 1s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }

.source-card {
    background: #0D2144;
    border: 1px solid #1E3A6B;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.3rem 0;
    color: #CBD5E1;
    font-size: 0.88rem;
}
.metric-box {
    background: #0D2144;
    border: 1px solid #1E3A6B;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-box .val { font-size: 1.8rem; font-weight: 700; color: #22D3EE; }
.metric-box .lbl { font-size: 0.8rem; color: #64748B; margin-top: 2px; }
.report-box {
    background: #0A1628;
    border: 1px solid #1E3A6B;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    color: #CBD5E1;
    font-size: 0.95rem;
    line-height: 1.7;
}
.contra {
    background: #1E0A0A;
    border-left: 4px solid #EF4444;
    border-radius: 6px;
    padding: 0.7rem 1rem;
    margin: 0.5rem 0;
    color: #FCA5A5;
    font-size: 0.9rem;
}
.voice-box {
    background: #0A2218;
    border: 1px solid #10B981;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #6EE7B7;
    font-size: 0.95rem;
    font-style: italic;
}
.tag { color: #0891B2; font-weight: 600; font-size: 0.82rem; }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🔬 ResearchPilot</h1>
  <p>AI-Powered Research Automation Agent — Turn hours of research into minutes</p>
  <span class="badge">Nova 2 Pro</span>
  <span class="badge">Nova 2 Lite</span>
  <span class="badge">Nova 2 Sonic</span>
  <span class="badge">Nova Act</span>
  <span class="badge">Nova Embeddings</span>
  <span class="badge">AWS Bedrock</span>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.text_input("Nova Act API Key", type="password", placeholder="nova-act-...", help="From nova.amazon.com/act")
    st.text_input("AWS Access Key ID", type="password")
    st.text_input("AWS Secret Access Key", type="password")
    st.selectbox("AWS Region", ["us-east-1", "us-west-2", "eu-west-1"])
    st.markdown("---")
    st.markdown("### 🔧 Settings")
    st.slider("Max Sources", 3, 15, 8)
    st.checkbox("Extended Thinking (Nova Pro)", value=True)
    st.slider("Confidence Threshold", 0.3, 0.9, 0.6)
    st.checkbox("Voice Output (Nova Sonic)", value=False)
    st.markdown("---")
    st.markdown("### 📎 Upload Documents")
    st.file_uploader("PDFs or Images", type=["pdf","png","jpg"], accept_multiple_files=True)
    st.markdown("---")
    st.markdown("**Team Debug Thugs**")
    st.markdown("Gaurav Kumar Nayak & Mohit Paul")
    st.markdown("Amazon Nova AI Hackathon 2026")

# ── QUERY INPUT ───────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_area("🔍 Research Query",
        value="Latest advances in solid-state batteries for electric vehicles",
        height=90)
with col2:
    st.markdown("<br/>", unsafe_allow_html=True)
    st.button("🎤 Voice Input", use_container_width=True)
    run = st.button("🚀 Start Research", use_container_width=True, type="primary")

# ── EXAMPLE CHIPS ─────────────────────────────────────────────────
st.markdown("**Quick examples:**")
ex_cols = st.columns(4)
examples = [
    "Impact of quantum computing on cryptography",
    "mRNA vaccines beyond COVID-19",
    "Carbon capture: current state & limits",
    "Multimodal LLM architecture trends 2025",
]
for i, (col, ex) in enumerate(zip(ex_cols, examples)):
    with col:
        if st.button(ex[:35]+"…", key=f"ex{i}", use_container_width=True):
            st.session_state["run_query"] = ex
            st.rerun()

if "run_query" in st.session_state:
    query = st.session_state.pop("run_query")
    run = True

# ── PIPELINE SIMULATION ───────────────────────────────────────────
PIPELINE_STEPS = [
    ("📋", "Nova 2 Lite",        "Planning research strategy & decomposing query into sub-tasks"),
    ("🌐", "Nova Act",           "Browsing Google Scholar — extracting academic papers"),
    ("🌐", "Nova Act",           "Browsing arXiv.org — finding preprints & recent research"),
    ("🌐", "Nova Act",           "Searching Google News — capturing latest developments"),
    ("🌐", "Nova Act",           "Extracting Wikipedia background context"),
    ("📄", "Nova 2 Pro",         "Analyzing Source 1 — Kim et al. 2024 (multimodal PDF)"),
    ("📄", "Nova 2 Pro",         "Analyzing Source 4 — Zhang et al. 2023 (chart extraction)"),
    ("🔍", "Nova Embeddings",    "Generating semantic vectors for all 6 sources"),
    ("🔍", "Nova Embeddings",    "FAISS cosine similarity reranking by query relevance"),
    ("🔎", "Nova 2 Pro",         "Contradiction detection across sources (extended thinking)"),
    ("🧠", "Nova 2 Pro",         "Synthesizing full report (8,000 token reasoning budget)"),
    ("📝", "Nova 2 Lite",        "Generating executive summary for voice delivery"),
    ("🔊", "Nova 2 Sonic",       "Converting summary to speech (TTS synthesis)"),
]

SOURCES = [
    ("academic", "🟢 0.96", "Solid-State Batteries: Progress & Prospects",      "Kim et al., arXiv 2024"),
    ("academic", "🟢 0.88", "Electrolyte Challenges in Solid-State Li-Ion Cells","Zhang et al., Nature Energy 2023"),
    ("news",     "🟢 0.91", "Toyota's All-Solid-State EV Battery Breakthrough",  "Reuters, 2024"),
    ("news",     "🟡 0.82", "CATL Condensed Battery: Semi-Solid Innovation",     "CATL Press Release, 2024"),
    ("web",      "🟡 0.79", "QuantumScape 2024 Production Update",               "quantumscape.com, 2024"),
    ("wiki",     "🟡 0.84", "Solid-state battery — Wikipedia",                   "Wikipedia"),
]

REPORT = """
## Executive Summary
Solid-state batteries (SSBs) represent the next frontier in EV energy storage, offering theoretical
energy densities **2–3× higher** than conventional lithium-ion cells with significantly improved safety.
As of 2024, several companies are reaching pilot production, though mass commercialization faces
persistent materials science challenges.

## Key Findings
- **Energy density:** Prototype SSBs achieve 400–500 Wh/kg vs ~250 Wh/kg for Li-ion `[Source 1]`
- **Toyota timeline:** Targeting **2027–2028** for initial solid-state EV production `[Source 3]`
- **Main bottleneck:** Solid electrolyte ionic conductivity at room temperature remains 2–5× below liquid `[Source 2]`
- **QuantumScape milestone:** 800+ charge cycles at >80% capacity retention achieved in 2024 `[Source 5]`
- **CATL semi-solid:** 500 Wh/kg condensed battery entering production 2025 `[Source 4]`

## Detailed Analysis

### Current State of Knowledge
Solid-state batteries replace liquid electrolytes with solid alternatives — oxides (LLZO), sulfides (LGPS),
or polymers. Each trades off ionic conductivity vs. manufacturability vs. electrochemical stability.

### Recent Developments (2023–2024)
Multiple companies reached inflection points: QuantumScape demonstrated automotive-grade cycle life;
Toyota opened a solid-state battery pilot line; CATL's condensed battery entered commercial production.

## Confidence Assessment
| Finding | Confidence |
|---------|-----------|
| Energy density advantage | 🟢 High |
| Toyota 2027 timeline | 🟡 Medium |
| Manufacturing cost parity | 🔴 Low |
"""

CONTRADICTIONS = [
    "Toyota states 2027 production target [Source 3] — BloombergNEF analysts estimate 2030+ for meaningful volume [Source 6]",
    "Academia favors oxide ceramic electrolytes for stability — Samsung SDI & Solid Power pursuing sulfide routes for conductivity",
]

VOICE_SUMMARY = (
    "Solid-state batteries show great promise for electric vehicles, with prototypes achieving "
    "twice the energy density of current lithium-ion cells. Toyota and QuantumScape are closest "
    "to production, targeting 2027 to 2028. The main challenge remains manufacturing at scale, "
    "with experts divided on whether mass commercialization will arrive before 2030."
)

if run and query:
    st.markdown("---")
    st.markdown(f"### 🔬 Researching: *{query}*")

    # ── PIPELINE STEPS ─────────────────────────────────────────
    st.markdown("#### Pipeline Execution")
    placeholders = []
    for step in PIPELINE_STEPS:
        placeholders.append(st.empty())

    # Render all as pending first
    for i, (icon, model, desc) in enumerate(PIPELINE_STEPS):
        placeholders[i].markdown(
            f'<div class="step-card">⬜ <b style="color:#64748B">{model}</b> — {desc}</div>',
            unsafe_allow_html=True
        )

    time.sleep(0.3)

    delays = [0.6, 1.0, 0.9, 0.7, 0.6, 1.0, 0.9, 0.6, 0.5, 1.3, 1.8, 0.5, 0.7]

    for i, (icon, model, desc) in enumerate(PIPELINE_STEPS):
        # Mark current as active
        placeholders[i].markdown(
            f'<div class="step-card active">⚡ <b style="color:#F59E0B">{model}</b> — {desc}</div>',
            unsafe_allow_html=True
        )
        time.sleep(delays[i])
        # Mark done
        placeholders[i].markdown(
            f'<div class="step-card done">✅ <b style="color:#10B981">{model}</b> — {desc}</div>',
            unsafe_allow_html=True
        )

    # ── METRICS ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📊 Results")
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        ("6", "Sources Analyzed"),
        ("5", "Nova Models Used"),
        ("84%", "Confidence Score"),
        ("2", "Contradictions"),
        ("~4 min", "Pipeline Time"),
    ]
    for col, (val, lbl) in zip([m1,m2,m3,m4,m5], metrics):
        with col:
            st.markdown(f'<div class="metric-box"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    # ── SOURCES ────────────────────────────────────────────────
    st.markdown("#### 📚 Sources (Nova Embeddings Ranked)")
    s1, s2 = st.columns(2)
    for i, (stype, score, title, meta) in enumerate(SOURCES):
        col = s1 if i % 2 == 0 else s2
        with col:
            st.markdown(
                f'<div class="source-card"><b>{score}</b> &nbsp;|&nbsp; '
                f'<span style="color:#22D3EE">{stype}</span> &nbsp;|&nbsp; '
                f'<b style="color:#E2E8F0">{title}</b><br/>'
                f'<span style="color:#64748B;font-size:0.82rem">{meta}</span></div>',
                unsafe_allow_html=True
            )

    # ── CONTRADICTIONS ─────────────────────────────────────────
    st.markdown("#### ⚠️ Contradictions Detected (Nova 2 Pro Extended Thinking)")
    for c in CONTRADICTIONS:
        st.markdown(f'<div class="contra">⚠️ {c}</div>', unsafe_allow_html=True)

    # ── REPORT ─────────────────────────────────────────────────
    st.markdown("#### 📄 Synthesized Report (Nova 2 Pro)")
    with st.container():
        st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
        st.markdown(REPORT)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── VOICE SUMMARY ──────────────────────────────────────────
    st.markdown("#### 🔊 Voice Summary (Nova 2 Sonic)")
    st.markdown(f'<div class="voice-box">🔊 &nbsp;{VOICE_SUMMARY}</div>', unsafe_allow_html=True)

    # ── DOWNLOAD ───────────────────────────────────────────────
    st.markdown("#### 💾 Download Report")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button("📄 Download Markdown", data=REPORT, file_name="researchpilot_report.md", use_container_width=True)
    with d2:
        st.download_button("🌐 Download HTML", data=f"<html><body>{REPORT}</body></html>", file_name="researchpilot_report.html", use_container_width=True)
    with d3:
        st.download_button("📊 Download JSON", data='{"query":"'+query+'","confidence":0.84,"sources":6}', file_name="researchpilot_report.json", use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="tag">#AmazonNova &nbsp; Built by Team Debug Thugs — Gaurav Kumar Nayak & Mohit Paul &nbsp;|&nbsp; Amazon Nova AI Hackathon 2026</p>', unsafe_allow_html=True)

elif run and not query:
    st.warning("Please enter a research query first.")
