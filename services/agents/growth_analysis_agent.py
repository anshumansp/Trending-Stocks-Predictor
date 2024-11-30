from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate
from typing import List, Dict, Any
import numpy as np
from base_agent import BaseAgent

class GrowthAnalysisPromptTemplate(StringPromptTemplate):
    template = """You are a Growth Analysis Agent responsible for evaluating a stock's growth potential.
Your goal is to analyze various factors and provide a comprehensive growth assessment.

You have access to the following tools:
{tools}

Current conversation:
{chat_history}

New input: {input}

Think through this step-by-step:
1) What growth metrics should you analyze?
2) How do you evaluate the company's competitive position?
3) What are the key risk factors to consider?

Action: """

    def format(self, **kwargs) -> str:
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in kwargs["tools"]])
        return self.template.format(**kwargs)

class GrowthAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("GrowthAnalysisAgent")

    def _get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="analyze_financial_metrics",
                func=self._analyze_financial_metrics,
                description="Analyze key financial metrics for growth assessment"
            ),
            Tool(
                name="evaluate_market_position",
                func=self._evaluate_market_position,
                description="Evaluate the company's market position and competitive advantages"
            ),
            Tool(
                name="assess_growth_potential",
                func=self._assess_growth_potential,
                description="Provide comprehensive growth potential assessment"
            )
        ]

    def _create_prompt(self) -> StringPromptTemplate:
        return GrowthAnalysisPromptTemplate()

    async def _analyze_financial_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key financial metrics"""
        try:
            metrics = data.get('metrics', {})
            
            # Calculate growth rates
            revenue_growth = self._calculate_growth_rate(metrics.get('revenue', []))
            profit_growth = self._calculate_growth_rate(metrics.get('profit', []))
            
            # Calculate efficiency ratios
            roi = self._calculate_roi(metrics)
            asset_turnover = self._calculate_asset_turnover(metrics)

            return {
                'symbol': data['symbol'],
                'financial_analysis': {
                    'growth_rates': {
                        'revenue': revenue_growth,
                        'profit': profit_growth
                    },
                    'efficiency_ratios': {
                        'roi': roi,
                        'asset_turnover': asset_turnover
                    },
                    'risk_metrics': self._calculate_risk_metrics(metrics)
                }
            }

        except Exception as e:
            return {'error': f"Failed to analyze financial metrics: {str(e)}"}

    async def _evaluate_market_position(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate market position and competitive advantages"""
        try:
            market_data = data.get('market_data', {})
            
            return {
                'symbol': data['symbol'],
                'market_position': {
                    'market_share': self._calculate_market_share(market_data),
                    'competitive_advantages': self._identify_competitive_advantages(market_data),
                    'industry_analysis': self._analyze_industry(market_data)
                }
            }

        except Exception as e:
            return {'error': f"Failed to evaluate market position: {str(e)}"}

    async def _assess_growth_potential(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide comprehensive growth assessment"""
        try:
            financial_analysis = data.get('financial_analysis', {})
            market_position = data.get('market_position', {})
            sentiment_data = data.get('sentiment_data', {})

            growth_score = self._calculate_growth_score(
                financial_analysis,
                market_position,
                sentiment_data
            )

            return {
                'symbol': data['symbol'],
                'growth_assessment': {
                    'overall_score': growth_score,
                    'components': {
                        'financial_health': self._assess_financial_health(financial_analysis),
                        'market_strength': self._assess_market_strength(market_position),
                        'sentiment_impact': self._assess_sentiment_impact(sentiment_data)
                    },
                    'recommendations': self._generate_recommendations(growth_score)
                }
            }

        except Exception as e:
            return {'error': f"Failed to assess growth potential: {str(e)}"}

    def _calculate_growth_rate(self, values: List[float]) -> float:
        """Calculate compound annual growth rate"""
        if not values or len(values) < 2:
            return 0.0
        
        try:
            start_value = values[0]
            end_value = values[-1]
            periods = len(values) - 1
            
            if start_value <= 0 or end_value <= 0:
                return 0.0
                
            return (np.power(end_value / start_value, 1/periods) - 1) * 100
        except:
            return 0.0

    def _calculate_roi(self, metrics: Dict[str, Any]) -> float:
        """Calculate return on investment"""
        try:
            net_income = metrics.get('net_income', 0)
            total_investment = metrics.get('total_investment', 1)  # Avoid division by zero
            return (net_income / total_investment) * 100
        except:
            return 0.0

    def _calculate_asset_turnover(self, metrics: Dict[str, Any]) -> float:
        """Calculate asset turnover ratio"""
        try:
            revenue = metrics.get('revenue', 0)
            total_assets = metrics.get('total_assets', 1)  # Avoid division by zero
            return revenue / total_assets
        except:
            return 0.0

    def _calculate_risk_metrics(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate various risk metrics"""
        return {
            'beta': metrics.get('beta', 0),
            'volatility': metrics.get('volatility', 0),
            'sharpe_ratio': metrics.get('sharpe_ratio', 0)
        }

    def _calculate_market_share(self, market_data: Dict[str, Any]) -> float:
        """Calculate market share percentage"""
        try:
            company_revenue = market_data.get('company_revenue', 0)
            total_market_size = market_data.get('total_market_size', 1)  # Avoid division by zero
            return (company_revenue / total_market_size) * 100
        except:
            return 0.0

    def _identify_competitive_advantages(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify and score competitive advantages"""
        advantages = []
        for advantage in market_data.get('competitive_advantages', []):
            advantages.append({
                'type': advantage['type'],
                'strength': advantage['strength'],
                'sustainability': advantage['sustainability']
            })
        return advantages

    def _analyze_industry(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze industry conditions"""
        return {
            'growth_rate': market_data.get('industry_growth_rate', 0),
            'barriers_to_entry': market_data.get('barriers_to_entry', 'medium'),
            'competition_level': market_data.get('competition_level', 'high')
        }

    def _calculate_growth_score(
        self,
        financial_analysis: Dict[str, Any],
        market_position: Dict[str, Any],
        sentiment_data: Dict[str, Any]
    ) -> float:
        """Calculate overall growth score"""
        # Implement weighted scoring system
        weights = {
            'financial': 0.4,
            'market': 0.4,
            'sentiment': 0.2
        }

        financial_score = self._calculate_financial_score(financial_analysis)
        market_score = self._calculate_market_score(market_position)
        sentiment_score = self._calculate_sentiment_score(sentiment_data)

        return (
            financial_score * weights['financial'] +
            market_score * weights['market'] +
            sentiment_score * weights['sentiment']
        )

    def _assess_financial_health(self, financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financial health components"""
        return {
            'growth_sustainability': self._assess_growth_sustainability(financial_analysis),
            'profitability': self._assess_profitability(financial_analysis),
            'efficiency': self._assess_efficiency(financial_analysis)
        }

    def _assess_market_strength(self, market_position: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market strength components"""
        return {
            'competitive_position': self._assess_competitive_position(market_position),
            'market_trends': self._assess_market_trends(market_position),
            'growth_opportunities': self._assess_growth_opportunities(market_position)
        }

    def _assess_sentiment_impact(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess sentiment impact on growth"""
        return {
            'market_sentiment': sentiment_data.get('market_sentiment', 'neutral'),
            'investor_confidence': sentiment_data.get('investor_confidence', 'medium'),
            'news_impact': sentiment_data.get('news_impact', 'neutral')
        }

    def _generate_recommendations(self, growth_score: float) -> List[str]:
        """Generate growth-based recommendations"""
        recommendations = []
        
        if growth_score >= 80:
            recommendations.append("Strong growth potential - Consider for long-term investment")
        elif growth_score >= 60:
            recommendations.append("Moderate growth potential - Monitor for entry points")
        else:
            recommendations.append("Limited growth potential - Consider alternative investments")

        return recommendations

    async def handle_callback(self, message: Dict[str, Any]) -> None:
        """Handle messages from other agents"""
        if message.get('type') == 'growth_analysis_request':
            result = await self.process(message['data'])
            # Implement callback mechanism to respond to the requesting agent
            pass
