"""
ResearchPilot — Main Entry Point
Amazon Nova AI Hackathon 2026 | Team Debug Thugs

Usage:
  python src/main.py --query "What are advances in solid-state batteries?"
  python src/main.py --voice
  python src/main.py --demo
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import ResearchPilotOrchestrator


def parse_args():
    parser = argparse.ArgumentParser(
        description="ResearchPilot — AI Research Agent powered by Amazon Nova"
    )
    parser.add_argument("--query", "-q", type=str, help="Research query text")
    parser.add_argument("--voice", action="store_true", help="Use voice input (Nova Sonic)")
    parser.add_argument("--speak", action="store_true", help="Speak output (Nova Sonic TTS)")
    parser.add_argument("--docs", nargs="*", help="Paths to PDF/image files to analyze")
    parser.add_argument("--no-save", action="store_true", help="Don't save report to disk")
    parser.add_argument("--demo", action="store_true", help="Run with demo query (no API needed)")
    return parser.parse_args()


def run_demo():
    """Demo mode — runs with a sample query using fallback (no Nova API key needed)."""
    print("\n" + "="*60)
    print("  RESEARCHPILOT — Amazon Nova AI Hackathon Demo")
    print("="*60)
    print("\nDemo query: 'Latest advances in solid-state batteries for electric vehicles'\n")

    # Import mock for demo
    from demo_runner import run_demo_pipeline
    run_demo_pipeline()


def main():
    args = parse_args()

    if args.demo:
        run_demo()
        return

    # Validate query
    if not args.voice and not args.query:
        print("❌ Please provide a query with --query or use --voice mode")
        print("   Example: python src/main.py --query 'advances in quantum computing'")
        print("   Or:       python src/main.py --demo")
        sys.exit(1)

    # Initialize orchestrator
    orchestrator = ResearchPilotOrchestrator()

    # Run the full pipeline
    result = orchestrator.run(
        query=args.query or "",
        voice_input=args.voice,
        voice_output=args.speak,
        extra_docs=args.docs or [],
        save_report=not args.no_save,
    )

    if result:
        print("\n" + "="*60)
        print("RESEARCH COMPLETE")
        print("="*60)
        if "saved_files" in result:
            for fmt, path in result["saved_files"].items():
                print(f"  {fmt.upper()}: {path}")


if __name__ == "__main__":
    main()
