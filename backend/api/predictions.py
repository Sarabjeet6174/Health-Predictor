"""
Prediction API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from backend.ml_models.model_manager import model_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class PredictionRequest(BaseModel):
    disease: str
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    ensemble: float
    rf: Optional[float] = None
    svm: Optional[float] = None
    nn: Optional[float] = None
    confidence: float
    feature_importance: Dict[str, float]

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make a health risk prediction
    
    Args:
        request: PredictionRequest with disease type and features
        
    Returns:
        PredictionResponse with risk scores and feature importance
    """
    try:
        logger.info("=" * 60)
        logger.info("PREDICTION REQUEST RECEIVED")
        logger.info("=" * 60)
        logger.info(f"Disease: {request.disease}")
        logger.info(f"Features received: {list(request.features.keys())}")
        logger.info(f"Feature values: {request.features}")
        
        # Validate disease type
        valid_diseases = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
        if request.disease not in valid_diseases:
            error_msg = f"Invalid disease type '{request.disease}'. Must be one of: {valid_diseases}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Check if model exists
        if request.disease not in model_manager.models:
            error_msg = f"Model for '{request.disease}' not found. Please train the model first using: python train_all_models.py"
            logger.error(error_msg)
            logger.info(f"Available models: {list(model_manager.models.keys())}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Prepare features
        raw_features = dict(request.features)
        
        # For non-diabetes diseases, convert all features to float
        if request.disease != 'diabetes':
            features = {}
            for k, v in raw_features.items():
                try:
                    features[k] = float(v)
                except (ValueError, TypeError) as e:
                    error_msg = f"Invalid value for feature '{k}': {v}. Must be a number. Error: {str(e)}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=400, detail=error_msg)
            logger.info(f"Converted features: {features}")
        else:
            # For diabetes, allow categorical values (gender, smoking_history) and let ModelManager handle encoding
            features = raw_features
            logger.info(f"Using raw features for diabetes: {features}")
        
        # Make prediction
        result = model_manager.predict(request.disease, features)
        logger.info(f"Prediction successful. Ensemble score: {result.get('ensemble', 0)}")
        
        return PredictionResponse(
            ensemble=result.get('ensemble', 0),
            rf=result.get('rf'),
            svm=result.get('svm'),
            nn=result.get('nn'),
            confidence=result.get('confidence', 90.0),
            feature_importance=result.get('feature_importance', {})
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        import traceback
        error_detail = f"Prediction error: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@router.get("/diseases")
async def get_diseases():
    """Get list of available disease types"""
    return {
        "diseases": ["diabetes", "heart", "stroke", "liver", "kidney"],
        "available_models": list(model_manager.models.keys())
    }

