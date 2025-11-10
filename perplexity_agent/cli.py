"""Command-line interface for Perplexity Agent."""

import argparse
import sys
from typing import Optional

from perplexity_agent.agent import PerplexityAgent


def main() -> None:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Perplexity Agent - Ask questions using Perplexity AI"
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="The question to ask (if not provided, will read from stdin)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Perplexity API key (overrides environment variable)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="sonar-reasoning",
        help="Model to use (default: sonar-reasoning)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum number of tokens to generate",
    )
    parser.add_argument(
        "--full-response",
        action="store_true",
        help="Output the full API response as JSON",
    )

    args = parser.parse_args()

    # Get question from argument or stdin
    question: Optional[str] = args.question
    if not question:
        question = sys.stdin.read().strip()
        if not question:
            parser.error("No question provided. Please provide a question as an argument or via stdin.")

    try:
        # Initialize agent
        agent = PerplexityAgent(api_key=args.api_key)

        # Get response
        if args.full_response:
            response = agent.get_full_response(
                question=question,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
            import json
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            answer = agent.ask(
                question=question,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
            print(answer)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

