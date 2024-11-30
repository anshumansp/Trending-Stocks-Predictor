from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate
from typing import List, Dict, Any
import tweepy
import praw
from textblob import TextBlob
from transformers import pipeline
from base_agent import BaseAgent
from config import TWITTER_CONFIG, REDDIT_CONFIG, SENTIMENT_CONFIG

class SentimentPromptTemplate(StringPromptTemplate):
    template = """You are a Sentiment Analysis Agent responsible for analyzing market sentiment from various sources.
Your goal is to gauge market sentiment and provide insights that could impact stock performance.

You have access to the following tools:
{tools}

Current conversation:
{chat_history}

New input: {input}

Think through this step-by-step:
1) What sources should you analyze for sentiment?
2) How should you weigh different sources?
3) What timeframe should you consider?

Action: """

    def format(self, **kwargs) -> str:
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in kwargs["tools"]])
        return self.template.format(**kwargs)

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("SentimentAgent")
        self._init_social_media_clients()
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )

    def _init_social_media_clients(self):
        """Initialize social media API clients"""
        # Twitter setup
        auth = tweepy.OAuthHandler(
            TWITTER_CONFIG['api_key'],
            TWITTER_CONFIG['api_secret']
        )
        auth.set_access_token(
            TWITTER_CONFIG['access_token'],
            TWITTER_CONFIG['access_token_secret']
        )
        self.twitter_client = tweepy.API(auth)

        # Reddit setup
        self.reddit_client = praw.Reddit(
            client_id=REDDIT_CONFIG['client_id'],
            client_secret=REDDIT_CONFIG['client_secret'],
            user_agent=REDDIT_CONFIG['user_agent']
        )

    def _get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="analyze_social_media",
                func=self._analyze_social_media,
                description="Analyze sentiment from social media posts about a stock"
            ),
            Tool(
                name="analyze_news_sentiment",
                func=self._analyze_news_sentiment,
                description="Analyze sentiment from news articles about a stock"
            ),
            Tool(
                name="get_aggregated_sentiment",
                func=self._get_aggregated_sentiment,
                description="Get aggregated sentiment analysis from all sources"
            )
        ]

    def _create_prompt(self) -> StringPromptTemplate:
        return SentimentPromptTemplate()

    async def _analyze_social_media(self, symbol: str) -> Dict[str, Any]:
        """Analyze sentiment from social media posts"""
        try:
            # Twitter analysis
            tweets = self.twitter_client.search_tweets(
                q=f"${symbol}",
                lang="en",
                count=100,
                tweet_mode="extended"
            )
            
            twitter_sentiments = []
            for tweet in tweets:
                sentiment = self.sentiment_analyzer(tweet.full_text)[0]
                twitter_sentiments.append({
                    'text': tweet.full_text,
                    'sentiment': sentiment['label'],
                    'score': sentiment['score']
                })

            # Reddit analysis
            subreddit = self.reddit_client.subreddit("stocks+investing+wallstreetbets")
            posts = subreddit.search(f"{symbol}", limit=50)
            
            reddit_sentiments = []
            for post in posts:
                sentiment = self.sentiment_analyzer(post.title + " " + post.selftext)[0]
                reddit_sentiments.append({
                    'title': post.title,
                    'sentiment': sentiment['label'],
                    'score': sentiment['score']
                })

            return {
                'symbol': symbol,
                'twitter_sentiment': {
                    'data': twitter_sentiments,
                    'summary': self._summarize_sentiments(twitter_sentiments)
                },
                'reddit_sentiment': {
                    'data': reddit_sentiments,
                    'summary': self._summarize_sentiments(reddit_sentiments)
                }
            }

        except Exception as e:
            return {'error': f"Failed to analyze social media: {str(e)}"}

    async def _analyze_news_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze sentiment from news articles"""
        try:
            # Implementation of news sentiment analysis
            # This would integrate with a news API and analyze sentiment
            return {
                'symbol': symbol,
                'news_sentiment': {
                    'overall_score': 0,
                    'articles': []
                }
            }
        except Exception as e:
            return {'error': f"Failed to analyze news sentiment: {str(e)}"}

    async def _get_aggregated_sentiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate sentiment from all sources"""
        try:
            social_media_sentiment = data.get('social_media', {})
            news_sentiment = data.get('news_sentiment', {})

            # Implement aggregation logic
            aggregated_score = 0  # Calculate weighted average

            return {
                'symbol': data['symbol'],
                'aggregated_sentiment': {
                    'score': aggregated_score,
                    'sources': {
                        'social_media': social_media_sentiment,
                        'news': news_sentiment
                    }
                }
            }
        except Exception as e:
            return {'error': f"Failed to aggregate sentiment: {str(e)}"}

    def _summarize_sentiments(self, sentiments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Summarize sentiment scores"""
        if not sentiments:
            return {
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0
            }

        counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_score = 0

        for sentiment in sentiments:
            counts[sentiment['sentiment']] += 1
            total_score += sentiment['score']

        total = len(sentiments)
        return {
            'positive': counts['positive'] / total,
            'negative': counts['negative'] / total,
            'neutral': counts['neutral'] / total,
            'average_score': total_score / total
        }

    async def handle_callback(self, message: Dict[str, Any]) -> None:
        """Handle messages from other agents"""
        if message.get('type') == 'sentiment_request':
            result = await self.process(message['data'])
            # Implement callback mechanism to respond to the requesting agent
            pass
