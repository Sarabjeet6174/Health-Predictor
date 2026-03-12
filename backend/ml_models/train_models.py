"""
ML Model Training Scripts
Trains models for different diseases using scikit-learn
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_data(disease: str, n_samples: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic training data for diseases
    In production, you would load real datasets from the data/ directory
    """
    np.random.seed(42)
    
    if disease == 'diabetes':
        data = {
            'pregnancies': np.random.randint(0, 20, n_samples),
            'glucose': np.random.normal(120, 30, n_samples).clip(0, 300),
            'bloodPressure': np.random.normal(70, 15, n_samples).clip(0, 200),
            'skinThickness': np.random.normal(25, 10, n_samples).clip(0, 100),
            'insulin': np.random.normal(100, 100, n_samples).clip(0, 900),
            'bmi': np.random.normal(30, 7, n_samples).clip(10, 70),
            'diabetesPedigreeFunction': np.random.normal(0.5, 0.2, n_samples).clip(0, 2),
            'age': np.random.randint(20, 80, n_samples)
        }
        # Create target based on glucose and BMI
        target = ((data['glucose'] > 140) | (data['bmi'] > 30)).astype(int)
        
    elif disease == 'heart':
        data = {
            'age': np.random.randint(20, 100, n_samples),
            'sex': np.random.randint(0, 2, n_samples),
            'cp': np.random.randint(0, 4, n_samples),
            'trestbps': np.random.normal(130, 20, n_samples).clip(80, 200),
            'chol': np.random.normal(250, 50, n_samples).clip(100, 600),
            'fbs': np.random.randint(0, 2, n_samples),
            'restecg': np.random.randint(0, 3, n_samples),
            'thalach': np.random.normal(150, 25, n_samples).clip(60, 220),
            'exang': np.random.randint(0, 2, n_samples),
            'oldpeak': np.random.normal(1, 1.5, n_samples).clip(0, 6),
            'slope': np.random.randint(0, 3, n_samples),
            'ca': np.random.randint(0, 4, n_samples),
            'thal': np.random.randint(0, 3, n_samples)
        }
        # Create target based on age, cholesterol, and blood pressure
        target = ((data['age'] > 55) | (data['chol'] > 240) | (data['trestbps'] > 140)).astype(int)
        
    elif disease == 'stroke':
        data = {
            'age': np.random.randint(18, 100, n_samples),
            'hypertension': np.random.randint(0, 2, n_samples),
            'heart_disease': np.random.randint(0, 2, n_samples),
            'avg_glucose': np.random.normal(100, 30, n_samples).clip(50, 300),
            'bmi': np.random.normal(25, 5, n_samples).clip(10, 60),
            'smoking_status': np.random.randint(0, 4, n_samples)
        }
        target = ((data['age'] > 65) | (data['hypertension'] == 1) | (data['heart_disease'] == 1)).astype(int)
        
    elif disease == 'liver':
        data = {
            'age': np.random.randint(1, 100, n_samples),
            'gender': np.random.randint(0, 2, n_samples),
            'tot_bilirubin': np.random.normal(1, 0.5, n_samples).clip(0.1, 80),
            'direct_bilirubin': np.random.normal(0.3, 0.2, n_samples).clip(0.1, 20),
            'alkphos': np.random.normal(200, 100, n_samples).clip(20, 1000),
            'sgpt': np.random.normal(40, 30, n_samples).clip(10, 500),
            'sgot': np.random.normal(35, 25, n_samples).clip(10, 500),
            'tot_proteins': np.random.normal(7, 1, n_samples).clip(3, 10),
            'albumin': np.random.normal(4, 0.5, n_samples).clip(2, 6),
            'ag_ratio': np.random.normal(1.2, 0.3, n_samples).clip(0.5, 2)
        }
        target = ((data['tot_bilirubin'] > 1.2) | (data['sgpt'] > 56)).astype(int)
        
    elif disease == 'kidney':
        data = {
            'age': np.random.randint(2, 100, n_samples),
            'bp': np.random.normal(80, 15, n_samples).clip(50, 200),
            'sg': np.random.normal(1.015, 0.005, n_samples).clip(1.0, 1.05),
            'albumin': np.random.randint(0, 6, n_samples),
            'sugar': np.random.randint(0, 6, n_samples),
            'rbc': np.random.randint(0, 2, n_samples),
            'pc': np.random.randint(0, 2, n_samples),
            'pcc': np.random.randint(0, 2, n_samples),
            'ba': np.random.randint(0, 2, n_samples),
            'bgr': np.random.normal(120, 40, n_samples).clip(50, 500),
            'bu': np.random.normal(30, 15, n_samples).clip(10, 200),
            'sc': np.random.normal(1.2, 0.5, n_samples).clip(0.5, 5),
            'sod': np.random.normal(140, 10, n_samples).clip(100, 200),
            'pot': np.random.normal(4.5, 1, n_samples).clip(2, 10),
            'hemo': np.random.normal(14, 3, n_samples).clip(5, 20),
            'pcv': np.random.normal(45, 8, n_samples).clip(20, 70),
            'wc': np.random.normal(8000, 2000, n_samples).clip(2000, 20000),
            'rc': np.random.normal(5, 1, n_samples).clip(2, 8),
            'htn': np.random.randint(0, 2, n_samples),
            'dm': np.random.randint(0, 2, n_samples),
            'cad': np.random.randint(0, 2, n_samples),
            'appet': np.random.randint(0, 2, n_samples),
            'pe': np.random.randint(0, 2, n_samples),
            'ane': np.random.randint(0, 2, n_samples)
        }
        target = ((data['sg'] < 1.010) | (data['albumin'] > 2) | (data['sc'] > 1.5)).astype(int)
        
    else:
        raise ValueError(f"Unknown disease type: {disease}")
    
    df = pd.DataFrame(data)
    df['target'] = target
    
    return df

