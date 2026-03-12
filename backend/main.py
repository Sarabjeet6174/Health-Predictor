"""
FastAPI Backend for Health Predictor
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ml_models.model_manager import ModelManager
from backend.api import predictions, training, models

app = FastAPI(
    title="MedPredict AI API",
    description="Machine Learning API for Health Risk Predictions",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(training.router, prefix="/api/training", tags=["Training"])
app.include_router(models.router, prefix="/api/models", tags=["Models"])

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "MedPredict AI API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

