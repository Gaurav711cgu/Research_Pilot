"""
Document Reader Agent — powered by Amazon Nova 2 Pro (Multimodal).
Reads PDFs, images, charts, tables and extracts structured information.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import base64
import io
from typing import List, Optional
from pathlib import Path
from tools.bedrock_client import BedrockClient


SYSTEM_PROMPT = """You are a meticulous research assistant specializing in 
document analysis. Your job is to extract key information from documents including:
- Main claims and findings
- Methodologies used  
- Data, statistics, and numbers
- Conclusions and limitations
- Charts, tables, and visual data
Always be precise and cite specific sections when possible."""


class DocumentChunk:
    def __init__(self, text: str, page: int, chunk_type: str = "text"):
        self.text = text
        self.page = page
        self.chunk_type = chunk_type  # "text", "table", "chart", "image"


class DocReaderAgent:
    """
    Amazon Nova 2 Pro-powered document reader.
    Handles: PDFs, images (charts/tables), plain text files.
    Uses multimodal capabilities to understand visual content.
    """

    def __init__(self):
        self.bedrock = BedrockClient()

    def read_pdf(self, pdf_path: str, query: str) -> dict:
        """
        Read a PDF file and extract relevant information for the query.
        Uses PyPDF2 for text extraction + Nova Pro for understanding.
        """
        try:
            import PyPDF2
        except ImportError:
            return {"error": "PyPDF2 not installed", "text": "", "insights": ""}

        text_chunks = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)
            for i, page in enumerate(reader.pages[:50]):  # Limit to 50 pages
                text = page.extract_text()
                if text.strip():
                    text_chunks.append(DocumentChunk(text, i + 1, "text"))

        combined_text = "\n\n".join(
            f"[Page {c.page}]\n{c.text[:800]}" for c in text_chunks[:10]
        )

        insights = self.bedrock.invoke_nova_pro(
            prompt=f"""Analyze this document for the research query: "{query}"

DOCUMENT CONTENT:
{combined_text}

Extract:
1. Key findings relevant to the query
2. Important statistics or data points
3. Author conclusions
4. Limitations or caveats
5. Relevance score (1-10) for the query

Format as structured markdown.""",
            system_prompt=SYSTEM_PROMPT,
            extended_thinking=True,
            max_tokens=2048,
        )

        return {
            "source": pdf_path,
            "pages": total_pages,
            "text": combined_text[:2000],
            "insights": insights,
            "source_type": "pdf"
        }

    def read_image(self, image_path: str, query: str) -> dict:
        """
        Read and analyze an image (chart, figure, table) using Nova Pro's
        multimodal capabilities.
        """
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # Determine mime type
        suffix = Path(image_path).suffix.lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".png": "image/png", ".gif": "image/gif",
                    ".webp": "image/webp"}
        mime_type = mime_map.get(suffix, "image/png")

        insights = self.bedrock.invoke_nova_pro(
            prompt=f"""Analyze this image/figure for the research query: "{query}"

Please:
1. Describe what this image/chart/table shows
2. Extract all numerical data visible
3. Identify trends or patterns
4. Explain relevance to the research query
5. Note any important labels or legends""",
            system_prompt=SYSTEM_PROMPT,
            image_base64=image_b64,
            image_mime=mime_type,
            max_tokens=1024,
        )

        return {
            "source": image_path,
            "type": "image",
            "insights": insights,
            "source_type": "image"
        }

    def read_text(self, text: str, source_url: str, query: str) -> dict:
        """
        Analyze plain text content (web page text, scraped content).
        Uses Nova Pro for deep understanding with extended thinking.
        """
        # Truncate if too long
        truncated = text[:4000] if len(text) > 4000 else text

        insights = self.bedrock.invoke_nova_pro(
            prompt=f"""Analyze this text for the research query: "{query}"

SOURCE: {source_url}
TEXT:
{truncated}

Extract:
1. Key claims relevant to the query
2. Evidence or data provided
3. Author perspective or bias
4. Publication recency signals
5. Credibility assessment (1-10)
6. Direct quotes useful for the report

Format as structured markdown.""",
            system_prompt=SYSTEM_PROMPT,
            extended_thinking=False,
            max_tokens=1500,
        )

        return {
            "source": source_url,
            "text": truncated,
            "insights": insights,
            "source_type": "web"
        }

    def extract_contradictions(self, analyses: List[dict], query: str) -> str:
        """
        Use Nova Pro extended thinking to identify contradictions
        across multiple sources — a unique ResearchPilot capability.
        """
        sources_text = "\n\n---\n\n".join(
            f"SOURCE {i+1}: {a.get('source', '')}\n{a.get('insights', '')}"
            for i, a in enumerate(analyses[:6])
        )

        return self.bedrock.invoke_nova_pro(
            prompt=f"""Analyze these {len(analyses)} research sources about "{query}".

SOURCES:
{sources_text}

Identify:
1. Points of agreement across sources
2. Contradictions or conflicting findings (flag these clearly with ⚠️)
3. Gaps in evidence
4. Consensus vs. emerging/minority views
5. Time evolution of understanding (has thinking changed?)

Be specific. Quote sources. Flag contradictions prominently.""",
            system_prompt="You are an expert meta-analyst skilled at synthesizing contradictory research.",
            extended_thinking=True,
            max_tokens=3000,
        )
