import asyncio
import boto3
import json
from typing import Dict, Any, List
import redis
from stock_data_agent import StockDataAgent
from sentiment_agent import SentimentAgent
from growth_analysis_agent import GrowthAnalysisAgent
from config import AWS_CONFIG, REDIS_CONFIG

class StockAnalysisOrchestrator:
    def __init__(self):
        self.stock_agent = StockDataAgent()
        self.sentiment_agent = SentimentAgent()
        self.growth_agent = GrowthAnalysisAgent()
        
        # Initialize AWS services
        self.sqs = boto3.client('sqs', **AWS_CONFIG)
        self.lambda_client = boto3.client('lambda', **AWS_CONFIG)
        
        # Initialize Redis for agent communication
        self.redis_client = redis.Redis(
            host=REDIS_CONFIG['host'],
            port=REDIS_CONFIG['port'],
            db=REDIS_CONFIG['db']
        )

    async def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Orchestrate full stock analysis"""
        try:
            # Step 1: Gather stock data
            stock_data = await self.stock_agent.process({
                'action': 'analyze',
                'symbol': symbol
            })

            # Step 2: Analyze sentiment in parallel with technical analysis
            sentiment_task = asyncio.create_task(
                self.sentiment_agent.process({
                    'action': 'analyze',
                    'symbol': symbol
                })
            )

            technical_task = asyncio.create_task(
                self.stock_agent.process({
                    'action': 'technical_analysis',
                    'data': stock_data['result']
                })
            )

            sentiment_result, technical_result = await asyncio.gather(
                sentiment_task,
                technical_task
            )

            # Step 3: Perform growth analysis with all collected data
            growth_analysis = await self.growth_agent.process({
                'action': 'analyze',
                'data': {
                    'stock_data': stock_data['result'],
                    'technical_analysis': technical_result['result'],
                    'sentiment_data': sentiment_result['result']
                }
            })

            # Step 4: Compile final recommendation
            return self._compile_recommendation(
                symbol,
                stock_data['result'],
                technical_result['result'],
                sentiment_result['result'],
                growth_analysis['result']
            )

        except Exception as e:
            return {
                'status': 'error',
                'error': f"Analysis failed: {str(e)}"
            }

    def _compile_recommendation(
        self,
        symbol: str,
        stock_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        sentiment_data: Dict[str, Any],
        growth_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile final stock recommendation"""
        try:
            # Calculate overall score
            technical_score = technical_data.get('score', 0) * 0.3
            sentiment_score = sentiment_data.get('aggregated_sentiment', {}).get('score', 0) * 0.3
            growth_score = growth_data.get('growth_assessment', {}).get('overall_score', 0) * 0.4

            overall_score = technical_score + sentiment_score + growth_score

            # Generate recommendation
            recommendation = self._generate_recommendation(overall_score)

            return {
                'status': 'success',
                'symbol': symbol,
                'recommendation': {
                    'overall_score': overall_score,
                    'recommendation': recommendation,
                    'components': {
                        'technical_analysis': technical_data,
                        'sentiment_analysis': sentiment_data,
                        'growth_analysis': growth_data
                    },
                    'current_data': stock_data
                }
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': f"Failed to compile recommendation: {str(e)}"
            }

    def _generate_recommendation(self, score: float) -> Dict[str, Any]:
        """Generate detailed recommendation based on score"""
        if score >= 80:
            strength = "Strong Buy"
            confidence = "High"
            timeframe = "Long-term"
        elif score >= 60:
            strength = "Buy"
            confidence = "Moderate"
            timeframe = "Medium-term"
        elif score >= 40:
            strength = "Hold"
            confidence = "Moderate"
            timeframe = "Short-term"
        else:
            strength = "Sell"
            confidence = "High"
            timeframe = "Immediate"

        return {
            'strength': strength,
            'confidence': confidence,
            'timeframe': timeframe,
            'score': score
        }

    async def process_queue(self):
        """Process incoming analysis requests from SQS"""
        while True:
            try:
                # Receive messages from SQS
                response = self.sqs.receive_message(
                    QueueUrl='YOUR_SQS_QUEUE_URL',
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20
                )

                messages = response.get('Messages', [])
                
                for message in messages:
                    # Process message
                    body = json.loads(message['Body'])
                    symbol = body.get('symbol')
                    
                    if symbol:
                        # Perform analysis
                        result = await self.analyze_stock(symbol)
                        
                        # Store result in Redis
                        self.redis_client.setex(
                            f"analysis:{symbol}",
                            3600,  # 1 hour expiration
                            json.dumps(result)
                        )
                        
                        # Delete processed message
                        self.sqs.delete_message(
                            QueueUrl='YOUR_SQS_QUEUE_URL',
                            ReceiptHandle=message['ReceiptHandle']
                        )

            except Exception as e:
                print(f"Error processing queue: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying

    async def start(self):
        """Start the orchestrator"""
        try:
            # Start queue processing
            queue_processor = asyncio.create_task(self.process_queue())
            
            # Keep the orchestrator running
            await queue_processor

        except Exception as e:
            print(f"Orchestrator error: {str(e)}")
            raise

if __name__ == "__main__":
    # Create and start the orchestrator
    orchestrator = StockAnalysisOrchestrator()
    
    # Run the orchestrator
    asyncio.run(orchestrator.start())
