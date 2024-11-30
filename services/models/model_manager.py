import pandas as pd
from typing import Dict, Any, List
import joblib
import json
from datetime import datetime
import os
from predictive_model import StockPredictiveModel

class ModelManager:
    def __init__(self, model_dir: str = 'models'):
        self.model_dir = model_dir
        self.models = {}
        self.model_metadata = {}
        os.makedirs(model_dir, exist_ok=True)

    def train_model(self, 
                   symbol: str,
                   historical_data: pd.DataFrame,
                   sentiment_data: List[Dict[str, Any]],
                   market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train a new model for a stock"""
        try:
            # Initialize and train model
            model = StockPredictiveModel()
            results = model.train(historical_data, sentiment_data, market_data)

            if results['status'] == 'success':
                # Save model and metadata
                self.models[symbol] = model
                self.model_metadata[symbol] = {
                    'last_trained': datetime.now().isoformat(),
                    'metrics': results['metrics'],
                    'feature_importance': results['feature_importance']
                }

                # Save to disk
                self._save_model(symbol, model)
                self._save_metadata(symbol)

            return results

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def get_prediction(self,
                      symbol: str,
                      current_data: pd.DataFrame,
                      sentiment_data: List[Dict[str, Any]],
                      market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get predictions for a stock"""
        try:
            # Load model if not in memory
            if symbol not in self.models:
                self._load_model(symbol)

            # Get predictions
            model = self.models[symbol]
            predictions = model.predict(current_data, sentiment_data, market_data)

            # Format predictions
            if predictions['status'] == 'success':
                formatted_predictions = self._format_predictions(predictions['predictions'])
                return {
                    'status': 'success',
                    'predictions': formatted_predictions,
                    'metadata': self.model_metadata[symbol]
                }
            else:
                return predictions

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _format_predictions(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Format predictions for better readability"""
        formatted = {}
        period_names = {
            '1d': 'Next Day',
            '5d': 'Next Week',
            '10d': 'Next Two Weeks',
            '20d': 'Next Month'
        }

        for period, pred in predictions.items():
            growth_pred = pred['growth']['prediction']
            confidence_interval = pred['growth']['confidence_interval']
            risk_level = pred['risk']['level']

            formatted[period_names[period]] = {
                'growth': {
                    'prediction': f"{growth_pred:.1f}%",
                    'range': f"{confidence_interval['lower']:.1f}% to {confidence_interval['upper']:.1f}%"
                },
                'risk': {
                    'level': risk_level,
                    'score': f"{pred['risk']['score']:.2f}"
                }
            }

        return formatted

    def _save_model(self, symbol: str, model: StockPredictiveModel):
        """Save model to disk"""
        model_path = os.path.join(self.model_dir, f"{symbol}_model.joblib")
        joblib.dump(model, model_path)

    def _save_metadata(self, symbol: str):
        """Save model metadata to disk"""
        metadata_path = os.path.join(self.model_dir, f"{symbol}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.model_metadata[symbol], f)

    def _load_model(self, symbol: str):
        """Load model from disk"""
        model_path = os.path.join(self.model_dir, f"{symbol}_model.joblib")
        metadata_path = os.path.join(self.model_dir, f"{symbol}_metadata.json")

        if os.path.exists(model_path) and os.path.exists(metadata_path):
            self.models[symbol] = joblib.load(model_path)
            with open(metadata_path, 'r') as f:
                self.model_metadata[symbol] = json.load(f)
        else:
            raise FileNotFoundError(f"No trained model found for {symbol}")

    def get_model_metadata(self, symbol: str) -> Dict[str, Any]:
        """Get model metadata"""
        if symbol in self.model_metadata:
            return {
                'status': 'success',
                'metadata': self.model_metadata[symbol]
            }
        else:
            return {
                'status': 'error',
                'error': f"No metadata found for {symbol}"
            }

    def retrain_if_needed(self,
                         symbol: str,
                         historical_data: pd.DataFrame,
                         sentiment_data: List[Dict[str, Any]],
                         market_data: Dict[str, Any],
                         max_age_days: int = 7) -> Dict[str, Any]:
        """Retrain model if it's too old"""
        try:
            if symbol in self.model_metadata:
                last_trained = datetime.fromisoformat(self.model_metadata[symbol]['last_trained'])
                age = (datetime.now() - last_trained).days

                if age > max_age_days:
                    return self.train_model(symbol, historical_data, sentiment_data, market_data)
                else:
                    return {
                        'status': 'success',
                        'message': f"Model is up to date (last trained {age} days ago)"
                    }
            else:
                return self.train_model(symbol, historical_data, sentiment_data, market_data)

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
