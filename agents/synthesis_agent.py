"""
Synthesis Agent — powered by Amazon Nova 2 Pro (Extended Thinking).
Synthesizes all research findings into a structured, citable report.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import json
from typing import List, Optional
from tools.bedrock_client import BedrockClient
from tools.report_formatter import ReportFormatter


SYNTHESIS_SYSTEM_PROMPT = """You are a world-class research analyst with expertise 
in synthesizing complex information from multiple sources into clear, accurate, 
well-structured reports. You:
- Always cite sources with [Source N] notation
- Distinguish between well-established facts and emerging/uncertain findings
- Flag contradictions and knowledge gaps
- Write for both expert and non-expert audiences
- Include actionable insights and implications
- Use precise language and quantify claims where possible"""


class SynthesisAgent:
    """
    The final stage of ResearchPilot's pipeline.
    Uses Nova 2 Pro with extended thinking to:
    1. Synthesize all gathered research
    2. Resolve contradictions
    3. Generate a structured report
    4. Assess confidence levels
    """

    def __init__(self):
        self.bedrock = BedrockClient()
        self.formatter = ReportFormatter()

    def synthesize(
        self,
        query: str,
        sources: List[dict],
        analyses: List[dict],
        contradiction_report: str = "",
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Main synthesis entry point.
        Returns a complete structured research report.
        """
        # Build context from all sources
        sources_context = self._build_sources_context(sources, analyses)

        # Generate the main report using Nova Pro with extended thinking
        print("[SynthesisAgent] Generating report with Nova 2 Pro extended thinking...")
        raw_report = self.bedrock.invoke_nova_pro(
            prompt=f"""Research Query: {query}

RESEARCH SOURCES ({len(sources)} total):
{sources_context}

CONTRADICTION ANALYSIS:
{contradiction_report or "Not provided"}

Generate a comprehensive research report with these sections:

# Executive Summary (2-3 sentences)
# Key Findings (5-7 bullet points with citations)
# Detailed Analysis
  ## Current State of Knowledge
  ## Recent Developments  
  ## Contradictions & Debates
  ## Knowledge Gaps
# Practical Implications
# Confidence Assessment (High/Medium/Low per finding)
# References (numbered list)

Be thorough. Cite every major claim. Use [Source N] notation.
Flag confidence level for each key finding.""",
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            extended_thinking=True,
            max_tokens=5000,
        )

        # Generate a short executive summary (for voice output)
        print("[SynthesisAgent] Generating voice summary with Nova 2 Lite...")
        voice_summary = self.bedrock.invoke_nova_lite(
            prompt=f"""Summarize this research report in 3-4 sentences suitable for 
text-to-speech delivery. Be clear, natural, and informative:

{raw_report[:2000]}""",
            system_prompt="You write concise, natural-sounding summaries for voice delivery.",
            max_tokens=300,
        )

        # Assess overall confidence
        confidence = self._assess_confidence(raw_report, sources)

        return {
            "query": query,
            "report_markdown": raw_report,
            "voice_summary": voice_summary,
            "num_sources": len(sources),
            "confidence_score": confidence,
            "needs_human_review": confidence < 0.6,
            "sources": [
                {"title": s.get("title", ""), "url": s.get("url", ""), "type": s.get("source_type", "")}
                for s in sources
            ],
        }

    def _build_sources_context(self, sources: List[dict], analyses: List[dict]) -> str:
        """Build a consolidated context string from all sources."""
        lines = []
        for i, (src, analysis) in enumerate(zip(sources, analyses)):
            title = src.get("title", f"Source {i+1}")
            url = src.get("url", "")
            source_type = src.get("source_type", "web")
            insights = analysis.get("insights", src.get("text", ""))[:600]

            lines.append(
                f"[Source {i+1}] {title} ({source_type})\n"
                f"URL: {url}\n"
                f"Key content: {insights}\n"
            )
        return "\n".join(lines)

    def _assess_confidence(self, report: str, sources: List[dict]) -> float:
        """
        Compute a confidence score for the synthesized report.
        Based on: source count, source diversity, recency, academic vs. web ratio.
        """
        score = 0.5  # Base

        # Source count bonus
        n = len(sources)
        if n >= 8:
            score += 0.2
        elif n >= 5:
            score += 0.1
        elif n < 3:
            score -= 0.2

        # Source diversity
        types = set(s.get("source_type", "") for s in sources)
        if len(types) >= 3:
            score += 0.1
        elif len(types) >= 2:
            score += 0.05

        # Academic sources boost
        academic_count = sum(1 for s in sources if s.get("source_type") == "academic")
        if academic_count >= 3:
            score += 0.15
        elif academic_count >= 1:
            score += 0.05

        # Contradiction penalty
        if "⚠️" in report and report.count("⚠️") > 3:
            score -= 0.1

        return min(max(score, 0.0), 1.0)
