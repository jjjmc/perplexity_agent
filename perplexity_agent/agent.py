"""Perplexity Agent implementation."""

import os
from typing import Optional, List, Dict, Any
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PerplexityAgent:
    """Perplexity AI Agent for making chat completions."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize the Perplexity Agent.

        Args:
            api_key: Perplexity API key. If not provided, will try to get from
                     environment variable PERPLEXITY_API_KEY.
            base_url: Base URL for the API. Defaults to Perplexity chat completions endpoint.
        """
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        self.base_url = base_url or "https://api.perplexity.ai/chat/completions"

        if not self.api_key:
            raise ValueError(
                "API key is required. Please provide it as an argument "
                "or set PERPLEXITY_API_KEY environment variable."
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "sonar-reasoning",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to Perplexity API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
                     Example: [{"role": "user", "content": "Hello!"}]
            model: Model to use for completion. Defaults to llama-3.1-sonar-small-128k-online.
            temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.
            max_tokens: Maximum number of tokens to generate. Optional.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            Dictionary containing the API response.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the response contains an error.
        """
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # Add any additional parameters
        payload.update(kwargs)

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # 尝试获取错误详情
            error_detail = ""
            try:
                error_detail = f" Response: {response.text}"
            except Exception:
                pass
            raise requests.exceptions.RequestException(
                f"Failed to make request to Perplexity API: {str(e)}{error_detail}"
            ) from e
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to make request to Perplexity API: {str(e)}"
            ) from e

    def ask(
        self,
        question: str,
        model: str = "sonar-reasoning",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """
        Ask a question and get a text response.

        Args:
            question: The question to ask.
            model: Model to use for completion. Defaults to llama-3.1-sonar-small-128k-online.
            temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.
            max_tokens: Maximum number of tokens to generate. Optional.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            The text content of the assistant's response.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the response format is unexpected.
        """
        messages = [{"role": "user", "content": question}]
        response = self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise ValueError(
                f"Unexpected response format from Perplexity API: {response}"
            ) from e

    def get_full_response(
        self,
        question: str,
        model: str = "sonar-reasoning",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Ask a question and get the full API response.

        Args:
            question: The question to ask.
            model: Model to use for completion. Defaults to llama-3.1-sonar-small-128k-online.
            temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.
            max_tokens: Maximum number of tokens to generate. Optional.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            The full response dictionary from the API.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        messages = [{"role": "user", "content": question}]
        return self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

