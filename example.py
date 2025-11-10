"""Example usage of Perplexity Agent."""

from perplexity_agent import PerplexityAgent


def main() -> None:
    """Example usage of Perplexity Agent."""
    # Initialize the agent
    # API key will be read from environment variable PERPLEXITY_API_KEY
    # or you can pass it directly: agent = PerplexityAgent(api_key="your-key")
    agent = PerplexityAgent()

    # Example 1: Simple question
    print("=" * 60)
    print("Example 1: Simple question")
    print("=" * 60)
    question = "What is the capital of France?"
    answer = agent.ask(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")

    # Example 2: Get full response
    print("=" * 60)
    print("Example 2: Get full response")
    print("=" * 60)
    question = "Explain quantum computing in simple terms"
    full_response = agent.get_full_response(question)
    print(f"Question: {question}")
    print(f"Full Response Keys: {list(full_response.keys())}")
    if "choices" in full_response and len(full_response["choices"]) > 0:
        print(f"Answer: {full_response['choices'][0]['message']['content']}\n")

    # Example 3: Custom chat with multiple messages
    print("=" * 60)
    print("Example 3: Custom chat with multiple messages")
    print("=" * 60)
    messages = [
        {"role": "user", "content": "What is Python?"},
        {
            "role": "assistant",
            "content": "Python is a high-level programming language known for its simplicity.",
        },
        {"role": "user", "content": "What are its main features?"},
    ]
    response = agent.chat(messages=messages)
    if "choices" in response and len(response["choices"]) > 0:
        print(f"Answer: {response['choices'][0]['message']['content']}\n")

    # Example 4: Custom parameters
    print("=" * 60)
    print("Example 4: Custom parameters")
    print("=" * 60)
    question = "Write a short poem about AI"
    answer = agent.ask(
        question=question,
        model="sonar-reasoning",
        temperature=0.7,  # Higher temperature for more creative responses
        max_tokens=200,
    )
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")


if __name__ == "__main__":
    main()

