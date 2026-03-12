# Data Format Guide for Training Models

## Overview

Your training data must be in **CSV format** with:
- **Feature columns**: Health parameters/measurements
- **Target column**: Binary classification (0 = no disease, 1 = disease)

## General Format

```csv
feature1,feature2,feature3,...,target
value1,value2,value3,...,0
value1,value2,value3,...,1
```

## Disease-Specific Formats

### 1. Diabetes (`diabetes`)

**Required Columns:**
- `pregnancies` (integer, 0-20)
- `glucose` (float, mg/dL, typically 70-300)
- `bloodPressure` (float, mm Hg, typically 60-200)
- `skinThickness` (float, mm, typically 10-100)
- `insulin` (float, μU/mL, typically 0-900)
- `bmi` (float, typically 10-70)
- `diabetesPedigreeFunction` (float, typically 0-2)
- `age` (integer, years)
- `target` (integer, 0 or 1)

**Example CSV:**
```csv
pregnancies,glucose,bloodPressure,skinThickness,insulin,bmi,diabetesPedigreeFunction,age,target
6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
1,89,66,23,94,28.1,0.167,21,0
```

### 2. Heart Disease (`heart`)

**Required Columns:**
- `age` (integer, years)
- `sex` (integer, 0=Female, 1=Male)
- `cp` (integer, 0-3: chest pain type)
- `trestbps` (float, resting blood pressure, mm Hg)
- `chol` (float, serum cholesterol, mg/dL)
- `fbs` (integer, 0 or 1: fasting blood sugar > 120)
- `restecg` (integer, 0-2: resting ECG results)
- `thalach` (float, maximum heart rate achieved)
- `exang` (integer, 0 or 1: exercise induced angina)
- `oldpeak` (float, ST depression induced by exercise)
- `slope` (integer, 0-2: slope of peak exercise ST segment)
- `ca` (integer, 0-3: number of major vessels)
- `thal` (integer, 0-2: thalassemia)
- `target` (integer, 0 or 1)

**Example CSV:**
```csv
age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
63,1,3,145,233,1,0,150,0,2.3,0,0,1,1
37,1,2,130,250,0,1,187,0,3.5,0,0,2,1
41,0,1,130,204,0,0,172,0,1.4,2,0,2,1
```

### 3. Stroke (`stroke`)

**Required Columns:**
- `age` (integer, years)
- `hypertension` (integer, 0=No, 1=Yes)
- `heart_disease` (integer, 0=No, 1=Yes)
- `avg_glucose` (float, average glucose level, mg/dL)
- `bmi` (float, body mass index)
- `smoking_status` (integer, 0-3: smoking status categories)
- `target` (integer, 0 or 1)

**Example CSV:**
```csv
age,hypertension,heart_disease,avg_glucose,bmi,smoking_status,target
67,0,1,228.69,36.6,1,1
61,0,0,202.21,28.9,2,0
80,0,1,105.92,32.5,2,1
49,0,0,171.23,34.4,3,0
```

### 4. Liver Disease (`liver`)

**Required Columns:**
- `age` (integer, years)
- `gender` (integer, 0=Female, 1=Male)
- `tot_bilirubin` (float, total bilirubin, mg/dL)
- `direct_bilirubin` (float, direct bilirubin, mg/dL)
- `alkphos` (float, alkaline phosphatase, IU/L)
- `sgpt` (float, SGPT/ALT, U/L)
- `sgot` (float, SGOT/AST, U/L)
- `tot_proteins` (float, total proteins, g/dL)
- `albumin` (float, albumin, g/dL)
- `ag_ratio` (float, albumin/globulin ratio)
- `target` (integer, 0 or 1)

**Example CSV:**
```csv
age,gender,tot_bilirubin,direct_bilirubin,alkphos,sgpt,sgot,tot_proteins,albumin,ag_ratio,target
65,0,0.7,0.1,187,16,18,6.8,3.3,0.9,0
62,1,10.9,5.5,699,64,100,7.5,3.2,0.74,1
62,1,7.3,4.1,490,60,68,7.0,3.3,0.89,1
```

### 5. Kidney Disease (`kidney`)

**Required Columns:**
- `age` (integer, years)
- `bp` (float, blood pressure, mm/Hg)
- `sg` (float, specific gravity, typically 1.005-1.030)
- `albumin` (integer, 0-5: albumin level)
- `sugar` (integer, 0-5: sugar level)
- `rbc` (integer, 0 or 1: red blood cells)
- `pc` (integer, 0 or 1: pus cell)
- `pcc` (integer, 0 or 1: pus cell clumps)
- `ba` (integer, 0 or 1: bacteria)
- `bgr` (float, blood glucose random, mg/dL)
- `bu` (float, blood urea, mg/dL)
- `sc` (float, serum creatinine, mg/dL)
- `sod` (float, sodium, mEq/L)
- `pot` (float, potassium, mEq/L)
- `hemo` (float, hemoglobin, g/dL)
- `pcv` (float, packed cell volume, %)
- `wc` (float, white blood cell count, cells/cumm)
- `rc` (float, red blood cell count, millions/cumm)
- `htn` (integer, 0 or 1: hypertension)
- `dm` (integer, 0 or 1: diabetes mellitus)
- `cad` (integer, 0 or 1: coronary artery disease)
- `appet` (integer, 0 or 1: appetite)
- `pe` (integer, 0 or 1: pedal edema)
- `ane` (integer, 0 or 1: anemia)
- `target` (integer, 0 or 1)

