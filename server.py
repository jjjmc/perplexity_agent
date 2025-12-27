"""
Perplexity Agent: A Minimal Composable Part (MCP) for Perplexity AI Search.
This file contains the MCP server implementation for Perplexity search capabilities.

APIs Provided:
1. perplexity_search: Search using Perplexity AI with a simple question.
2. perplexity_chat: Multi-turn conversation with Perplexity AI.
3. perplexity_search_full: Get full response with metadata from Perplexity AI.
"""
import logging
import os
from typing import List, Dict, Optional, Any
from pathlib import Path
import uuid

from perplexity_agent.agent import PerplexityAgent

### New MCP
from mcp.server.fastmcp import FastMCP

## Configuration
LOG_ENABLE = False

AGENT_ID = "jjjmc/perplexity_agent"
AGENT_NAME = "A2Z Perplexity Agent"

ROOT_DIR = Path(__file__).parent

# Initialize Perplexity Agent
print(f"Initializing Perplexity Agent...")
logging.info(f"Initializing Perplexity Agent")

try:
    # Get API key from environment variable, with default fallback
    # API key removed - use PERPLEXITY_API_KEY environment variable
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError(
            "PERPLEXITY_API_KEY environment variable is required. "
            "Please set it using: export PERPLEXITY_API_KEY=your_api_key_here"
        )
    agent = PerplexityAgent(api_key=api_key)
    print("--- Perplexity Agent Initialized Successfully ---")
except Exception as e:
    print(f"Failed to initialize Perplexity Agent: {e}")
    raise

# Create an MCP server
mcp = FastMCP(AGENT_NAME, json_response=True)

# Supported models list
SUPPORTED_MODELS = [
    "sonar-reasoning",
    "sonar",
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-huge-128k-online",
]


def generate_user_id() -> str:
    """Generate a temporary user ID."""
    return f"TEMP_{str(uuid.uuid4())[:8]}"