def train_disease_model(disease: str, dataset_path: Optional[str] = None):
    """
    Train ML models for a specific disease
    
    Args:
        disease: Disease type (diabetes, heart, stroke, liver, kidney)
        dataset_path: Optional path to CSV dataset file
    """
    logger.info(f"Starting training for {disease} model...")
    
    # Load or generate data
    if dataset_path and os.path.exists(dataset_path):
        logger.info(f"Loading dataset from {dataset_path}")
        df = pd.read_csv(dataset_path)
    else:
        logger.info(f"Generating synthetic data for {disease}")
        df = generate_synthetic_data(disease, n_samples=1000)
    
    # Prepare features and target
    if 'target' in df.columns:
        X = df.drop('target', axis=1)
        y = df['target']
    else:
        raise ValueError("Dataset must have a 'target' column")
    
    # Get feature names
    feature_order = list(X.columns)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train multiple models
    models = {}
    accuracies = {}
    
    # Random Forest
    logger.info("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf.fit(X_train_scaled, y_train)
    rf_pred = rf.predict(X_test_scaled)
    rf_acc = accuracy_score(y_test, rf_pred)
    models['random_forest'] = rf
    accuracies['random_forest'] = rf_acc
    logger.info(f"Random Forest Accuracy: {rf_acc:.4f}")
    
    # SVM
    logger.info("Training SVM...")
    svm = SVC(probability=True, random_state=42, kernel='rbf')
    svm.fit(X_train_scaled, y_train)
    svm_pred = svm.predict(X_test_scaled)
    svm_acc = accuracy_score(y_test, svm_pred)
    models['svm'] = svm
    accuracies['svm'] = svm_acc
    logger.info(f"SVM Accuracy: {svm_acc:.4f}")
    
    # Neural Network
    logger.info("Training Neural Network...")
    nn = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    nn.fit(X_train_scaled, y_train)
    nn_pred = nn.predict(X_test_scaled)
    nn_acc = accuracy_score(y_test, nn_pred)
    models['neural_network'] = nn
    accuracies['neural_network'] = nn_acc
    logger.info(f"Neural Network Accuracy: {nn_acc:.4f}")
    
    # Calculate ensemble accuracy
    ensemble_pred = (rf_pred + svm_pred + nn_pred) / 3
    ensemble_pred_binary = (ensemble_pred > 0.5).astype(int)
    ensemble_acc = accuracy_score(y_test, ensemble_pred_binary)
    logger.info(f"Ensemble Accuracy: {ensemble_acc:.4f}")
    
    # Save models - use project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    models_dir = os.path.join(project_root, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_data = {
        'random_forest': rf,
        'svm': svm,
        'neural_network': nn,
        'feature_order': feature_order,
        'accuracy': {
            'random_forest': float(rf_acc),
            'svm': float(svm_acc),
            'neural_network': float(nn_acc),
            'ensemble': float(ensemble_acc)
        }
    }
    
    model_path = os.path.join(models_dir, f"{disease}_model.pkl")
    scaler_path = os.path.join(models_dir, f"{disease}_scaler.pkl")
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    logger.info(f"Models saved to {model_path}")
    logger.info(f"Training completed for {disease} model")
    
    return {
        'disease': disease,
        'accuracy': ensemble_acc,
        'model_path': model_path
    }

if __name__ == "__main__":
    # Train all models
    diseases = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
    for disease in diseases:
        train_disease_model(disease)

