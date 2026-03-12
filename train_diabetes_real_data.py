"""
Train Diabetes Model with Real Dataset
Uses the actual diabetes_prediction_dataset.csv file
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_diabetes_with_real_data(dataset_path='diabetes_prediction_dataset.csv'):
    """
    Train diabetes model using the real dataset
    
    Args:
        dataset_path: Path to the CSV file
    """
    logger.info("=" * 60)
    logger.info("Training Diabetes Model with Real Dataset")
    logger.info("=" * 60)
    
    # Load dataset
    logger.info(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    # Check target distribution
    target_dist = df['diabetes'].value_counts()
    logger.info(f"\nTarget distribution:\n{target_dist}")
    logger.info(f"Diabetes rate: {target_dist[1] / len(df) * 100:.2f}%")
    
    # Prepare features
    # Handle categorical variables
    le_gender = LabelEncoder()
    le_smoking = LabelEncoder()
    
    # Create a copy for processing
    df_processed = df.copy()
    
    # Encode gender (Male=1, Female=0)
    df_processed['gender_encoded'] = le_gender.fit_transform(df_processed['gender'])
    
    # Encode smoking history
    df_processed['smoking_encoded'] = le_smoking.fit_transform(df_processed['smoking_history'])
    
    # Select features (excluding original categorical columns)
    feature_columns = [
        'gender_encoded',
        'age',
        'hypertension',
        'heart_disease',
        'smoking_encoded',
        'bmi',
        'HbA1c_level',
        'blood_glucose_level'
    ]
    
    X = df_processed[feature_columns]
    y = df_processed['diabetes']
    
    logger.info(f"\nFeatures used: {feature_columns}")
    logger.info(f"Feature matrix shape: {X.shape}")
    
    # Split data
    logger.info("\nSplitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Training set: {X_train.shape[0]} samples")
    logger.info(f"Test set: {X_test.shape[0]} samples")
    
    # Scale features
    logger.info("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    models = {}
    results = {}
    
    # Random Forest
    logger.info("\n" + "=" * 60)
    logger.info("Training Random Forest...")
    logger.info("=" * 60)
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle imbalanced dataset
    )
    rf.fit(X_train_scaled, y_train)
    rf_pred = rf.predict(X_test_scaled)
    rf_proba = rf.predict_proba(X_test_scaled)
    
    rf_acc = accuracy_score(y_test, rf_pred)
    rf_prec = precision_score(y_test, rf_pred)
    rf_rec = recall_score(y_test, rf_pred)
    rf_f1 = f1_score(y_test, rf_pred)
    
    models['random_forest'] = rf
    results['random_forest'] = {
        'accuracy': rf_acc,
        'precision': rf_prec,
        'recall': rf_rec,
        'f1': rf_f1
    }
    
    logger.info(f"Random Forest Results:")
    logger.info(f"  Accuracy:  {rf_acc:.4f}")
    logger.info(f"  Precision: {rf_prec:.4f}")
    logger.info(f"  Recall:    {rf_rec:.4f}")
    logger.info(f"  F1-Score:  {rf_f1:.4f}")
    
    # SVM
    logger.info("\n" + "=" * 60)
    logger.info("Training SVM...")
    logger.info("=" * 60)
    svm = SVC(
        probability=True,
        random_state=42,
        kernel='rbf',
        C=1.0,
        gamma='scale',
        class_weight='balanced'
    )
    svm.fit(X_train_scaled, y_train)
    svm_pred = svm.predict(X_test_scaled)
    svm_proba = svm.predict_proba(X_test_scaled)
    
    svm_acc = accuracy_score(y_test, svm_pred)
    svm_prec = precision_score(y_test, svm_pred)
    svm_rec = recall_score(y_test, svm_pred)
    svm_f1 = f1_score(y_test, svm_pred)
    
    models['svm'] = svm
    results['svm'] = {
        'accuracy': svm_acc,
        'precision': svm_prec,
        'recall': svm_rec,
        'f1': svm_f1
    }
    
    logger.info(f"SVM Results:")
    logger.info(f"  Accuracy:  {svm_acc:.4f}")
    logger.info(f"  Precision: {svm_prec:.4f}")
    logger.info(f"  Recall:    {svm_rec:.4f}")
    logger.info(f"  F1-Score:  {svm_f1:.4f}")
    
    # Neural Network
    logger.info("\n" + "=" * 60)
    logger.info("Training Neural Network...")
    logger.info("=" * 60)
    nn = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        max_iter=500,
        random_state=42,
        learning_rate='adaptive',
        early_stopping=True,
        validation_fraction=0.1
    )
    nn.fit(X_train_scaled, y_train)
    nn_pred = nn.predict(X_test_scaled)
    nn_proba = nn.predict_proba(X_test_scaled)
    
    nn_acc = accuracy_score(y_test, nn_pred)
    nn_prec = precision_score(y_test, nn_pred)
    nn_rec = recall_score(y_test, nn_pred)
    nn_f1 = f1_score(y_test, nn_pred)
    
    models['neural_network'] = nn
    results['neural_network'] = {
        'accuracy': nn_acc,
        'precision': nn_prec,
        'recall': nn_rec,
        'f1': nn_f1
    }
    
    logger.info(f"Neural Network Results:")
    logger.info(f"  Accuracy:  {nn_acc:.4f}")
    logger.info(f"  Precision: {nn_prec:.4f}")
    logger.info(f"  Recall:    {nn_rec:.4f}")
    logger.info(f"  F1-Score:  {nn_f1:.4f}")
    
    # Ensemble prediction
    logger.info("\n" + "=" * 60)
    logger.info("Calculating Ensemble Performance...")
    logger.info("=" * 60)
    
    # Weighted ensemble (based on F1 scores)
    weights = {
        'random_forest': results['random_forest']['f1'],
        'svm': results['svm']['f1'],
        'neural_network': results['neural_network']['f1']
    }
    total_weight = sum(weights.values())
    weights = {k: v/total_weight for k, v in weights.items()}
    
    logger.info(f"Ensemble weights: {weights}")
    
    # Ensemble prediction
    ensemble_proba = (
        weights['random_forest'] * rf_proba[:, 1] +
        weights['svm'] * svm_proba[:, 1] +
        weights['neural_network'] * nn_proba[:, 1]
    )
    ensemble_pred = (ensemble_proba > 0.5).astype(int)
    
    ensemble_acc = accuracy_score(y_test, ensemble_pred)
    ensemble_prec = precision_score(y_test, ensemble_pred)
    ensemble_rec = recall_score(y_test, ensemble_pred)
    ensemble_f1 = f1_score(y_test, ensemble_pred)
    
    results['ensemble'] = {
        'accuracy': ensemble_acc,
        'precision': ensemble_prec,
        'recall': ensemble_rec,
        'f1': ensemble_f1
    }
    
    logger.info(f"Ensemble Results:")
    logger.info(f"  Accuracy:  {ensemble_acc:.4f}")
    logger.info(f"  Precision: {ensemble_prec:.4f}")
    logger.info(f"  Recall:    {ensemble_rec:.4f}")
    logger.info(f"  F1-Score:  {ensemble_f1:.4f}")
    
    # Save models
    logger.info("\n" + "=" * 60)
    logger.info("Saving Models...")
    logger.info("=" * 60)
    
    os.makedirs("models", exist_ok=True)
    
    # Prepare model data
    model_data = {
        'random_forest': rf,
        'svm': svm,
        'neural_network': nn,
        'feature_order': feature_columns,
        'label_encoders': {
            'gender': le_gender,
            'smoking': le_smoking
        },
        'accuracy': {
            'random_forest': float(rf_acc),
            'svm': float(svm_acc),
            'neural_network': float(nn_acc),
            'ensemble': float(ensemble_acc)
        },
        'metrics': results,
        'ensemble_weights': weights,
        'dataset_info': {
            'total_samples': len(df),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'diabetes_rate': float(target_dist[1] / len(df))
        }
    }
    
    model_path = os.path.join("models", "diabetes_model.pkl")
    scaler_path = os.path.join("models", "diabetes_scaler.pkl")
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    logger.info(f"✓ Models saved to {model_path}")
    logger.info(f"✓ Scaler saved to {scaler_path}")
    
    # Print classification report
    logger.info("\n" + "=" * 60)
    logger.info("Detailed Classification Report (Ensemble):")
    logger.info("=" * 60)
    print(classification_report(y_test, ensemble_pred, target_names=['No Diabetes', 'Diabetes']))
    
    logger.info("\n" + "=" * 60)
    logger.info("Training Complete!")
    logger.info("=" * 60)
    
    return {
        'model_path': model_path,
        'scaler_path': scaler_path,
        'results': results,
        'feature_order': feature_columns
    }

if __name__ == "__main__":
    import sys
    
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else 'diabetes_prediction_dataset.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset file not found: {dataset_path}")
        print("Please provide the correct path to your diabetes dataset CSV file.")
        sys.exit(1)
    
    result = train_diabetes_with_real_data(dataset_path)
    print("\n✅ Model training completed successfully!")
    print(f"📊 Best model accuracy: {result['results']['ensemble']['accuracy']:.4f}")

