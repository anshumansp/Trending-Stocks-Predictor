import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
import ta
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = []

    def create_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create technical indicators as features"""
        # Trend Indicators
        df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
        df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        df['ema_20'] = ta.trend.ema_indicator(df['close'], window=20)
        df['macd'] = ta.trend.macd_diff(df['close'])
        df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'])

        # Momentum Indicators
        df['rsi'] = ta.momentum.rsi(df['close'])
        df['stoch'] = ta.momentum.stoch(df['high'], df['low'], df['close'])
        df['cci'] = ta.trend.cci(df['high'], df['low'], df['close'])
        df['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'])

        # Volatility Indicators
        df['bbands_width'] = ta.volatility.bollinger_wband(df['close'])
        df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])

        # Volume Indicators
        df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
        df['mfi'] = ta.volume.money_flow_index(df['high'], df['low'], df['close'], df['volume'])

        return df

    def create_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create price-based features"""
        # Price Changes
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log1p(df['returns'])
        
        # Rolling Statistics
        windows = [5, 10, 20, 50]
        for window in windows:
            df[f'volatility_{window}d'] = df['returns'].rolling(window).std()
            df[f'momentum_{window}d'] = df['returns'].rolling(window).mean()
            df[f'price_range_{window}d'] = (df['high'].rolling(window).max() - 
                                          df['low'].rolling(window).min()) / df['close']

        # Price Levels
        df['distance_from_high'] = df['close'] / df['high'].rolling(20).max() - 1
        df['distance_from_low'] = df['close'] / df['low'].rolling(20).min() - 1

        return df

    def create_sentiment_features(self, sentiment_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create sentiment-based features"""
        df = pd.DataFrame(sentiment_data)
        
        # Aggregate sentiment scores
        df['sentiment_score'] = df['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})
        df['weighted_sentiment'] = df['sentiment_score'] * df['confidence']
        
        # Calculate sentiment metrics
        sentiment_features = {
            'avg_sentiment': df['sentiment_score'].mean(),
            'weighted_avg_sentiment': (df['weighted_sentiment'] * df['volume']).sum() / df['volume'].sum(),
            'sentiment_volatility': df['sentiment_score'].std(),
            'sentiment_momentum': df['sentiment_score'].diff().mean(),
            'positive_ratio': (df['sentiment_score'] > 0).mean(),
            'negative_ratio': (df['sentiment_score'] < 0).mean()
        }
        
        return pd.DataFrame([sentiment_features])

    def create_market_features(self, market_data: Dict[str, Any]) -> pd.DataFrame:
        """Create market-related features"""
        features = {
            'market_volatility': market_data.get('volatility', 0),
            'sector_performance': market_data.get('sector_performance', 0),
            'market_sentiment': market_data.get('market_sentiment', 0),
            'interest_rate': market_data.get('interest_rate', 0),
            'market_volume': market_data.get('market_volume', 0)
        }
        return pd.DataFrame([features])

    def prepare_features(self, 
                        historical_data: pd.DataFrame,
                        sentiment_data: List[Dict[str, Any]],
                        market_data: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Prepare all features for the model"""
        # Create features from historical data
        df = historical_data.copy()
        df = self.create_technical_features(df)
        df = self.create_price_features(df)

        # Create sentiment features
        sentiment_features = self.create_sentiment_features(sentiment_data)
        
        # Create market features
        market_features = self.create_market_features(market_data)

        # Combine all features
        for col in sentiment_features.columns:
            df[f'sentiment_{col}'] = sentiment_features[col].iloc[0]
        
        for col in market_features.columns:
            df[f'market_{col}'] = market_features[col].iloc[0]

        # Handle missing values
        df = df.fillna(method='ffill').fillna(method='bfill')

        # Scale features
        feature_cols = [col for col in df.columns if col not in ['date', 'open', 'high', 'low', 'close', 'volume']]
        df[feature_cols] = self.scaler.fit_transform(df[feature_cols])

        self.feature_columns = feature_cols
        return df, feature_cols

    def create_targets(self, df: pd.DataFrame, forecast_periods: List[int]) -> pd.DataFrame:
        """Create target variables for different forecast periods"""
        for period in forecast_periods:
            # Calculate future returns
            df[f'target_{period}d'] = df['close'].pct_change(period).shift(-period)
            
            # Calculate risk (volatility) for the period
            df[f'risk_{period}d'] = df['returns'].rolling(period).std().shift(-period)

        return df.dropna()

    def prepare_prediction_data(self, 
                              current_data: pd.DataFrame,
                              sentiment_data: List[Dict[str, Any]],
                              market_data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare features for prediction"""
        df, _ = self.prepare_features(current_data, sentiment_data, market_data)
        return df[self.feature_columns].iloc[-1:]
