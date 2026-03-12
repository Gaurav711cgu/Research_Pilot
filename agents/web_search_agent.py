"""
Web Search Agent — powered by Amazon Nova Act.
Autonomously browses Google Scholar, arXiv, Wikipedia, news sites.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import json
from typing import List, Optional
from pydantic import BaseModel
from src.config import CONFIG


class SearchResult(BaseModel):
    title: str
    url: str
    text: str
    source_type: str   # "academic", "news", "wiki", "web"
    year: Optional[str] = None
    authors: Optional[str] = None
    citations: Optional[int] = None


class WebSearchAgent:
    """
    Nova Act-powered agent that autonomously browses the web to gather
    research sources. Uses natural language instructions + Python control flow.
    """

    def __init__(self):
        self.api_key = CONFIG.nova_act_api_key
        self.results: List[SearchResult] = []

    def search(self, query: str, num_sources: int = 8) -> List[SearchResult]:
        """
        Run a complete web research cycle for the given query.
        Searches multiple source types in parallel.
        """
        print(f"[WebSearchAgent] Searching: {query}")

        # Try Nova Act if API key available, else fallback to requests
        if self.api_key:
            return self._nova_act_search(query, num_sources)
        else:
            return self._requests_fallback_search(query, num_sources)

    def _nova_act_search(self, query: str, num_sources: int) -> List[SearchResult]:
        """
        Full Nova Act browser-based research workflow.
        Navigates to multiple sources and extracts structured data.
        """
        try:
            from nova_act import NovaAct
        except ImportError:
            print("[WebSearchAgent] nova-act not installed, using fallback")
            return self._requests_fallback_search(query, num_sources)

        results = []

        # ── Search Google Scholar for academic papers ──
        with NovaAct(
            starting_page="https://scholar.google.com",
            api_key=self.api_key,
            headless=True,
        ) as agent:
            agent.act(f'Search for "{query}" in the search box and press Enter')
            agent.act("Wait for results to load")

            # Extract up to 5 results
            for i in range(min(5, num_sources // 2)):
                try:
                    raw = agent.act(
                        f"Extract the title, authors, year, and snippet of result {i+1}. "
                        "Return as JSON with keys: title, authors, year, snippet, link",
                        schema=SearchResult.model_json_schema()
                    )
                    data = json.loads(raw.response.parsed_response)
                    results.append(SearchResult(
                        title=data.get("title", "Unknown"),
                        url=data.get("link", ""),
                        text=data.get("snippet", ""),
                        source_type="academic",
                        year=data.get("year"),
                        authors=data.get("authors"),
                    ))
                except Exception:
                    continue

        # ── Search Wikipedia for background context ──
        wiki_query = query.replace(" ", "_")
        with NovaAct(
            starting_page=f"https://en.wikipedia.org/wiki/Special:Search?search={wiki_query}",
            api_key=self.api_key,
            headless=True,
        ) as agent:
            agent.act("Click on the first search result")
            agent.act("Wait for the article to load")
            try:
                raw = agent.act(
                    "Extract the first 3 paragraphs of the main article text. "
                    "Return as JSON with keys: title, text, url",
                )
                data = json.loads(raw.response.parsed_response)
                results.append(SearchResult(
                    title=data.get("title", "Wikipedia"),
                    url=data.get("url", ""),
                    text=data.get("text", ""),
                    source_type="wiki",
                ))
            except Exception:
                pass

        # ── Search news for recent developments ──
        with NovaAct(
            starting_page=f"https://news.google.com/search?q={query.replace(' ', '+')}",
            api_key=self.api_key,
            headless=True,
        ) as agent:
            agent.act("Wait for news articles to load")
            for i in range(min(3, num_sources - len(results))):
                try:
                    raw = agent.act(
                        f"Extract the title, source, date, and first paragraph of news article {i+1}. "
                        "Return as JSON with keys: title, source, date, text, url",
                    )
                    data = json.loads(raw.response.parsed_response)
                    results.append(SearchResult(
                        title=data.get("title", "News"),
                        url=data.get("url", ""),
                        text=data.get("text", ""),
                        source_type="news",
                        year=data.get("date", "")[:4] if data.get("date") else None,
                    ))
                except Exception:
                    continue

        self.results = results[:num_sources]
        print(f"[WebSearchAgent] Found {len(self.results)} sources via Nova Act")
        return self.results

    def _requests_fallback_search(self, query: str, num_sources: int) -> List[SearchResult]:
        """
        Fallback search using requests + BeautifulSoup when Nova Act
        API key is not configured. Uses Wikipedia & arXiv APIs.
        """
        import requests
        from bs4 import BeautifulSoup

        results = []

        # Wikipedia API
        try:
            resp = requests.get(
                "https://en.wikipedia.org/api/rest_v1/page/summary/" +
                query.replace(" ", "_"),
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                results.append(SearchResult(
                    title=data.get("title", "Wikipedia"),
                    url=data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    text=data.get("extract", ""),
                    source_type="wiki",
                ))
        except Exception:
            pass

        # arXiv API for academic papers
        try:
            arxiv_query = query.replace(" ", "+")
            resp = requests.get(
                f"http://export.arxiv.org/api/query?search_query=all:{arxiv_query}&max_results=5",
                timeout=8
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "xml")
                for entry in soup.find_all("entry")[:5]:
                    title = entry.find("title").text.strip() if entry.find("title") else ""
                    summary = entry.find("summary").text.strip() if entry.find("summary") else ""
                    url = entry.find("id").text.strip() if entry.find("id") else ""
                    authors_list = [a.find("name").text for a in entry.find_all("author")[:3]]
                    published = entry.find("published").text[:4] if entry.find("published") else ""
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        text=summary[:500],
                        source_type="academic",
                        year=published,
                        authors=", ".join(authors_list),
                    ))
        except Exception:
            pass

        self.results = results[:num_sources]
        print(f"[WebSearchAgent] Found {len(self.results)} sources via fallback")
        return self.results
