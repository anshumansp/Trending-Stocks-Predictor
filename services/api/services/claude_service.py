import os
import anthropic
from typing import Dict, List, Optional
from fastapi import HTTPException

class ClaudeService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_CLAUDE_API_KEY environment variable is not set")
        self.client = anthropic.Client(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"  # Using Claude 3 Haiku
        self.max_tokens = 4096  # Haiku's context window

    async def analyze_stock_sentiment(self, 
        company_name: str,
        news_data: List[Dict],
        financial_data: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze stock sentiment using Claude's advanced NLP capabilities
        """
        try:
            # Prepare context for Claude
            context = f"Analyze the sentiment and potential impact on {company_name}'s stock based on the following information:\n\n"
            
            # Add news articles
            context += "Recent News:\n"
            for article in news_data:
                context += f"- {article['title']}: {article['summary']}\n"
            
            # Add financial data if available
            if financial_data:
                context += "\nFinancial Metrics:\n"
                for key, value in financial_data.items():
                    context += f"- {key}: {value}\n"
            
            # Create the message with system prompt
            system_prompt = "You are a financial analyst expert. Provide concise, accurate analysis of stock sentiment and market impact."
            
            # Get Claude's response
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context + "\nProvide a detailed analysis of the sentiment, key factors affecting the stock, and potential market impact. Format the response as JSON with 'sentiment_score', 'analysis', 'key_factors', and 'market_impact' fields."
                    }
                ]
            )

            # Parse the response content
            content = response.content[0].text
            
            # Here you would parse the JSON response
            # For now, returning a simplified structure
            return {
                "sentiment_score": 0.0,  # This should be parsed from Claude's response
                "analysis": content,
                "key_factors": [],  # This should be parsed from Claude's response
                "market_impact": ""  # This should be parsed from Claude's response
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing stock sentiment: {str(e)}"
            )

    async def generate_market_insights(self, market_data: Dict) -> Dict:
        """
        Generate comprehensive market insights using Claude
        """
        try:
            # Prepare context
            context = "Based on the following market data, provide comprehensive insights:\n\n"
            for key, value in market_data.items():
                context += f"{key}: {value}\n"

            # Create message with system prompt
            system_prompt = "You are a market analysis expert. Provide clear, actionable insights based on market data."
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context + "\nProvide market insights, trends, and recommendations."
                    }
                ]
            )

            return {
                "insights": response.content[0].text,
                "timestamp": market_data.get("timestamp", "")
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating market insights: {str(e)}"
            )

    async def analyze_company_fundamentals(self, 
        company_symbol: str,
        fundamental_data: Dict
    ) -> Dict:
        """
        Analyze company fundamentals using Claude
        """
        try:
            # Prepare context
            context = f"Analyze the fundamental data for {company_symbol}:\n\n"
            for key, value in fundamental_data.items():
                context += f"{key}: {value}\n"

            # Create message with system prompt
            system_prompt = "You are a fundamental analysis expert. Provide detailed analysis of company fundamentals and financial health."
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context + "\nProvide a comprehensive analysis of the company's fundamentals, financial health, and future outlook."
                    }
                ]
            )

            return {
                "analysis": response.content[0].text,
                "company_symbol": company_symbol,
                "timestamp": fundamental_data.get("timestamp", "")
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing company fundamentals: {str(e)}"
            )
