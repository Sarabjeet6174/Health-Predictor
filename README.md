# MedPredict AI - Health Risk Prediction System

A comprehensive machine learning-based health risk prediction system with a modern web interface and FastAPI backend. Predicts risks for diabetes, heart disease, stroke, liver disease, and kidney disease using ensemble ML models (Random Forest, SVM, Neural Networks).

## 🏗️ Project Structure

```
Health-Predictor/
├── frontend/
│   └── index.html          # Frontend web interface
├── backend/
│   ├── main.py             # FastAPI application entry point
│   ├── api/
│   │   ├── predictions.py  # Prediction endpoints
│   │   ├── training.py     # Model training endpoints
│   │   └── models.py       # Model information endpoints
│   └── ml_models/
│       ├── model_manager.py    # Model loading and management
│       └── train_models.py      # ML model training scripts
├── models/                 # Trained model files (generated)
├── data/                   # Training datasets (optional)
├── train_all_models.py     # Standalone training script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train ML Models

Before using the prediction API, you need to train the models:

**Option A: Train all models at once**
```bash
python train_all_models.py
```

**Option B: Train models via API (after starting server)**
```bash
# Start the server first, then:
curl -X POST "http://localhost:8000/api/training/train-all"
```

**Option C: Train individual models**
```python
from backend.ml_models.train_models import train_disease_model
train_disease_model('diabetes')
```

### 3. Start the FastAPI Backend

```bash
# Using uvicorn directly
uvicorn backend.main:app --reload

# Or using Python
python -m uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Open the Frontend

Open `frontend/index.html` in your web browser, or serve it using a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

## 📡 API Endpoints

### Predictions

- **POST** `/api/predictions/predict` - Make a health risk prediction
  ```json
  {
    "disease": "diabetes",
    "features": {
      "pregnancies": 2,
      "glucose": 148,
      "bloodPressure": 72,
      "skinThickness": 35,
      "insulin": 0,
      "bmi": 33.6
    }
  }
  ```

- **GET** `/api/predictions/diseases` - Get list of available diseases

### Training

- **POST** `/api/training/train` - Train a specific disease model
  ```json
  {
    "disease": "diabetes",
    "dataset_path": "data/diabetes.csv"  // optional
  }
  ```

- **POST** `/api/training/train-all` - Train all disease models

- **GET** `/api/training/status/{disease}` - Get training status

### Models

- **GET** `/api/models/list` - List all available models
- **GET** `/api/models/info/{disease}` - Get model information
- **POST** `/api/models/reload/{disease}` - Reload a model

## 🤖 Machine Learning Models

The system uses ensemble learning with three algorithms:

1. **Random Forest** - Ensemble of decision trees (40% weight)
2. **Support Vector Machine (SVM)** - RBF kernel classifier (30% weight)
3. **Neural Network** - Multi-layer perceptron (30% weight)

Final predictions are weighted averages of all three models.

### Supported Diseases

1. **Diabetes** - 6 features (pregnancies, glucose, blood pressure, etc.)
2. **Heart Disease** - 5 features (age, cholesterol, blood pressure, etc.)
3. **Stroke** - 5 features (age, hypertension, glucose, BMI, etc.)
4. **Liver Disease** - 6 features (bilirubin, enzymes, proteins, etc.)
5. **Kidney Disease** - 6 features (blood pressure, albumin, glucose, etc.)

## 📊 Using Your Own Data

To train models with your own datasets:

1. Place CSV files in the `data/` directory
2. Ensure your CSV has a `target` column (0/1 for binary classification)
3. Train using the API:
   ```bash
   curl -X POST "http://localhost:8000/api/training/train" \
     -H "Content-Type: application/json" \
     -d '{"disease": "diabetes", "dataset_path": "data/your_data.csv"}'
   ```

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to:
- Change CORS settings (line 24)
- Modify port (line 40)
- Add authentication/authorization

### Frontend Configuration

Edit `frontend/index.html` to:
- Change API URL (line 780: `const API_BASE_URL`)
- Modify disease configurations (lines 510-604)

## 📝 Development

### Adding a New Disease Model

1. Add disease configuration in `frontend/index.html` (diseaseConfigs object)
2. Add feature mapping in `backend/ml_models/train_models.py`
3. Update feature order in model training script
4. Train the new model

### Model Architecture

Models are saved as pickle files containing:
- Trained model objects (Random Forest, SVM, Neural Network)
- Feature order (for input preprocessing)
- Accuracy metrics
- Scaler object (for feature normalization)

## 🐛 Troubleshooting

**Issue: Models not found**
- Solution: Run `python train_all_models.py` to train all models

**Issue: CORS errors in browser**
- Solution: Ensure backend is running and CORS is enabled in `backend/main.py`

**Issue: Import errors**
- Solution: Make sure you're running from the project root directory

**Issue: Port already in use**
- Solution: Change the port in `backend/main.py` or stop the process using port 8000

## 📦 Dependencies

- **FastAPI** - Modern web framework for APIs
- **Uvicorn** - ASGI server
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **pydantic** - Data validation

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Support

For questions or issues, please open an issue on the project repository.

---

**Built with ❤️ using FastAPI, scikit-learn, and modern web technologies**
