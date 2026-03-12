"""
ResearchPilot — Streamlit Web Dashboard
Beautiful, interactive frontend for the research agent.
Amazon Nova AI Hackathon 2026 | Team Debug Thugs
"""
import sys
import json
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchPilot — Amazon Nova",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
  .main-header {
    background: linear-gradient(135deg, #0A1628, #0D3259);
    color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;
    text-align: center;
  }
  .nova-badge {
    background: #22D3EE; color: #0A1628; padding: 4px 12px;
    border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    display: inline-block; margin: 2px;
  }
  .metric-card {
    background: white; border: 1px solid #E2E8F0; border-radius: 8px;
    padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  .status-green { color: #10B981; font-weight: bold; }
  .status-yellow { color: #F59E0B; font-weight: bold; }
  .status-red { color: #EF4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🔬 ResearchPilot</h1>
  <p style="color:#94A3B8; margin:0">AI-Powered Research Automation Agent</p>
  <br/>
  <span class="nova-badge">Nova 2 Pro</span>
  <span class="nova-badge">Nova 2 Lite</span>
  <span class="nova-badge">Nova 2 Sonic</span>
  <span class="nova-badge">Nova Act</span>
  <span class="nova-badge">Nova Embeddings</span>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar: Configuration ──────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    nova_act_key = st.text_input(
        "Nova Act API Key",
        type="password",
        help="From nova.amazon.com/act",
        placeholder="nova-act-..."
    )
    aws_key = st.text_input("AWS Access Key ID", type="password")
    aws_secret = st.text_input("AWS Secret Access Key", type="password")
    aws_region = st.selectbox(
        "AWS Region",
        ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
    )

    st.markdown("---")
    st.markdown("### 🔧 Research Settings")
    num_sources = st.slider("Max Sources", 3, 15, 8)
    use_extended_thinking = st.checkbox("Extended Thinking (Nova Pro)", value=True)
    confidence_threshold = st.slider("Confidence Threshold", 0.3, 0.9, 0.6)
    voice_output = st.checkbox("Voice Output (Nova Sonic)", value=False)

    st.markdown("---")
    st.markdown("### 📎 Upload Documents")
    uploaded_files = st.file_uploader(
        "PDFs or Images",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    st.markdown("---")
    st.markdown("**Built by:** Debug Thugs")
    st.markdown("**Amazon Nova AI Hackathon 2026**")

# ─── Main Area: Query Input ──────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_area(
        "🔍 Research Query",
        placeholder="e.g. What are the latest advances in solid-state battery technology for electric vehicles?",
        height=100,
    )
with col2:
    st.markdown("<br/>", unsafe_allow_html=True)
    voice_btn = st.button("🎤 Voice Input", use_container_width=True)
    run_btn = st.button("🚀 Start Research", use_container_width=True, type="primary")

# ─── Example Queries ────────────────────────────────────────────
st.markdown("**Quick examples:**")
examples = [
    "Latest advances in mRNA vaccines beyond COVID-19",
    "Impact of quantum computing on cryptography in 2025",
    "Carbon capture technologies: current state and limitations",
    "Multimodal LLMs: architecture trends and benchmarks",
]
cols = st.columns(len(examples))
for i, (col, ex) in enumerate(zip(cols, examples)):
    with col:
        if st.button(ex[:40]+"...", key=f"ex_{i}", use_container_width=True):
            st.session_state.example_query = ex

if "example_query" in st.session_state:
    query = st.session_state.pop("example_query")

# ─── Pipeline Execution ──────────────────────────────────────────
if run_btn and query:
    # Set env variables from UI
    import os
    if nova_act_key:
        os.environ["NOVA_ACT_API_KEY"] = nova_act_key
    if aws_key:
        os.environ["AWS_ACCESS_KEY_ID"] = aws_key
    if aws_secret:
        os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret
    os.environ["AWS_DEFAULT_REGION"] = aws_region

    # Progress display
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_status(msg, pct):
            status_text.markdown(f"**{msg}**")
            progress_bar.progress(pct)
            time.sleep(0.3)

        update_status("📋 Planning research strategy (Nova 2 Lite)...", 10)

        # Run pipeline
        try:
            from src.orchestrator import ResearchPilotOrchestrator
            orchestrator = ResearchPilotOrchestrator()

            update_status("🌐 Searching web with Nova Act...", 25)

            # Save uploaded files
            doc_paths = []
            for uf in (uploaded_files or []):
                tmp = f"/tmp/{uf.name}"
                with open(tmp, "wb") as f:
                    f.write(uf.read())
                doc_paths.append(tmp)

            update_status("📄 Analyzing sources with Nova 2 Pro (multimodal)...", 50)
            update_status("🔍 Semantic reranking with Nova Embeddings...", 65)
            update_status("🔎 Detecting contradictions (extended thinking)...", 75)
            update_status("🧠 Synthesizing report (Nova 2 Pro)...", 88)

            result = orchestrator.run(
                query=query,
                voice_output=voice_output,
                extra_docs=doc_paths,
                save_report=True,
            )

            update_status("✅ Complete!", 100)

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure your AWS credentials and Nova Act API key are configured.")
            result = None

    # ─── Results Display ──────────────────────────────────────────
    if result:
        st.markdown("---")
        st.markdown("## 📊 Research Results")

        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        conf = result.get("confidence_score", 0)
        conf_class = "status-green" if conf >= 0.75 else "status-yellow" if conf >= 0.5 else "status-red"
        with m1:
            st.metric("Sources Analyzed", result.get("num_sources", 0))
        with m2:
            st.metric("Confidence Score", f"{conf:.0%}")
        with m3:
            st.metric("Human Review Needed",
                      "Yes ⚠️" if result.get("needs_human_review") else "No ✅")
        with m4:
            st.metric("Report Sections", "7")

        # Report
        st.markdown("### 📄 Full Report")
        st.markdown(result.get("report_markdown", "No report generated."))

        # Voice summary
        if result.get("voice_summary"):
            st.markdown("### 🔊 Voice Summary")
            st.info(result["voice_summary"])

        # Sources
        if result.get("sources"):
            with st.expander(f"📚 Sources ({len(result['sources'])})"):
                for i, src in enumerate(result["sources"]):
                    st.markdown(
                        f"{i+1}. **[{src['title']}]({src['url']})** — *{src['type']}*"
                    )

        # Download buttons
        st.markdown("### 💾 Download Report")
        if result.get("saved_files"):
            dcols = st.columns(3)
            for i, (fmt, path) in enumerate(result["saved_files"].items()):
                with dcols[i % 3]:
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                        st.download_button(
                            f"Download {fmt.upper()}",
                            data=content,
                            file_name=Path(path).name,
                            use_container_width=True,
                        )
                    except Exception:
                        pass

elif run_btn and not query:
    st.warning("Please enter a research query first.")
