"""
Standalone script to train all ML models
Run this script to train all disease prediction models
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.ml_models.train_models import train_disease_model

def main():
    """Train all disease models"""
    diseases = ['diabetes', 'heart', 'stroke', 'liver', 'kidney']
    
    print("=" * 60)
    print("Health Predictor - ML Model Training")
    print("=" * 60)
    print()
    
    for i, disease in enumerate(diseases, 1):
        print(f"[{i}/{len(diseases)}] Training {disease} model...")
        try:
            result = train_disease_model(disease)
            print(f"✓ {disease} model trained successfully!")
            print(f"  Accuracy: {result['accuracy']:.4f}")
            print()
        except Exception as e:
            print(f"✗ Error training {disease} model: {str(e)}")
            print()
    
    print("=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("\nModels saved in the 'models/' directory")
    print("You can now start the FastAPI server with: python -m uvicorn backend.main:app --reload")

if __name__ == "__main__":
    main()

