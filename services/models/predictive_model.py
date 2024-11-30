import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import optuna
import mlflow
import shap
from datetime import datetime, timedelta
from feature_engineering import FeatureEngineer

class StockPredictiveModel:
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.models = {}
        self.feature_importance = {}
        self.shap_values = {}
        self.forecast_periods = [1, 5, 10, 20]  # 1 day, 1 week, 2 weeks, 1 month

    def train(self, 
             historical_data: pd.DataFrame,
             sentiment_data: List[Dict[str, Any]],
             market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train prediction models for different time horizons"""
        try:
            # Prepare features and targets
            df, feature_cols = self.feature_engineer.prepare_features(
                historical_data, sentiment_data, market_data
            )
            df = self.feature_engineer.create_targets(df, self.forecast_periods)

            # Train models for each forecast period
            results = {}
            for period in self.forecast_periods:
                # Train growth prediction model
                growth_model, growth_metrics = self._train_model(
                    df[feature_cols],
                    df[f'target_{period}d'],
                    f'growth_{period}d'
                )
                
                # Train risk prediction model
                risk_model, risk_metrics = self._train_model(
                    df[feature_cols],
                    df[f'risk_{period}d'],
                    f'risk_{period}d'
                )

                self.models[f'growth_{period}d'] = growth_model
                self.models[f'risk_{period}d'] = risk_model

                # Calculate feature importance
                self._calculate_feature_importance(
                    growth_model, 
                    feature_cols,
                    df[feature_cols],
                    f'growth_{period}d'
                )

                results[f'{period}d'] = {
                    'growth_metrics': growth_metrics,
                    'risk_metrics': risk_metrics
                }

            return {
                'status': 'success',
                'metrics': results,
                'feature_importance': self.feature_importance
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def predict(self,
               current_data: pd.DataFrame,
               sentiment_data: List[Dict[str, Any]],
               market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate predictions for different time horizons"""
        try:
            # Prepare prediction data
            X = self.feature_engineer.prepare_prediction_data(
                current_data, sentiment_data, market_data
            )

            predictions = {}
            for period in self.forecast_periods:
                # Predict growth
                growth_pred = self.models[f'growth_{period}d'].predict(X)[0]
                
                # Predict risk
                risk_pred = self.models[f'risk_{period}d'].predict(X)[0]

                # Calculate confidence intervals
                growth_std = self.models[f'growth_{period}d'].predict_proba(X)[0].std()
                
                predictions[f'{period}d'] = {
                    'growth': {
                        'prediction': growth_pred,
                        'confidence_interval': {
                            'lower': growth_pred - 1.96 * growth_std,
                            'upper': growth_pred + 1.96 * growth_std
                        }
                    },
                    'risk': {
                        'score': risk_pred,
                        'level': self._categorize_risk(risk_pred)
                    }
                }

            return {
                'status': 'success',
                'predictions': predictions,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _train_model(self, 
                    X: pd.DataFrame, 
                    y: pd.Series,
                    model_name: str) -> Tuple[Any, Dict[str, float]]:
        """Train and optimize a model"""
        # Create time series cross-validation
        tscv = TimeSeriesSplit(n_splits=5)

        # Define optimization objective
        def objective(trial):
            # Create model with trial parameters
            model = self._create_model(trial)
            
            # Perform cross-validation
            scores = []
            for train_idx, val_idx in tscv.split(X):
                X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                
                model.fit(X_train, y_train)
                pred = model.predict(X_val)
                score = np.sqrt(np.mean((y_val - pred) ** 2))
                scores.append(score)
            
            return np.mean(scores)

        # Optimize hyperparameters
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=50)

        # Train final model with best parameters
        best_model = self._create_model(study.best_trial)
        best_model.fit(X, y)

        # Calculate metrics
        metrics = self._calculate_metrics(best_model, X, y)

        # Log to MLflow
        with mlflow.start_run(run_name=model_name):
            mlflow.log_params(study.best_params)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(best_model, model_name)

        return best_model, metrics

    def _create_model(self, trial: optuna.Trial) -> Any:
        """Create model with trial parameters"""
        model_type = trial.suggest_categorical('model_type', 
            ['rf', 'gbm', 'xgb', 'lgbm']
        )

        if model_type == 'rf':
            return RandomForestRegressor(
                n_estimators=trial.suggest_int('n_estimators', 100, 500),
                max_depth=trial.suggest_int('max_depth', 3, 10),
                min_samples_split=trial.suggest_int('min_samples_split', 2, 10),
                random_state=42
            )
        elif model_type == 'gbm':
            return GradientBoostingRegressor(
                n_estimators=trial.suggest_int('n_estimators', 100, 500),
                learning_rate=trial.suggest_loguniform('learning_rate', 1e-3, 1e-1),
                max_depth=trial.suggest_int('max_depth', 3, 10),
                random_state=42
            )
        elif model_type == 'xgb':
            return XGBRegressor(
                n_estimators=trial.suggest_int('n_estimators', 100, 500),
                learning_rate=trial.suggest_loguniform('learning_rate', 1e-3, 1e-1),
                max_depth=trial.suggest_int('max_depth', 3, 10),
                random_state=42
            )
        else:
            return LGBMRegressor(
                n_estimators=trial.suggest_int('n_estimators', 100, 500),
                learning_rate=trial.suggest_loguniform('learning_rate', 1e-3, 1e-1),
                max_depth=trial.suggest_int('max_depth', 3, 10),
                random_state=42
            )

    def _calculate_metrics(self, 
                         model: Any, 
                         X: pd.DataFrame, 
                         y: pd.Series) -> Dict[str, float]:
        """Calculate model performance metrics"""
        pred = model.predict(X)
        return {
            'rmse': np.sqrt(np.mean((y - pred) ** 2)),
            'mae': np.mean(np.abs(y - pred)),
            'r2': model.score(X, y)
        }

    def _calculate_feature_importance(self,
                                   model: Any,
                                   feature_cols: List[str],
                                   X: pd.DataFrame,
                                   model_name: str):
        """Calculate and store feature importance"""
        # Get feature importance from model
        importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        # Calculate SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        self.feature_importance[model_name] = importance
        self.shap_values[model_name] = shap_values

    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level based on score"""
        if risk_score < 0.2:
            return 'Very Low'
        elif risk_score < 0.4:
            return 'Low'
        elif risk_score < 0.6:
            return 'Moderate'
        elif risk_score < 0.8:
            return 'High'
        else:
            return 'Very High'

    def get_feature_importance(self, model_name: str) -> Dict[str, Any]:
        """Get feature importance analysis"""
        if model_name not in self.feature_importance:
            return {'error': 'Model not found'}

        return {
            'feature_importance': self.feature_importance[model_name].to_dict(),
            'shap_values': self.shap_values[model_name].tolist()
        }
