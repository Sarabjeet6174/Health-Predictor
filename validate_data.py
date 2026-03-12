"""
Data Validation Script
Use this to validate your CSV data before training models
"""

import pandas as pd
import sys
import os

# Expected columns for each disease
EXPECTED_COLUMNS = {
    'diabetes': ['pregnancies', 'glucose', 'bloodPressure', 'skinThickness', 
                 'insulin', 'bmi', 'diabetesPedigreeFunction', 'age', 'target'],
    'heart': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
              'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'],
    'stroke': ['age', 'hypertension', 'heart_disease', 'avg_glucose', 'bmi', 
               'smoking_status', 'target'],
    'liver': ['age', 'gender', 'tot_bilirubin', 'direct_bilirubin', 'alkphos',
              'sgpt', 'sgot', 'tot_proteins', 'albumin', 'ag_ratio', 'target'],
    'kidney': ['age', 'bp', 'sg', 'albumin', 'sugar', 'rbc', 'pc', 'pcc', 'ba',
               'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc',
               'htn', 'dm', 'cad', 'appet', 'pe', 'ane', 'target']
}

def validate_dataset(file_path: str, disease: str):
    """
    Validate a dataset for a specific disease
    
    Args:
        file_path: Path to CSV file
        disease: Disease type (diabetes, heart, stroke, liver, kidney)
    """
    print("=" * 60)
    print(f"Validating {disease} dataset: {file_path}")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        return False
    
    # Load data
    try:
        df = pd.read_csv(file_path)
        print(f"✓ File loaded successfully")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
    except Exception as e:
        print(f"❌ ERROR: Could not read CSV file: {str(e)}")
        return False
    
    # Check for target column
    if 'target' not in df.columns:
        print("❌ ERROR: Missing 'target' column")
        print("  Your CSV must have a 'target' column with values 0 or 1")
        return False
    else:
        print("✓ Target column found")
    
    # Check target values
    target_values = df['target'].unique()
    if not all(val in [0, 1] for val in target_values):
        print(f"❌ ERROR: Target column contains invalid values: {target_values}")
        print("  Target must only contain 0 (no disease) or 1 (disease)")
        return False
    else:
        print(f"✓ Target values are valid: {target_values}")
        print(f"  Distribution: {df['target'].value_counts().to_dict()}")
    
    # Check expected columns
    if disease not in EXPECTED_COLUMNS:
        print(f"❌ ERROR: Unknown disease type: {disease}")
        print(f"  Valid types: {list(EXPECTED_COLUMNS.keys())}")
        return False
    
    expected = set(EXPECTED_COLUMNS[disease])
    actual = set(df.columns)
    
    missing = expected - actual
    extra = actual - expected
    
    if missing:
        print(f"❌ ERROR: Missing required columns: {list(missing)}")
        return False
    
    if extra:
        print(f"⚠ WARNING: Extra columns found (will be ignored): {list(extra)}")
    
    print(f"✓ All required columns present: {list(expected)}")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print(f"⚠ WARNING: Missing values found:")
        for col, count in missing_values[missing_values > 0].items():
            print(f"  {col}: {count} missing values")
        print("  Consider filling missing values before training")
    else:
        print("✓ No missing values found")
    
    # Check data types
    print("\nData types:")
    for col in EXPECTED_COLUMNS[disease]:
        if col in df.columns:
            print(f"  {col}: {df[col].dtype}")
    
    # Check value ranges
    print("\nValue ranges:")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        if col != 'target':
            print(f"  {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")
    
    print("\n" + "=" * 60)
    print("✓ Dataset is valid and ready for training!")
    print("=" * 60)
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_data.py <disease_type> <csv_file_path>")
        print("\nExample:")
        print("  python validate_data.py diabetes data/diabetes_data.csv")
        print("\nValid disease types:")
        for disease in EXPECTED_COLUMNS.keys():
            print(f"  - {disease}")
        sys.exit(1)
    
    disease = sys.argv[1].lower()
    file_path = sys.argv[2]
    
    if validate_dataset(file_path, disease):
        print("\n✅ Validation passed! You can now train the model with:")
        print(f"   from backend.ml_models.train_models import train_disease_model")
        print(f"   train_disease_model('{disease}', '{file_path}')")
    else:
        print("\n❌ Validation failed! Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

