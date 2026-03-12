"""
ResearchPilot Orchestrator — powered by Amazon Nova 2 Pro.
The central planning agent that decomposes queries and coordinates
all sub-agents in parallel for maximum research speed.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import asyncio
import json
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from tools.bedrock_client import BedrockClient
from tools.embedding_search import EmbeddingSearch
from tools.report_formatter import ReportFormatter
from agents.web_search_agent import WebSearchAgent
from agents.doc_reader_agent import DocReaderAgent
from agents.synthesis_agent import SynthesisAgent
from agents.voice_interface import VoiceInterface
from src.config import CONFIG


ORCHESTRATOR_SYSTEM = """You are a research orchestration AI. Your job is to:
1. Understand the user's research intent
2. Decompose it into specific sub-queries
3. Identify what types of sources are most relevant
4. Plan the optimal research strategy
Always respond with valid JSON."""


class ResearchPilotOrchestrator:
    """
    The central brain of ResearchPilot.
    Powered by Amazon Nova 2 Pro for planning + reasoning.
    Coordinates: WebSearchAgent, DocReaderAgent, SynthesisAgent, VoiceInterface.
    """

    def __init__(self):
        self.bedrock = BedrockClient()
        self.search_agent = WebSearchAgent()
        self.doc_agent = DocReaderAgent()
        self.synthesis_agent = SynthesisAgent()
        self.voice = VoiceInterface()
        self.embeddings = EmbeddingSearch()
        self.formatter = ReportFormatter()
        self.executor = ThreadPoolExecutor(max_workers=CONFIG.parallel_agents)

    def plan_research(self, query: str) -> dict:
        """
        Use Nova 2 Pro to decompose the query into a research plan.
        Returns structured JSON plan with sub-queries and source types.
        """
        raw = self.bedrock.invoke_nova_lite(
            prompt=f"""Decompose this research query into an optimal research plan.

Query: "{query}"

