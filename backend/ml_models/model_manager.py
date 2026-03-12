"""
Model Manager - Handles loading and managing ML models
"""

import os
import pickle
import numpy as np
from typing import Dict, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages loading and using trained ML models"""
    
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            # Get project root directory (parent of backend)
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            models_dir = os.path.join(project_root, "models")
        self.models_dir = models_dir
        self.models: Dict[str, Dict[str, Any]] = {}
        self.scalers: Dict[str, Any] = {}
        self.load_all_models()
    
    def load_all_models(self):
        """Load all trained models from the models directory"""
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir, exist_ok=True)
            logger.warning(f"Models directory {self.models_dir} does not exist. Created new directory.")
            return
        
        disease_types = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
        
        for disease in disease_types:
            try:
                model_path = os.path.join(self.models_dir, f"{disease}_model.pkl")
                scaler_path = os.path.join(self.models_dir, f"{disease}_scaler.pkl")
                
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        model_data = pickle.load(f)
                        self.models[disease] = model_data
                        logger.info(f"Loaded {disease} model")
                    
                    if os.path.exists(scaler_path):
                        with open(scaler_path, 'rb') as f:
                            self.scalers[disease] = pickle.load(f)
                else:
                    logger.warning(f"Model for {disease} not found at {model_path}")
            except Exception as e:
                logger.error(f"Error loading {disease} model: {str(e)}")
    
    def predict(self, disease: str, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make prediction using the appropriate model
        
        Args:
            disease: Type of disease (diabetes, heart, stroke, liver, kidney)
            features: Dictionary of feature values
            
        Returns:
            Dictionary with prediction results
        """
        if disease not in self.models:
            raise ValueError(f"Model for {disease} not found. Please train the model first.")
        
        model_data = self.models[disease]
        
        # Get feature order from model
        feature_order = model_data.get('feature_order', [])
        
        # Prepare input array
        input_array = []
        for feature in feature_order:
            if feature in features:
                input_array.append(float(features[feature]))
            else:
                raise ValueError(f"Missing required feature: {feature}")
        
        input_array = np.array([input_array])
        
        # Scale if scaler exists
        if disease in self.scalers:
            input_array = self.scalers[disease].transform(input_array)
        
        # Get predictions from all models
        results = {}
        
        # Random Forest prediction
        if 'random_forest' in model_data:
            rf_proba = model_data['random_forest'].predict_proba(input_array)[0]
            results['rf'] = float(rf_proba[1] * 100)  # Probability of positive class
        
        # SVM prediction
        if 'svm' in model_data:
            svm_proba = model_data['svm'].predict_proba(input_array)[0]
            results['svm'] = float(svm_proba[1] * 100)
        
        # Neural Network prediction
        if 'neural_network' in model_data:
            nn_proba = model_data['neural_network'].predict_proba(input_array)[0]
            results['nn'] = float(nn_proba[1] * 100)
        
        # Ensemble prediction (weighted average)
        if results:
            weights = {'rf': 0.4, 'svm': 0.3, 'nn': 0.3}
            ensemble_score = sum(results.get(key, 0) * weights.get(key, 0) for key in weights.keys())
            results['ensemble'] = float(ensemble_score)
        else:
            # Fallback to single model if available
            if 'model' in model_data:
                proba = model_data['model'].predict_proba(input_array)[0]
                results['ensemble'] = float(proba[1] * 100)
        
        # Get feature importance if available
        feature_importance = {}
        if 'random_forest' in model_data:
            importances = model_data['random_forest'].feature_importances_
            for i, feature in enumerate(feature_order):
                if i < len(importances):
                    feature_importance[feature] = float(importances[i])
        
        results['confidence'] = 90.0  # Can be calculated from model confidence
        results['feature_importance'] = feature_importance
        
        return results
    
    def get_model_info(self, disease: str) -> Optional[Dict[str, Any]]:
        """Get information about a trained model"""
        if disease not in self.models:
            return None
        
        model_data = self.models[disease]
        return {
            'disease': disease,
            'accuracy': model_data.get('accuracy', 'N/A'),
            'features': model_data.get('feature_order', []),
            'model_types': list(model_data.keys()),
            'trained': True
        }
    
    def reload_model(self, disease: str):
        """Reload a specific model"""
        model_path = os.path.join(self.models_dir, f"{disease}_model.pkl")
        scaler_path = os.path.join(self.models_dir, f"{disease}_scaler.pkl")
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.models[disease] = pickle.load(f)
            
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scalers[disease] = pickle.load(f)
            
            logger.info(f"Reloaded {disease} model")
        else:
            raise FileNotFoundError(f"Model file not found: {model_path}")

# Global model manager instance
model_manager = ModelManager()

