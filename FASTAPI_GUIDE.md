# FastAPI Backend Guide

## Why FastAPI?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python. It's perfect for ML applications because:

1. **Fast**: Built on Starlette and Pydantic, it's one of the fastest Python frameworks
2. **Easy to Use**: Simple syntax, automatic API documentation
3. **Type Safety**: Uses Python type hints for validation
4. **Async Support**: Built-in support for async/await
5. **Auto Documentation**: Interactive API docs at `/docs` endpoint

## Project Architecture

### Backend Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── api/
│   ├── predictions.py     # Prediction endpoints
│   ├── training.py        # Model training endpoints
│   └── models.py          # Model management endpoints
└── ml_models/
    ├── model_manager.py   # Model loading/prediction logic
    └── train_models.py    # ML training scripts
```

## Key Components Explained

### 1. Main Application (`backend/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MedPredict AI API")

# CORS middleware allows frontend to make requests
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Include API routers
app.include_router(predictions.router, prefix="/api/predictions")
```

**Key Features:**
- Creates the FastAPI application instance
- Configures CORS for frontend communication
- Includes all API route modules
- Provides health check endpoints

### 2. Prediction Endpoints (`backend/api/predictions.py`)

```python
@router.post("/predict")
async def predict(request: PredictionRequest):
    result = model_manager.predict(request.disease, request.features)
    return PredictionResponse(...)
```

**What it does:**
- Receives prediction requests from frontend
- Validates input using Pydantic models
- Calls model manager to make predictions
- Returns structured JSON response

### 3. Training Endpoints (`backend/api/training.py`)

```python
@router.post("/train")
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(train_disease_model, request.disease)
    return {"status": "training"}
```

**Key Features:**
- Accepts training requests
- Runs training in background (non-blocking)
- Returns immediate response while training continues

### 4. Model Manager (`backend/ml_models/model_manager.py`)

```python
class ModelManager:
    def predict(self, disease: str, features: Dict) -> Dict:
        # Load model
        # Preprocess features
        # Make prediction
        # Return results
```

**Responsibilities:**
- Loads trained models from disk
- Preprocesses input features
- Runs predictions through ensemble models
- Returns formatted results

## API Request/Response Flow

### Making a Prediction

1. **Frontend sends request:**
```javascript
fetch('http://localhost:8000/api/predictions/predict', {
  method: 'POST',
  body: JSON.stringify({
    disease: 'diabetes',
    features: { glucose: 148, bmi: 33.6, ... }
  })
})
```

2. **FastAPI receives and validates:**
```python
class PredictionRequest(BaseModel):
    disease: str
    features: Dict[str, Any]
```

3. **Model Manager processes:**
```python
model_manager.predict('diabetes', features)
```

4. **Response sent back:**
```json
{
  "ensemble": 75.5,
  "rf": 72.3,
  "svm": 78.1,
  "nn": 76.2,
  "confidence": 92.0,
  "feature_importance": {...}
}
```

## Training Models with FastAPI

### Option 1: Via API Endpoint

```bash
# Train a specific model
curl -X POST "http://localhost:8000/api/training/train" \
  -H "Content-Type: application/json" \
  -d '{"disease": "diabetes"}'

# Train all models
curl -X POST "http://localhost:8000/api/training/train-all"
```

### Option 2: Direct Python Script

```python
from backend.ml_models.train_models import train_disease_model

# Train diabetes model
train_disease_model('diabetes')

# Train with custom dataset
train_disease_model('diabetes', 'data/my_dataset.csv')
```

### Option 3: Standalone Script

```bash
python train_all_models.py
```

## Model Training Process

1. **Data Loading:**
   - Loads CSV from `data/` directory OR
   - Generates synthetic data if no dataset provided

2. **Preprocessing:**
   - Splits into train/test sets
   - Scales features using StandardScaler
   - Handles missing values

3. **Model Training:**
   - Trains Random Forest (100 trees)
   - Trains SVM (RBF kernel)
   - Trains Neural Network (2 hidden layers)

4. **Evaluation:**
   - Calculates accuracy for each model
   - Computes ensemble accuracy
   - Saves metrics

5. **Model Saving:**
   - Saves models as pickle files
   - Saves scaler for preprocessing
   - Stores feature order and metadata

## Adding New Endpoints

### Example: Add a Statistics Endpoint

1. **Create endpoint in `backend/api/predictions.py`:**

```python
@router.get("/stats")
async def get_prediction_stats():
    return {
        "total_predictions": 1000,
        "avg_risk": 45.2,
        "diseases": ["diabetes", "heart", ...]
    }
```

2. **The endpoint is automatically available at:**
   - `GET /api/predictions/stats`
   - Documented at `http://localhost:8000/docs`

## Error Handling

FastAPI automatically handles:
- **Validation errors**: Invalid input types
- **404 errors**: Non-existent endpoints
- **500 errors**: Server-side exceptions

Example error response:
```json
{
  "detail": "Model for diabetes not found. Please train the model first."
}
```

## Testing the API

### Using the Interactive Docs

1. Start the server: `python start_server.py`
2. Open: http://localhost:8000/docs
3. Click "Try it out" on any endpoint
4. Fill in parameters and click "Execute"

### Using curl

```bash
# Health check
curl http://localhost:8000/api/health

# List models
curl http://localhost:8000/api/models/list

# Make prediction
curl -X POST "http://localhost:8000/api/predictions/predict" \
  -H "Content-Type: application/json" \
  -d '{"disease": "diabetes", "features": {...}}'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/predictions/predict",
    json={
        "disease": "diabetes",
        "features": {
            "glucose": 148,
            "bmi": 33.6,
            # ... other features
        }
    }
)
print(response.json())
```

## Deployment Considerations

### Production Settings

1. **CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
)
```

2. **Environment Variables:**
```python
import os
API_PORT = int(os.getenv("PORT", 8000))
```

3. **Error Logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Deployment Options

- **Heroku**: Add `Procfile` with `web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **AWS Lambda**: Use Mangum adapter
- **Docker**: Create Dockerfile with uvicorn
- **DigitalOcean**: Use App Platform

## Performance Tips

1. **Model Loading**: Models are loaded once at startup (in ModelManager)
2. **Async Operations**: Use `async def` for I/O-bound operations
3. **Caching**: Consider caching predictions for repeated inputs
4. **Background Tasks**: Use for long-running operations (training)

## Common Patterns

### Background Tasks
```python
from fastapi import BackgroundTasks

@router.post("/train")
async def train(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_function)
    return {"status": "started"}
```

### Dependency Injection
```python
from fastapi import Depends

def get_model_manager():
    return model_manager

@router.get("/predict")
async def predict(manager: ModelManager = Depends(get_model_manager)):
    return manager.predict(...)
```

## Next Steps

1. **Add Authentication**: Implement JWT tokens
2. **Add Database**: Store predictions in PostgreSQL/MongoDB
3. **Add Caching**: Use Redis for model caching
4. **Add Monitoring**: Integrate with Prometheus/Grafana
5. **Add Tests**: Write unit tests with pytest

---

**FastAPI makes it easy to build production-ready ML APIs! 🚀**