@mcp.tool()
def perplexity_search(
    question: str,
    model: str = "sonar-reasoning",
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict:
    """
    Search and get an answer using Perplexity AI. This is the simplest way to get answers to questions.

    Args:
        question: REQUIRED. The question or query to search for. This can be any question you want to ask.
        model: The Perplexity model to use. Defaults to "sonar-reasoning". 
               Supported models: sonar-reasoning, sonar, llama-3.1-sonar-small-128k-online, 
               llama-3.1-sonar-large-128k-online, llama-3.1-sonar-huge-128k-online.
        temperature: Sampling temperature (0.0 to 1.0). Lower values make output more deterministic. 
                     Defaults to 0.2.
        max_tokens: Optional. Maximum number of tokens to generate. If not specified, model uses default.

    Returns:
        A dictionary containing:
        - 'answer': The text answer from Perplexity AI
        - 'model': The model used
        - 'question': The original question
        - 'message': Status message
    """
    answer = ""
    message = "Success"

    if not question or not question.strip():
        return {
            "answer": "",
            "model": model,
            "question": question,
            "message": "Error: Question cannot be empty.",
        }

    if model not in SUPPORTED_MODELS:
        return {
            "answer": "",
            "model": model,
            "question": question,
            "message": f"Error: Model '{model}' not supported. Supported models: {', '.join(SUPPORTED_MODELS)}",
        }

    try:
        answer = agent.ask(
            question=question,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        message = f"Successfully retrieved answer for question: {question[:50]}..."
    except Exception as e:
        print(f"Failed to search with Perplexity: {e}")
        message = f"Failed to get answer: {str(e)}"
        answer = ""

    return {
        "answer": answer,
        "model": model,
        "question": question,
        "message": message,
    }


@mcp.tool()
def perplexity_chat(
    messages: List[Dict[str, str]],
    model: str = "sonar-reasoning",
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict:
    """
    Conduct a multi-turn conversation with Perplexity AI. Useful for follow-up questions and context-aware discussions.

    Args:
        messages: REQUIRED. List of message dictionaries with 'role' and 'content' keys.
                 Example: [
                     {"role": "user", "content": "What is Python?"},
                     {"role": "assistant", "content": "Python is a programming language."},
                     {"role": "user", "content": "What are its main features?"}
                 ]
        model: The Perplexity model to use. Defaults to "sonar-reasoning".
        temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.
        max_tokens: Optional. Maximum number of tokens to generate.

    Returns:
        A dictionary containing:
        - 'response': The full API response from Perplexity
        - 'answer': The text content of the assistant's response (extracted from response)
        - 'model': The model used
        - 'message': Status message
    """
    response: Dict[str, Any] = {}
    answer = ""
    message = "Success"

    if not messages or not isinstance(messages, list):
        return {
            "response": {},
            "answer": "",
            "model": model,
            "message": "Error: Messages must be a non-empty list of message dictionaries.",
        }

    if model not in SUPPORTED_MODELS:
        return {
            "response": {},
            "answer": "",
            "model": model,
            "message": f"Error: Model '{model}' not supported. Supported models: {', '.join(SUPPORTED_MODELS)}",
        }

    try:
        response = agent.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Extract answer from response
        try:
            answer = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except (KeyError, IndexError):
            answer = ""

        message = f"Successfully completed chat conversation with {len(messages)} messages."
    except Exception as e:
        print(f"Failed to chat with Perplexity: {e}")
        message = f"Failed to complete chat: {str(e)}"
        response = {}

    return {
        "response": response,
        "answer": answer,
        "model": model,
        "message": message,
    }


@mcp.tool()
def perplexity_search_full(
    question: str,
    model: str = "sonar-reasoning",
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict:
    """
    Search using Perplexity AI and get the full response with metadata, citations, and other details.
    Use this when you need complete information including sources, citations, or metadata.

    Args:
        question: REQUIRED. The question or query to search for.
        model: The Perplexity model to use. Defaults to "sonar-reasoning".
        temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.
        max_tokens: Optional. Maximum number of tokens to generate.

    Returns:
        A dictionary containing:
        - 'response': The complete API response with all metadata
        - 'answer': The text content (extracted from response)
        - 'model': The model used
        - 'question': The original question
        - 'message': Status message
    """
    response: Dict[str, Any] = {}
    answer = ""
    message = "Success"

    if not question or not question.strip():
        return {
            "response": {},
            "answer": "",
            "model": model,
            "question": question,
            "message": "Error: Question cannot be empty.",
        }

    if model not in SUPPORTED_MODELS:
        return {
            "response": {},
            "answer": "",
            "model": model,
            "question": question,
            "message": f"Error: Model '{model}' not supported. Supported models: {', '.join(SUPPORTED_MODELS)}",
        }

    try:
        response = agent.get_full_response(
            question=question,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Extract answer from response
        try:
            answer = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except (KeyError, IndexError):
            answer = ""

        message = f"Successfully retrieved full response for question: {question[:50]}..."
    except Exception as e:
        print(f"Failed to get full response from Perplexity: {e}")
        message = f"Failed to get full response: {str(e)}"
        response = {}

    return {
        "response": response,
        "answer": answer,
        "model": model,
        "question": question,
        "message": message,
    }


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Hello, I am Agent A2Z Perplexity Agent, who can help you search the web and answer questions using Perplexity AI. You can ask me any question like 'What is the latest news about AI?', 'Explain quantum computing', 'What are the best practices for Python?', etc. I can search the internet in real-time and provide you with accurate, up-to-date information.",
        "formal": "I am the A2Z Perplexity Agent, a web search assistant powered by Perplexity AI. I can help you find information, answer questions, and conduct research on any topic.",
        "casual": "Hey! I'm the Perplexity Agent. Ask me anything and I'll search the web for you!",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    # STARTUP: Initialize Perplexity Agent
    print("--- APPLICATION STARTUP ---")
    # Agent is already initialized at module level
    # If needed, we can add async initialization here

    async with mcp.session_manager.run():
        yield

    # SHUTDOWN: Cleanup
    print("--- APPLICATION SHUTDOWN ---")
    # PerplexityAgent doesn't require explicit cleanup


async def get_mcp_root_id_handler(request):
    """
    This function handles the GET request to the root of the MCP application (i.e., /mcp).
    """
    unique_id = AGENT_ID
    return JSONResponse({"id": AGENT_ID})


# --- Starlette Route Function (for the main / route) ---
async def starlette_root_id_endpoint(request):
    """
    Starlette endpoint to serve the root path of the main application: http://<server>:7004/
    """
    unique_id = str(uuid.uuid4())[:8]
    return JSONResponse({"app_root_id": unique_id})


## Route: single endpoint, Mount: /xxx all the subsequent urls
## mcp_app 里面定义了前缀 /mcp

mcp_app = mcp.streamable_http_app()
mcp_app.routes.insert(
    0, Route("/mcp", get_mcp_root_id_handler, methods=["GET"])
)

## GET /mcp : 1. Mount("/", app=mcp_app) -> 2. mcp_app.Route, e.g. http://0.0.0.0:7004/
## POST /mcp : 1. Mount("/", app=mcp_app) -> 3. mcp_app里面 /json_rpc handler

# Mount using Host-based routing
app = Starlette(
    routes=[
        Mount("/", app=mcp_app),
    ],
    lifespan=lifespan,
)

# Define the argument parser
def parse_args():
    """Parses command line arguments for the server port."""
    import argparse

    parser = argparse.ArgumentParser(description="Run the A2Z Perplexity Agent MCP Server.")
    parser.add_argument(
        "--port",
        type=int,
        default=7004,  # Set a default port (different from bill agent's 7003)
        help="The port number on which to run the server (e.g., 7004).",
    )
    return parser.parse_args()


# Run with streamable HTTP transport
if __name__ == "__main__":
    """
    Uvicorn Run通过 环境变量: MCP_SERVER_URL, 把内部在哪个端口运营跑起来，内部还会应用转发一次
    Starlette: 把 mcp 绑定到 / 上
    """

    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7004)
    args = parser.parse_args()

    print(f"Starting MCP server on port {args.port}")
    os.environ["MCP_SERVER_URL"] = f"http://0.0.0.0:{args.port}/mcp"
    mcp.run("streamable-http")

