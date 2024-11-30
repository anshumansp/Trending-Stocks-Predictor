import os
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass
from multi_agent_orchestrator import Orchestrator, AgentCallbacks, AgentOptions, AgentResponse
from stock_data_agent import StockDataAgent
from sentiment_agent import SentimentAgent
from growth_analysis_agent import GrowthAnalysisAgent
from config import ANTHROPIC_CONFIG

@dataclass
class AgentMetadata:
    agent_id: str
    agent_name: str
    user_input: str
    user_id: str
    session_id: str
    additional_params: Dict[str, Any]

class AgentResponse:
    def __init__(self, metadata: AgentMetadata, output: Any, streaming: bool = False):
        self.metadata = metadata
        self.output = output
        self.streaming = streaming

class StockAgentCallbacks(AgentCallbacks):
    def on_llm_new_token(self, token: str) -> None:
        # Handle streaming responses
        print(token, end='', flush=True)

class StockAnalysisOrchestrator:
    def __init__(self):
        # Initialize agents with callbacks and streaming
        self.stock_data_agent = StockDataAgent()
        self.sentiment_agent = SentimentAgent()
        self.growth_agent = GrowthAnalysisAgent()
        
        # Initialize the orchestrator with our agents
        self.orchestrator = Orchestrator(
            agents=[
                self.stock_data_agent,
                self.sentiment_agent,
                self.growth_agent
            ]
        )

        # Set up callbacks for streaming
        self.callbacks = StockAgentCallbacks()

    async def analyze_stock(self, symbol: str, user_id: str = 'default', session_id: Optional[str] = None) -> AgentResponse:
        """
        Perform comprehensive stock analysis using all agents with streaming support
        """
        if session_id is None:
            session_id = f"stock_analysis_{symbol}_{user_id}"

        try:
            # Create the analysis context
            context = {
                'timestamp': None,
                'symbol': symbol,
                'user_id': user_id,
                'session_id': session_id
            }

            # Create metadata for response
            metadata = AgentMetadata(
                agent_id='stock_analysis',
                agent_name='Stock Analysis Orchestrator',
                user_input=f"Analyze stock {symbol}",
                user_id=user_id,
                session_id=session_id,
                additional_params={'symbol': symbol}
            )

            # Collect data from all agents in parallel
            tasks = [
                self.stock_data_agent.process_request(
                    f"Analyze stock data for {symbol}",
                    context,
                    callbacks=self.callbacks
                ),
                self.sentiment_agent.process_request(
                    f"Analyze market sentiment for {symbol}",
                    context,
                    callbacks=self.callbacks
                ),
                self.growth_agent.process_request(
                    f"Analyze growth potential for {symbol}",
                    context,
                    callbacks=self.callbacks
                )
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Combine and structure the results
            analysis_result = {
                'symbol': symbol,
                'stock_data': results[0].get('stock_data', {}),
                'sentiment_analysis': results[1].get('sentiment_analysis', {}),
                'growth_analysis': results[2].get('growth_analysis', {}),
                'timestamp': results[0].get('timestamp'),
                'status': 'success'
            }

            return AgentResponse(
                metadata=metadata,
                output=analysis_result,
                streaming=ANTHROPIC_CONFIG.get('streaming', True)
            )

        except Exception as e:
            error_result = {
                'symbol': symbol,
                'error': str(e),
                'status': 'error'
            }
            return AgentResponse(
                metadata=metadata,
                output=error_result,
                streaming=False
            )

    async def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """
        Get capabilities of all agents
        """
        return {
            'stock_data': self.stock_data_agent._get_capabilities(),
            'sentiment': self.sentiment_agent._get_capabilities(),
            'growth': self.growth_agent._get_capabilities()
        }

async def main():
    orchestrator = StockAnalysisOrchestrator()
    response = await orchestrator.analyze_stock(
        "AAPL",
        user_id='demo_user',
        session_id='demo_session'
    )

    # Handle the response (streaming or non-streaming)
    if response.streaming:
        print("\n** STREAMING RESPONSE **\n")
        # Print metadata
        print(f"> Agent ID: {response.metadata.agent_id}")
        print(f"> Agent Name: {response.metadata.agent_name}")
        print(f"> User Input: {response.metadata.user_input}")
        print(f"> User ID: {response.metadata.user_id}")
        print(f"> Session ID: {response.metadata.session_id}")
        print(f"> Additional Parameters: {response.metadata.additional_params}")
        print("\n> Analysis Results:")
        
        # Handle streaming output
        if isinstance(response.output, AsyncGenerator):
            async for chunk in response.output:
                print(chunk, end='', flush=True)
        else:
            print(response.output)
    else:
        print("\n** RESPONSE **\n")
        print(f"> Agent ID: {response.metadata.agent_id}")
        print(f"> Agent Name: {response.metadata.agent_name}")
        print(f"> Analysis Results: {response.output}")

if __name__ == "__main__":
    asyncio.run(main())
