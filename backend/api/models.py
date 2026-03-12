"""
Model information API endpoints
"""

from fastapi import APIRouter, HTTPException
from backend.ml_models.model_manager import model_manager

router = APIRouter()

@router.get("/info/{disease}")
async def get_model_info(disease: str):
    """
    Get information about a trained model
    
    Args:
        disease: Disease type
        
    Returns:
        Model information
    """
    info = model_manager.get_model_info(disease)
    
    if info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Model for {disease} not found. Please train the model first."
        )
    
    return info

@router.get("/list")
async def list_models():
    """
    List all available models
    
    Returns:
        List of available models
    """
    models_info = {}
    
    for disease in ['diabetes', 'heart', 'stroke', 'liver', 'kidney']:
        info = model_manager.get_model_info(disease)
        models_info[disease] = info if info else {"trained": False}
    
    return {
        "models": models_info,
        "total_trained": sum(1 for m in models_info.values() if m.get('trained', False))
    }

@router.post("/reload/{disease}")
async def reload_model(disease: str):
    """
    Reload a specific model
    
    Args:
        disease: Disease type
        
    Returns:
        Reload status
    """
    try:
        model_manager.reload_model(disease)
        return {
            "message": f"Model for {disease} reloaded successfully",
            "disease": disease,
            "status": "success"
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading model: {str(e)}")

