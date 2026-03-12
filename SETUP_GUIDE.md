# Setup Guide - MedPredict AI

## Step-by-Step Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- scikit-learn (machine learning)
- pandas (data processing)
- numpy (numerical computing)

### Step 2: Train the ML Models

Before you can make predictions, you need to train the models:

```bash
python train_all_models.py
```

This will:
- Generate synthetic training data for each disease
- Train Random Forest, SVM, and Neural Network models
- Save trained models to the `models/` directory
- Display accuracy metrics for each model

**Note:** Training takes a few minutes. You'll see progress for each disease type.

### Step 3: Start the Backend Server

Open a new terminal window and run:

```bash
python start_server.py
```

Or alternatively:

```bash
uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The API is now running! You can:
- Access the API at: http://localhost:8000
- View API documentation at: http://localhost:8000/docs
- Test endpoints at: http://localhost:8000/redoc

### Step 4: Open the Frontend

**Option A: Direct file open**
- Navigate to `frontend/index.html`
- Open it in your web browser (Chrome, Firefox, Edge, etc.)

**Option B: Local web server (recommended)**
```bash
cd frontend
python -m http.server 8080
```
Then open: http://localhost:8080

### Step 5: Test the System

1. Open the frontend in your browser
2. Select a disease type (e.g., "Diabetes Risk")
3. Fill in the health parameters
4. Click "Run ML Prediction"
5. View the prediction results!

## Using Your Own Training Data

### Prepare Your Dataset

1. Create a CSV file with your data
2. Ensure it has:
   - Feature columns (health parameters)
   - A `target` column (0 = no disease, 1 = disease)
3. Place it in the `data/` directory

### Train with Custom Data

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/training/train" \
  -H "Content-Type: application/json" \
  -d '{"disease": "diabetes", "dataset_path": "data/my_diabetes_data.csv"}'
```

**Via Python:**
```python
from backend.ml_models.train_models import train_disease_model
train_disease_model('diabetes', 'data/my_diabetes_data.csv')
```

## API Usage Examples

### Make a Prediction

```bash
curl -X POST "http://localhost:8000/api/predictions/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "diabetes",
    "features": {
      "pregnancies": 2,
      "glucose": 148,
      "bloodPressure": 72,
      "skinThickness": 35,
      "insulin": 0,
      "bmi": 33.6
    }
  }'
```

### Check Available Models

```bash
curl http://localhost:8000/api/models/list
```

### Get Model Information

```bash
curl http://localhost:8000/api/models/info/diabetes
```

## Troubleshooting

### "Models not found" Error

**Solution:** Run `python train_all_models.py` to train all models first.

### CORS Errors in Browser

**Solution:** The backend already has CORS enabled. Make sure:
1. Backend is running on port 8000
2. Frontend is trying to connect to `http://localhost:8000`

### Port Already in Use

**Solution:** 
- Stop the process using port 8000, or
- Change the port in `start_server.py` or `backend/main.py`

### Import Errors

**Solution:** Make sure you're running commands from the project root directory.

### Models Not Loading

**Solution:** 
1. Check that `models/` directory exists
2. Verify model files (`*_model.pkl`) are present
3. Re-train models if needed

## Project Structure Overview

```
Health-Predictor/
├── frontend/
│   └── index.html          # Web interface
├── backend/
│   ├── main.py             # FastAPI app
│   ├── api/                # API endpoints
│   └── ml_models/          # ML training code
├── models/                 # Trained models (created after training)
├── data/                   # Your datasets (optional)
├── train_all_models.py     # Training script
├── start_server.py         # Server startup script
└── requirements.txt       # Dependencies
```

## Next Steps

1. **Customize Models:** Edit `backend/ml_models/train_models.py` to adjust model parameters
2. **Add Features:** Modify disease configurations in `frontend/index.html`
3. **Improve UI:** Customize the frontend styling and layout
4. **Add Authentication:** Implement user authentication in the backend
5. **Deploy:** Deploy to cloud services (Heroku, AWS, etc.)

## Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all dependencies are installed
3. Ensure models are trained before making predictions
4. Check that the backend server is running

---

**Happy Predicting! 🎉**

