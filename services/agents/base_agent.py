from typing import Dict, Any, Optional, Protocol
from abc import ABC, abstractmethod
import anthropic
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ANTHROPIC_CONFIG

class AgentCallbacks(Protocol):
    def on_llm_new_token(self, token: str) -> None:
        """Called when a new token is generated."""
        pass

    def on_llm_end(self, response: str) -> None:
        """Called when LLM response generation is complete."""
        pass

    def on_llm_error(self, error: str) -> None:
        """Called when LLM encounters an error."""
        pass

class BaseStockAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.client = anthropic.Client(api_key=ANTHROPIC_CONFIG['api_key'])
        self.model = ANTHROPIC_CONFIG['model']
        self.temperature = ANTHROPIC_CONFIG['temperature']
        self.streaming = ANTHROPIC_CONFIG['streaming']
        self.max_tokens = ANTHROPIC_CONFIG['max_tokens']

    @abstractmethod
    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a request specific to this agent's expertise"""
        pass

    async def _call_claude(self, prompt: str, system_prompt: str) -> str:
        """Call Claude with the given prompt"""
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error calling Claude: {str(e)}"

    def _get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities of this agent"""
        return {}