Return ONLY valid JSON:
{{
  "main_query": "refined version of the query",
  "sub_queries": ["specific sub-question 1", "sub-question 2", "sub-question 3"],
  "source_types_needed": ["academic", "news", "wiki", "technical"],
  "key_concepts": ["concept1", "concept2"],
  "estimated_complexity": "low|medium|high",
  "search_keywords": ["keyword1", "keyword2", "keyword3"]
}}""",
            system_prompt=ORCHESTRATOR_SYSTEM,
            max_tokens=512,
        )
        try:
            # Strip markdown fences if present
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {
                "main_query": query,
                "sub_queries": [query],
                "source_types_needed": ["academic", "web"],
                "key_concepts": query.split()[:3],
                "estimated_complexity": "medium",
                "search_keywords": query.split()[:5],
            }

    def run(
        self,
        query: str,
        voice_input: bool = False,
        voice_output: bool = False,
        extra_docs: Optional[List[str]] = None,
        save_report: bool = True,
    ) -> dict:
        """
        Full ResearchPilot pipeline execution.

        Pipeline:
        1. Voice input (optional) → query
        2. Nova Pro planning → decomposed sub-queries
        3. Parallel: WebSearch (Nova Act) + DocRead (Nova Pro multimodal)
        4. Nova Embeddings → semantic reranking
        5. Nova Pro extended thinking → contradiction detection
        6. Nova Pro extended thinking → synthesis & report
        7. Nova Lite → executive summary
        8. Voice output (optional)
        """
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn
        console = Console()

        # ── Step 1: Voice Input ──────────────────────────────────
        if voice_input:
            console.print("[bold cyan]🎤 Voice input mode — speak your query...[/bold cyan]")
            query = self.voice.listen(duration_seconds=12)
            if not query:
                console.print("[red]No voice input detected. Please try again.[/red]")
                return {}

        console.print(f"\n[bold green]🔬 ResearchPilot Starting[/bold green]")
        console.print(f"[bold]Query:[/bold] {query}")
        console.rule()

        # ── Step 2: Planning ─────────────────────────────────────
        console.print("[cyan]📋 Planning research strategy...[/cyan]")
        plan = self.plan_research(query)
        console.print(f"[dim]Plan: {plan.get('estimated_complexity', 'medium')} complexity, "
                      f"{len(plan.get('sub_queries', []))} sub-queries[/dim]")

        # ── Step 3a: Web Search (Nova Act) ───────────────────────
        console.print("[cyan]🌐 Searching the web with Nova Act...[/cyan]")
        web_sources = self.search_agent.search(
            query=query,
            num_sources=CONFIG.max_web_sources,
        )

        # ── Step 3b: Analyze each source with Nova Pro ───────────
        console.print(f"[cyan]📄 Analyzing {len(web_sources)} sources with Nova 2 Pro...[/cyan]")
        analyses = []
        for src in web_sources:
            analysis = self.doc_agent.read_text(
                text=src.text,
                source_url=src.url,
                query=query,
            )
            analyses.append(analysis)

        # ── Step 3c: Extra documents (PDFs/images) ───────────────
        if extra_docs:
            console.print(f"[cyan]📎 Processing {len(extra_docs)} uploaded documents...[/cyan]")
            for doc_path in extra_docs:
                if doc_path.lower().endswith(".pdf"):
                    doc_result = self.doc_agent.read_pdf(doc_path, query)
                elif doc_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    doc_result = self.doc_agent.read_image(doc_path, query)
                else:
                    continue
                # Add to sources
                src_dict = {"title": doc_path, "url": doc_path,
                            "text": doc_result.get("text", ""), "source_type": "document"}
                web_sources_dicts = [s.__dict__ if hasattr(s, '__dict__') else s for s in web_sources]
                analyses.append(doc_result)

        # ── Step 4: Semantic Reranking (Nova Embeddings) ─────────
        console.print("[cyan]🔍 Reranking sources by relevance...[/cyan]")
        sources_dicts = [
            {"title": s.title, "url": s.url, "text": s.text,
             "source_type": s.source_type}
            for s in web_sources
        ]
        reranked = self.embeddings.rerank(query, sources_dicts)
        # Use reranked order if we got results
        if reranked:
            reranked_urls = {s["url"] for s in reranked}
            sources_final = [s for s in sources_dicts if s["url"] in reranked_urls]
            analyses_final = analyses[:len(sources_final)]
        else:
            sources_final = sources_dicts
            analyses_final = analyses

        # ── Step 5: Contradiction Detection ─────────────────────
        console.print("[cyan]🔎 Detecting contradictions across sources...[/cyan]")
        contradiction_report = self.doc_agent.extract_contradictions(
            analyses_final, query
        )

        # ── Step 6: Final Synthesis ──────────────────────────────
        console.print("[cyan]🧠 Synthesizing report with Nova 2 Pro (extended thinking)...[/cyan]")
        final_report = self.synthesis_agent.synthesize(
            query=query,
            sources=sources_final,
            analyses=analyses_final,
            contradiction_report=contradiction_report,
        )

        # ── Step 7: Human escalation check ──────────────────────
        if final_report.get("needs_human_review"):
            console.print("[bold yellow]⚠️  Confidence below threshold — flagging for human review[/bold yellow]")

        # ── Step 8: Save Report ──────────────────────────────────
        if save_report:
            safe_name = query[:30].replace(" ", "_").replace("/", "-")
            paths = self.formatter.save(final_report, f"report_{safe_name}")
            final_report["saved_files"] = paths
            console.print(f"[green]✅ Report saved: {paths}[/green]")

        # ── Step 9: Voice Output ─────────────────────────────────
        if voice_output:
            console.print("[cyan]🔊 Delivering voice summary via Nova 2 Sonic...[/cyan]")
            self.voice.speak(final_report.get("voice_summary", ""))

        console.print("\n[bold green]✅ ResearchPilot complete![/bold green]")
        console.print(f"[dim]Sources: {final_report['num_sources']} | "
                      f"Confidence: {final_report['confidence_score']:.0%}[/dim]")

        return final_report
