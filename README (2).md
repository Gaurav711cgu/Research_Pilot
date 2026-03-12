<div align="center">

<img src="https://img.shields.io/badge/Amazon%20Nova-AI%20Hackathon%202026-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/Category-Agentic%20AI-22D3EE?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<br/><br/>

# 🔬 ResearchPilot
### AI-Powered Research Automation Agent

**"Turn hours of research into minutes — voice-in, insight-out."**

ResearchPilot is a multi-agent AI system that orchestrates all five Amazon Nova models into a single autonomous research pipeline. Speak a question → get a fully cited, contradiction-detected, confidence-scored research report in under 5 minutes.

<br/>

[🚀 Quick Start](#-quick-start) &nbsp;•&nbsp; [🏗️ Architecture](#️-architecture) &nbsp;•&nbsp; [✨ Features](#-features) &nbsp;•&nbsp; [🎬 Demo](#-demo) &nbsp;•&nbsp; [📁 Structure](#-project-structure)

</div>

---

## 🎬 Demo

Run instantly — **no API keys needed:**

```bash
pip install rich
python demo_runner.py
```

Launch the Streamlit UI:

```bash
pip install streamlit
streamlit run demo_app.py
```

What you'll see:

```
Query: "Latest advances in solid-state batteries for electric vehicles"

📋 Nova 2 Lite     → Planning research strategy & decomposing into sub-queries
🌐 Nova Act        → Browsing Google Scholar — extracting academic papers
🌐 Nova Act        → Browsing arXiv.org — finding latest preprints
🌐 Nova Act        → Scraping Google News — capturing recent developments
🌐 Nova Act        → Extracting Wikipedia background context
📄 Nova 2 Pro      → Analyzing Source 1 — Kim et al. 2024 (multimodal PDF)
📄 Nova 2 Pro      → Analyzing Source 4 — Zhang et al. 2023 (chart extraction)
🔍 Nova Embeddings → Generating semantic vectors for all 6 sources
🔍 Nova Embeddings → FAISS cosine similarity reranking by relevance
🔎 Nova 2 Pro      → Contradiction detection (extended thinking — 8,000 tokens)
🧠 Nova 2 Pro      → Synthesizing 7-section report with citations
📝 Nova 2 Lite     → Generating executive summary
🔊 Nova 2 Sonic    → Delivering voice summary (TTS)

✅ Complete in ~4 min | Sources: 6 | Confidence: 🟢 84% | Contradictions: 2
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│           Voice Input (Nova 2 Sonic STT)  /  Streamlit UI        │
└───────────────────────────┬──────────────────────────────────────┘
                            │ query
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR AGENT                           │
│                        Nova 2 Pro                                │
│          Decomposes query → plans parallel agent execution       │
└──────────┬─────────────────────────────────┬─────────────────────┘
           │                                 │
     ┌─────┴──────────────┐     ┌────────────┴───────────┐
     ▼                    ▼     ▼                        ▼
┌──────────────┐  ┌──────────────────┐        ┌──────────────────┐
│ Web Search   │  │ Document Reader  │        │ Embedding Search │
│ Agent        │  │ Agent            │        │ Agent            │
│              │  │                  │        │                  │
│ Nova Act     │  │ Nova 2 Pro       │        │ Nova Embeddings  │
│ ──────────── │  │ ──────────────── │        │ ──────────────── │
│ Google       │  │ PDF text extract │        │ FAISS cosine     │
│ Scholar      │  │ Chart/image read │        │ similarity       │
│ arXiv        │  │ Table extraction │        │ Source reranking │
│ Wikipedia    │  │ Credibility score│        │ Noise filtering  │
│ Google News  │  │                  │        │                  │
└──────┬───────┘  └────────┬─────────┘        └────────┬─────────┘
       │                   │                           │
       └───────────────────┼───────────────────────────┘
                           │ ranked + analyzed sources
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      SYNTHESIS AGENT                             │
│                        Nova 2 Pro                                │
│   Extended thinking → contradiction detection across all sources │
│   7-section structured report → confidence score computation     │
│   Human-escalation flag when confidence < configurable threshold │
└───────────────────────────┬──────────────────────────────────────┘
                            │ final report
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        OUTPUT LAYER                              │
│  Nova 2 Sonic TTS  ·  Markdown  ·  HTML  ·  JSON  ·  Dashboard  │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Nova Model | Description |
|---------|-----------|-------------|
| 🎤 Voice query input | Nova 2 Sonic | Speak your research question naturally |
| 🌐 Autonomous web research | Nova Act | Browses Scholar, arXiv, Wikipedia, news |
| 📄 Multimodal doc analysis | Nova 2 Pro | Reads PDFs, images, charts, tables |
| 🔍 Semantic source ranking | Nova Embeddings | FAISS cosine similarity reranking |
| 🔎 Contradiction detection | Nova 2 Pro | Extended thinking across all sources |
| 🧠 Deep report synthesis | Nova 2 Pro | 7-section cited report + confidence scores |
| 📝 Fast structured output | Nova 2 Lite | Research planning + executive summary |
| 🔊 Voice report delivery | Nova 2 Sonic | TTS executive summary playback |
| ⚠️ Human escalation | Confidence engine | Auto-flags low-confidence reports |
| 💾 Multi-format export | Report formatter | Markdown / HTML / JSON output |

---

## 🔧 Amazon Nova Models Used

| Model | Role | Key Capability Used |
|-------|------|-------------------|
| **Nova 2 Pro** | Orchestration · Doc analysis · Contradiction detection · Synthesis | Extended thinking (8,000 token budget) + Multimodal vision |
| **Nova 2 Lite** | Research planning · Structured JSON · Executive summary | Fast, cost-efficient structured output |
| **Nova 2 Sonic** | Voice input (STT) + Voice output (TTS) | Purpose-built real-time speech model |
| **Nova Act** | Autonomous browser research across 4+ sites | Natural language browser control |
| **Nova Embeddings** | Semantic reranking · FAISS similarity search | Text + image vector embeddings |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- AWS account with Bedrock access (`us-east-1`)
- Nova Act API key — get it from [nova.amazon.com/act](https://nova.amazon.com/act)

### Install

```bash
git clone https://github.com/YOUR_USERNAME/researchpilot.git
cd researchpilot
pip install -r requirements.txt
```

### Configure

```bash
# Windows
set AWS_ACCESS_KEY_ID=your_key
set AWS_SECRET_ACCESS_KEY=your_secret
set AWS_DEFAULT_REGION=us-east-1
set NOVA_ACT_API_KEY=your_nova_act_key

# Mac / Linux
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
export NOVA_ACT_API_KEY=your_nova_act_key
```

### Run

```bash
# No API keys needed — demo mode
python demo_runner.py

# No API keys needed — Streamlit UI
streamlit run demo_app.py

# Full pipeline with real Nova models
python src/main.py --query "Latest advances in solid-state batteries for EVs"

# Voice input mode (speaks back to you too)
python src/main.py --voice --speak

# Analyze your own uploaded documents
python src/main.py --query "summarize key findings" --docs paper.pdf chart.png
```

---

## 📁 Project Structure

```
researchpilot/
│
├── demo_runner.py              ← Start here — rich terminal demo, no API keys
├── demo_app.py                 ← Streamlit UI demo, no API keys
├── requirements.txt
│
├── src/
│   ├── main.py                 # CLI entry point + argument parser
│   ├── orchestrator.py         # Central planning agent (Nova 2 Pro)
│   └── config.py               # AWS + Nova model configuration
│
├── agents/
│   ├── web_search_agent.py     # Nova Act browser automation agent
│   ├── doc_reader_agent.py     # Nova 2 Pro multimodal document reader
│   ├── synthesis_agent.py      # Nova 2 Pro synthesis + confidence scoring
│   └── voice_interface.py      # Nova 2 Sonic speech I/O
│
├── tools/
│   ├── bedrock_client.py       # Unified Bedrock API client (all 5 Nova models)
│   ├── embedding_search.py     # FAISS + Nova Embeddings semantic search
│   └── report_formatter.py     # Markdown / HTML / JSON report builder
│
├── frontend/
│   └── app.py                  # Full Streamlit dashboard (requires AWS keys)
│
└── docs/
    └── architecture.md         # Deep-dive architecture documentation
```

---

## 🧠 How It Works

### Step 1 — Research Planning (Nova 2 Lite)
Nova 2 Lite decomposes the query into specific sub-questions, identifies needed source types, and plans the parallel agent execution graph — fast and cost-efficient.

### Step 2 — Autonomous Web Research (Nova Act)
Nova Act navigates real websites using natural language:
```python
with NovaAct(starting_page="https://scholar.google.com") as agent:
    agent.act(f'Search for "{query}" and press Enter')
    agent.act("Extract result 1 as JSON: title, authors, year, snippet, link")
```
No CSS selectors. No scraping fragility. Nova Act handles JavaScript rendering, pop-ups, and pagination automatically.

### Step 3 — Multimodal Document Analysis (Nova 2 Pro)
Every source — web pages, PDFs, charts, tables — is analyzed with Nova 2 Pro. Images and charts are passed directly to the multimodal API. Key claims, statistics, and credibility scores are extracted per source.

### Step 4 — Semantic Reranking (Nova Embeddings + FAISS)
All sources are embedded into a shared vector space using Nova Multimodal Embeddings. Sources are ranked by cosine similarity to the original query via FAISS. Sources scoring below 0.3 are filtered before synthesis.

### Step 5 — Contradiction Detection (Nova 2 Pro Extended Thinking)
Nova 2 Pro gets an 8,000-token thinking budget to reason across all sources:
```
⚠️ Contradiction found:
   Toyota states 2027 production target [Source 2]
   BloombergNEF estimates 2030+ for meaningful volume [Source 3]
   → Gap reflects pilot-scale vs. gigawatt-scale definitions
```

### Step 6 — Report Synthesis (Nova 2 Pro)
A 7-section structured report: Executive Summary → Key Findings → Detailed Analysis → Contradictions & Debates → Knowledge Gaps → Practical Implications → Confidence Assessment.

### Step 7 — Voice Delivery (Nova 2 Sonic)
The executive summary is synthesized to speech and played back. Full report is exported in Markdown, HTML, and JSON simultaneously.

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Average pipeline time | ~4 minutes |
| Sources analyzed per run | 6–10 |
| Nova models used | 5 |
| Parallel agents | 3 |
| Output formats | Markdown · HTML · JSON |
| Confidence range | 0–100% |
| Human escalation threshold | Configurable (default 60%) |

---

## 🌍 Real-World Impact

| User | Without ResearchPilot | With ResearchPilot |
|------|-----------------------|--------------------|
| Student literature review | 6–12 hours | 20–40 minutes |
| Analyst sector briefing | 4–8 hours | 15–30 minutes |
| Journalist fact-check | 2–4 hours | 10–20 minutes |

Knowledge workers spend **30–40% of their time on information gathering and synthesis.** ResearchPilot makes that the fastest part of the job, not the slowest.

---

## 🛡️ Reliability

- **Fallback architecture** — every Nova component falls back gracefully (arXiv API, Wikipedia REST, in-memory FAISS) so the system runs even without all API keys
- **Confidence scoring** — computed from source count, diversity, academic-to-web ratio, and contradiction density
- **Human escalation** — automatically flags reports when confidence falls below the configurable threshold
- **Parallel execution** — web search, document reading, and image analysis run simultaneously via `ThreadPoolExecutor`
- **Extended thinking budget** — only enabled for contradiction detection and synthesis, keeping costs optimal

---

## 👥 Team

**Team Debug Thugs** — Amazon Nova AI Hackathon 2026

| | Name | Contribution |
|-|------|-------------|
| 👨‍💻 | **Gaurav Kumar Nayak** | Team Lead · Backend · Nova Act integration · Orchestrator |
| 👨‍💻 | **Mohit Paul** | Frontend · Nova Embeddings · Synthesis pipeline · UI |

CSE (Data Science), 2nd Year · C.V. Raman Global University, Bhubaneswar
📧 gauravnayak711@gmail.com

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ for the **Amazon Nova AI Hackathon 2026**

`#AmazonNova` &nbsp;·&nbsp; `#AgenticAI` &nbsp;·&nbsp; `#AWSBedrock` &nbsp;·&nbsp; `#TeamDebugThugs`

</div>
