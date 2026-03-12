"""
ResearchPilot Demo Runner
Demonstrates the full pipeline with mock data — no API keys needed.
Shows judges exactly what the system does end-to-end.
Amazon Nova AI Hackathon 2026 | Team Debug Thugs
"""
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn


DEMO_QUERY = "Latest advances in solid-state batteries for electric vehicles"

MOCK_SOURCES = [
    {"title": "Solid-State Batteries: Progress and Prospects", "url": "https://arxiv.org/abs/2312.12345",
     "source_type": "academic", "year": "2024", "authors": "Kim et al."},
    {"title": "Toyota's All-Solid-State EV Battery Breakthrough", "url": "https://reuters.com/technology/toyota",
     "source_type": "news", "year": "2024"},
    {"title": "Solid-state battery — Wikipedia", "url": "https://en.wikipedia.org/wiki/Solid-state_battery",
     "source_type": "wiki"},
    {"title": "Electrolyte Challenges in Solid-State Li-Ion Cells", "url": "https://nature.com/articles/energy2024",
     "source_type": "academic", "year": "2023", "authors": "Zhang et al."},
    {"title": "Quantumscape 2024 Production Update", "url": "https://quantumscape.com/news/2024",
     "source_type": "web", "year": "2024"},
    {"title": "CATL Condensed Battery: Semi-Solid Innovation", "url": "https://catl.com/news/condensed",
     "source_type": "news", "year": "2024"},
]

MOCK_REPORT = """## Executive Summary
Solid-state batteries (SSBs) represent the next frontier in EV energy storage, 
offering theoretical energy densities 2-3× higher than conventional lithium-ion cells 
with significantly improved safety profiles. As of 2024, several companies are reaching 
pilot production, though mass commercialization faces persistent materials science challenges.

## Key Findings
- **Energy density:** Prototype SSBs achieve 400-500 Wh/kg vs. ~250 Wh/kg for Li-ion [Source 1]
- **Toyota timeline:** Targeting 2027-2028 for initial solid-state EV production [Source 2]  
- **Main bottleneck:** Solid electrolyte ionic conductivity at room temperature remains 2-5× below liquid electrolytes [Source 4]
- **QuantumScape milestone:** Achieved 800+ charge cycles at >80% capacity retention in 2024 [Source 5]
- **CATL semi-solid:** Condensed battery bridges gap with 500 Wh/kg, entering production 2025 [Source 6]

## Detailed Analysis

### Current State of Knowledge
Solid-state batteries replace liquid electrolytes with solid alternatives — oxides (LLZO), 
sulfides (LGPS), or polymers. Each trades off ionic conductivity vs. manufacturability vs. 
electrochemical stability. Sulfide electrolytes offer the best conductivity but react 
violently with moisture, complicating manufacturing.

### Recent Developments (2023-2024)
Multiple companies reached inflection points: QuantumScape demonstrated automotive-grade 
cycle life; Toyota opened a solid-state battery pilot line; CATL's semi-solid condensed 
battery entered commercial production, proving partial transitions are commercially viable.

### ⚠️ Contradictions & Debates
**Disagreement on timeline:** Toyota states 2027 production [Source 2] while independent 
analysts at BloombergNEF estimate 2030+ for meaningful volume [Source 3].  
**Electrolyte choice:** Academic consensus favors oxide ceramics for stability, but 
industry leaders (Samsung SDI, Solid Power) are pursuing sulfide routes for conductivity.

### Knowledge Gaps
- Long-term degradation mechanisms at solid-solid interfaces remain poorly understood
- Scalable, cost-competitive manufacturing processes have not been demonstrated at GWh scale

## Practical Implications
Investors should note the 3-7 year commercialization gap. Semi-solid batteries (CATL, 
BYD) offer near-term density improvements while true SSBs mature. OEMs planning post-2028 
platforms can design for SSB integration.

## Confidence Assessment
| Finding | Confidence |
|---------|-----------|
| Energy density advantage | 🟢 High (multiple peer-reviewed sources) |
| Toyota 2027 timeline | 🟡 Medium (company statements, analyst skepticism) |
| Manufacturing cost parity | 🔴 Low (speculative, no public data) |
"""

MOCK_VOICE_SUMMARY = (
    "Solid-state batteries show great promise for electric vehicles, with prototypes achieving "
    "twice the energy density of current lithium-ion cells. Toyota and QuantumScape are closest "
    "to production, targeting 2027 to 2028. The main challenge remains manufacturing at scale, "
    "with experts divided on whether mass commercialization will arrive before 2030."
)


