"""
Training API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.ml_models.train_models import train_disease_model

router = APIRouter()

class TrainingRequest(BaseModel):
    disease: str
    dataset_path: Optional[str] = None

class TrainingResponse(BaseModel):
    message: str
    disease: str
    status: str

@router.post("/train", response_model=TrainingResponse)
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Train a model for a specific disease
    
    Args:
        request: TrainingRequest with disease type and optional dataset path
        background_tasks: FastAPI background tasks
        
    Returns:
        TrainingResponse with training status
    """
    valid_diseases = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
    
    if request.disease not in valid_diseases:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid disease type. Must be one of: {valid_diseases}"
        )
    
    # Add training task to background
    background_tasks.add_task(train_disease_model, request.disease, request.dataset_path)
    
    return TrainingResponse(
        message=f"Training started for {request.disease} model",
        disease=request.disease,
        status="training"
    )

@router.post("/train-all")
async def train_all_models(background_tasks: BackgroundTasks):
    """
    Train all disease models
    
    Args:
        background_tasks: FastAPI background tasks
        
    Returns:
        Response with training status
    """
    diseases = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
    
    for disease in diseases:
        background_tasks.add_task(train_disease_model, disease, None)
    
    return {
        "message": "Training started for all models",
        "diseases": diseases,
        "status": "training"
    }

@router.get("/status/{disease}")
async def get_training_status(disease: str):
    """
    Get training status for a disease model
    
    Args:
        disease: Disease type
        
    Returns:
        Training status information
    """
    # Check if model exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    model_path = os.path.join(project_root, "models", f"{disease}_model.pkl")
    
    if os.path.exists(model_path):
        return {
            "disease": disease,
            "status": "trained",
            "model_exists": True
        }
    else:
        return {
            "disease": disease,
            "status": "not_trained",
            "model_exists": False
        }

