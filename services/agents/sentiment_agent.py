from typing import Dict, Any, Optional
from base_agent import BaseStockAgent

class SentimentAgent(BaseStockAgent):
    def __init__(self):
        super().__init__(
            name="Sentiment Agent",
            description="Analyzes market sentiment through news, social media, and other sources. Specializes in natural language processing of market-related content."
        )

    def _get_capabilities(self) -> Dict[str, Any]:
        return {
            'sentiment_analysis': True,
            'news_processing': True,
            'social_media_analysis': True,
            'market_mood_detection': True,
            'trend_analysis': True
        }

    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a sentiment analysis request"""
        system_prompt = """You are an expert financial sentiment analyzer. Your role is to:
1. Analyze market sentiment from various sources
2. Detect sentiment patterns and trends
3. Evaluate the impact of news and social media on market sentiment
4. Provide quantified sentiment scores
5. Identify key sentiment drivers

Format your response as a structured analysis with clear sections and metrics."""

        # Construct the analysis prompt
        analysis_prompt = f"""Analyze the market sentiment for the following context:
{request}

Please provide:
1. Overall Sentiment Score (0-100)
2. Sentiment Breakdown:
   - News Sentiment
   - Social Media Sentiment
   - Market Commentary Sentiment
3. Key Drivers of Current Sentiment
4. Trend Analysis
5. Risk Factors
6. Confidence Level in Analysis

Additional Context:
{context if context else 'No additional context provided'}"""

        # Get Claude's analysis
        response = await self._call_claude(analysis_prompt, system_prompt)

        # Process and structure the response
        return {
            'sentiment_analysis': response,
            'source': 'claude-3-haiku',
            'analysis_type': 'comprehensive_sentiment',
            'timestamp': context.get('timestamp') if context else None
        }