**Example CSV:**
```csv
age,bp,sg,albumin,sugar,rbc,pc,pcc,ba,bgr,bu,sc,sod,pot,hemo,pcv,wc,rc,htn,dm,cad,appet,pe,ane,target
48,80,1.02,1,0,1,1,0,0,121,36,1.2,137,4.63,15.4,44,7800,5.2,1,1,0,1,1,1,1
7,50,1.02,4,0,1,1,1,0,0,18,0.8,111,2.5,11.3,38,6000,4.71,0,0,0,1,0,0,0
62,80,1.01,2,3,0,1,1,0,423,53,1.8,111,2.5,9.6,31,7500,3.9,0,1,0,0,1,1,1
```

## Important Notes

### 1. Column Names Must Match Exactly
- Column names are case-sensitive
- They must match the feature names expected by the model
- The `target` column is mandatory

### 2. Data Types
- **Integers**: Use whole numbers (0, 1, 2, etc.)
- **Floats**: Use decimal numbers (33.6, 148.0, etc.)
- **Target**: Must be 0 (no disease) or 1 (disease)

### 3. Missing Values
- The current implementation doesn't handle missing values automatically
- Preprocess your data to fill or remove missing values before training
- You can use pandas to handle this:
  ```python
  df = pd.read_csv('your_data.csv')
  df = df.fillna(df.mean())  # Fill with mean
  # or
  df = df.dropna()  # Remove rows with missing values
  ```

### 4. Data Size
- Minimum recommended: 100+ samples per class
- More data = better model performance
- Balanced datasets (equal 0s and 1s) work best

## How to Use Your Data

### Step 1: Prepare Your CSV File

1. Create a CSV file with the required columns for your disease type
2. Ensure the `target` column exists (0 or 1)
3. Save it in the `data/` directory

Example file structure:
```
Health-Predictor/
└── data/
    ├── diabetes_data.csv
    ├── heart_data.csv
    └── stroke_data.csv
```

### Step 2: Train with Your Data

**Option A: Via Python Script**
```python
from backend.ml_models.train_models import train_disease_model

# Train diabetes model with your data
train_disease_model('diabetes', 'data/diabetes_data.csv')
```

**Option B: Via API (after starting server)**
```bash
curl -X POST "http://localhost:8000/api/training/train" \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "diabetes",
    "dataset_path": "data/diabetes_data.csv"
  }'
```

**Option C: Modify train_all_models.py**
```python
# In train_all_models.py, change:
train_disease_model('diabetes', 'data/your_diabetes_data.csv')
```

## Example: Creating a Sample Dataset

Here's a Python script to create a sample diabetes dataset:

```python
import pandas as pd
import numpy as np

# Generate sample data
n_samples = 500
data = {
    'pregnancies': np.random.randint(0, 20, n_samples),
    'glucose': np.random.normal(120, 30, n_samples).clip(70, 300),
    'bloodPressure': np.random.normal(70, 15, n_samples).clip(60, 200),
    'skinThickness': np.random.normal(25, 10, n_samples).clip(10, 100),
    'insulin': np.random.normal(100, 100, n_samples).clip(0, 900),
    'bmi': np.random.normal(30, 7, n_samples).clip(10, 70),
    'diabetesPedigreeFunction': np.random.normal(0.5, 0.2, n_samples).clip(0, 2),
    'age': np.random.randint(20, 80, n_samples)
}

# Create target (diabetes = 1 if glucose > 140 or bmi > 30)
df = pd.DataFrame(data)
df['target'] = ((df['glucose'] > 140) | (df['bmi'] > 30)).astype(int)

# Save to CSV
df.to_csv('data/diabetes_data.csv', index=False)
print("Dataset created: data/diabetes_data.csv")
```

## Validating Your Data

Before training, validate your data format:

```python
import pandas as pd

# Load your data
df = pd.read_csv('data/your_data.csv')

# Check required columns
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("Target distribution:", df['target'].value_counts())
print("Missing values:", df.isnull().sum())
print("Data types:", df.dtypes)
```

## Common Issues & Solutions

### Issue: "Dataset must have a 'target' column"
**Solution:** Ensure your CSV has a column named exactly `target` (lowercase)

### Issue: Column names don't match
**Solution:** Rename columns to match the expected feature names exactly

### Issue: Wrong data types
**Solution:** Convert columns to appropriate types:
```python
df['age'] = df['age'].astype(int)
df['bmi'] = df['bmi'].astype(float)
```

### Issue: Missing values
**Solution:** Handle missing values before training:
```python
df = df.fillna(0)  # Fill with 0
# or
df = df.dropna()  # Remove rows with missing values
```

## Quick Reference

| Disease | Required Columns | Example File |
|---------|------------------|--------------|
| diabetes | 8 features + target | `data/diabetes_data.csv` |
| heart | 13 features + target | `data/heart_data.csv` |
| stroke | 5 features + target | `data/stroke_data.csv` |
| liver | 10 features + target | `data/liver_data.csv` |
| kidney | 23 features + target | `data/kidney_data.csv` |

---

**Need help?** Check the column names in `backend/ml_models/train_models.py` in the `generate_synthetic_data()` function for each disease type.

