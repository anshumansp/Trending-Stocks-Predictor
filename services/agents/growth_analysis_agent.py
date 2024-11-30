from typing import Dict, Any, Optional
from base_agent import BaseStockAgent

class GrowthAnalysisAgent(BaseStockAgent):
    def __init__(self):
        super().__init__(
            name="Growth Analysis Agent",
            description="Analyzes company growth potential through financial metrics, market position, and competitive advantages."
        )

    def _get_capabilities(self) -> Dict[str, Any]:
        return {
            'financial_analysis': True,
            'market_position_analysis': True,
            'competitive_analysis': True,
            'growth_metrics': True,
            'risk_assessment': True
        }

    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a growth analysis request"""
        system_prompt = """You are an expert financial growth analyst. Your role is to:
1. Analyze company financial metrics
2. Evaluate market position and competitive advantages
3. Assess growth potential and scalability
4. Identify key growth drivers and barriers
5. Provide risk-adjusted growth projections

Format your response as a structured analysis with clear sections and quantified metrics."""

        # Construct the analysis prompt
        analysis_prompt = f"""Analyze the growth potential for the following context:
{request}

Please provide:
1. Financial Growth Metrics
   - Revenue Growth Rate
   - Profit Margin Trends
   - Cash Flow Analysis
2. Market Position Analysis
   - Market Share
   - Competitive Advantages
   - Industry Position
3. Growth Drivers
   - Key Growth Catalysts
   - Market Opportunities
   - Innovation Pipeline
4. Risk Assessment
   - Growth Barriers
   - Market Risks
   - Execution Risks
5. Growth Projections
   - Short-term (1-2 years)
   - Medium-term (3-5 years)
   - Long-term (5+ years)

Additional Context:
{context if context else 'No additional context provided'}"""

        # Get Claude's analysis
        response = await self._call_claude(analysis_prompt, system_prompt)

        # Process and structure the response
        return {
            'growth_analysis': response,
            'source': 'claude-3-haiku',
            'analysis_type': 'comprehensive_growth',
            'timestamp': context.get('timestamp') if context else None
        }
