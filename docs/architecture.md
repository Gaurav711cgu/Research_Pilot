# ResearchPilot — System Architecture

## Overview

ResearchPilot is a multi-agent research automation system built on Amazon Nova.
It uses every major Nova model in a coherent, production-grade pipeline.

## Agent Roles

### 1. Orchestrator (Nova 2 Pro)
- Parses user intent from natural language or voice
- Uses Nova 2 Lite to decompose into sub-queries and plan the research strategy
- Manages parallel agent execution via ThreadPoolExecutor
- Coordinates handoffs between all downstream agents

### 2. Web Search Agent (Nova Act)
- Autonomously browses Google Scholar, arXiv, Wikipedia, Google News
- Uses Nova Act's reliable browser automation for structured extraction
- Handles pop-ups, pagination, dynamic content automatically
- Falls back to arXiv API + Wikipedia API when Nova Act unavailable

### 3. Document Reader Agent (Nova 2 Pro Multimodal)
- Analyzes PDFs using PyPDF2 + Nova Pro text understanding
- Analyzes charts, figures, tables using Nova Pro vision capabilities
- Extracts structured insights: claims, statistics, limitations, relevance score
- Uses extended thinking mode for complex technical documents
- Performs cross-source contradiction detection

### 4. Embedding Search (Nova Multimodal Embeddings + FAISS)
- Embeds all gathered sources into semantic vector space
- Reranks sources by cosine similarity to the research query
- Filters out low-relevance sources (score < 0.3)
- Supports both text and image embeddings

### 5. Synthesis Agent (Nova 2 Pro Extended Thinking)
- Synthesizes all analyzed sources into a coherent report
- Uses extended thinking (8,000 token budget) for deep reasoning
- Generates 7-section structured report with citations
- Computes confidence scores and flags human review needs
- Uses Nova 2 Lite for fast executive summary generation

### 6. Voice Interface (Nova 2 Sonic)
- Speech-to-text: records microphone → WAV → Nova Sonic transcription
- Text-to-speech: report summary → Nova Sonic synthesis → audio playback
- Streaming TTS for low-latency sentence-by-sentence delivery

## Data Flow

```
Query (text or voice)
  → Orchestrator plans research
  → Parallel: WebSearch + DocRead (if docs uploaded)
  → Embeddings rerank sources
  → Contradiction detection
  → Synthesis → full report (markdown, HTML, JSON)
  → Voice summary (optional)
```

## Key Technical Decisions

1. **Parallel execution**: Web search and doc reading run in parallel threads
2. **Semantic reranking**: Nova Embeddings ensures only relevant sources reach synthesis
3. **Extended thinking**: Used only for contradiction detection and synthesis (cost-effective)
4. **Human-in-the-loop**: Automatic escalation when confidence < threshold
5. **Multi-format output**: Markdown, HTML, JSON all generated simultaneously
6. **Fallback architecture**: Every Nova component has a fallback for resilience

## Amazon Nova Models Used

| Model | Usage | Why This Model |
|-------|-------|---------------|
| Nova 2 Pro | Orchestration, doc analysis, contradiction detection, synthesis | Best reasoning + multimodal |
| Nova 2 Lite | Research planning, structured output, exec summary | Fast + cost-efficient |
| Nova 2 Sonic | Voice I/O | Purpose-built for speech |
| Nova Act | Browser automation for web research | Best browser agent reliability |
| Nova Multimodal Embeddings | Semantic reranking | Supports text + image modalities |