def run_demo_pipeline():
    """Simulate the full ResearchPilot pipeline with rich terminal output."""
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]ResearchPilot[/bold cyan] [white]— Amazon Nova AI Hackathon Demo[/white]\n"
        "[dim]Powered by Nova 2 Pro · Nova 2 Lite · Nova 2 Sonic · Nova Act · Nova Embeddings[/dim]",
        border_style="cyan"
    ))

    console.print(f"\n[bold]Query:[/bold] {DEMO_QUERY}\n")

    steps = [
        ("📋 Nova 2 Lite: Planning research strategy", 0.8),
        ("🌐 Nova Act: Browsing Google Scholar", 1.2),
        ("🌐 Nova Act: Browsing arXiv.org", 1.0),
        ("🌐 Nova Act: Scraping Google News", 0.9),
        ("🌐 Nova Act: Extracting Wikipedia context", 0.6),
        ("📄 Nova 2 Pro: Analyzing academic paper [Source 1]", 1.1),
        ("📄 Nova 2 Pro: Analyzing academic paper [Source 4]", 1.1),
        ("📊 Nova 2 Pro: Reading chart in Source 1 (multimodal)", 0.8),
        ("🔍 Nova Embeddings: Generating semantic vectors", 0.7),
        ("🔍 Nova Embeddings: FAISS reranking by relevance", 0.5),
        ("🔎 Nova 2 Pro: Contradiction detection (extended thinking)", 1.5),
        ("🧠 Nova 2 Pro: Synthesizing report (extended thinking)", 2.0),
        ("📝 Nova 2 Lite: Generating executive summary", 0.6),
        ("🔊 Nova 2 Sonic: Generating voice summary (TTS)", 0.8),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}[/cyan]"),
        BarColumn(),
        TextColumn("[bold]{task.percentage:.0f}%[/bold]"),
        console=console,
    ) as progress:
        task = progress.add_task("ResearchPilot Pipeline", total=len(steps))
        for description, delay in steps:
            progress.update(task, description=description, advance=1)
            time.sleep(delay)

    # Sources table
    console.print("\n[bold cyan]📚 Sources Found (Nova Act + Embeddings)[/bold cyan]")
    table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("#", width=3)
    table.add_column("Title", max_width=42)
    table.add_column("Type", width=10)
    table.add_column("Year", width=6)
    table.add_column("Relevance", width=10)

    relevance_scores = [0.96, 0.91, 0.84, 0.88, 0.79, 0.82]
    for i, src in enumerate(MOCK_SOURCES):
        score = relevance_scores[i]
        score_str = f"{'🟢' if score>0.85 else '🟡'} {score:.2f}"
        table.add_row(
            str(i+1), src["title"][:42], src["source_type"],
            src.get("year", "—"), score_str
        )
    console.print(table)

    # Research plan output
    plan = {
        "main_query": "Solid-state battery technology advances for EV applications",
        "sub_queries": [
            "Current solid-state battery energy density benchmarks 2024",
            "Commercial production timeline solid-state batteries Toyota QuantumScape",
            "Solid electrolyte ionic conductivity challenges",
        ],
        "estimated_complexity": "high",
    }
    console.print(f"\n[bold cyan]📋 Research Plan (Nova 2 Lite)[/bold cyan]")
    console.print(f"  [dim]Complexity:[/dim] {plan['estimated_complexity']}")
    for q in plan["sub_queries"]:
        console.print(f"  • {q}")

    # Contradiction highlight
    console.print("\n[bold yellow]⚠️  Contradictions Detected (Nova 2 Pro Extended Thinking)[/bold yellow]")
    console.print("  • Toyota timeline: Company says 2027, BloombergNEF says 2030+")
    console.print("  • Electrolyte choice: Academia favors oxides, industry uses sulfides")

    # Final report
    console.print("\n[bold green]📄 Synthesized Report (Nova 2 Pro)[/bold green]")
    console.print(Markdown(MOCK_REPORT[:1200] + "\n\n*[...full report saved to file...]*"))

    # Voice summary box
    console.print(Panel(
        f"[bold]🔊 Nova 2 Sonic Voice Summary:[/bold]\n\n{MOCK_VOICE_SUMMARY}",
        border_style="green"
    ))

    # Final stats
    console.print("\n[bold]━━━━━ Pipeline Complete ━━━━━[/bold]")
    stats_table = Table(show_header=False, border_style="dim")
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Value", style="cyan")
    stats_table.add_row("Sources analyzed", "6")
    stats_table.add_row("Nova models used", "5 (Pro, Lite, Sonic, Act, Embeddings)")
    stats_table.add_row("Confidence score", "🟢 84%")
    stats_table.add_row("Contradictions found", "2")
    stats_table.add_row("Human review needed", "No ✅")
    stats_table.add_row("Report length", "~2,400 words")
    stats_table.add_row("Total pipeline time", "~4 minutes")
    console.print(stats_table)

    console.print(Panel(
        "[bold cyan]ResearchPilot[/bold cyan] — Built by [bold]Debug Thugs[/bold]\n"
        "Gaurav Kumar Nayak & Mohit Paul | CVR Global University\n"
        "[dim]Amazon Nova AI Hackathon 2026[/dim]",
        border_style="cyan"
    ))


if __name__ == "__main__":
    run_demo_pipeline()
