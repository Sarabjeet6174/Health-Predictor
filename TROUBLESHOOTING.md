# Troubleshooting Guide

## Common Issues and Solutions

### 400 Bad Request Error

If you're getting `400 Bad Request` errors when making predictions, here are the most common causes:

#### 1. Models Not Trained

**Error:** `Model for 'diabetes' not found. Please train the model first.`

**Solution:**
```bash
python train_all_models.py
```

This will train all models and save them to the `models/` directory.

#### 2. Feature Name Mismatch

**Error:** `Missing required feature: glucose`

**Problem:** The feature names in your frontend form don't match what the model expects.

**Solution:** Check the feature names in:
- Frontend: `frontend/index.html` (diseaseConfigs object)
- Model: The model expects the exact feature names from training

**Common mismatches:**
- `bloodPressure` vs `blood_pressure`
- `skinThickness` vs `skin_thickness`
- Case sensitivity issues

#### 3. Invalid Data Types

**Error:** `Invalid value for feature 'glucose': abc. Must be a number.`

**Problem:** Non-numeric values being sent to the API.

**Solution:** Ensure all form inputs are numeric. Check:
- No text in number fields
- Select dropdowns return numeric values (0, 1, 2, etc.)

#### 4. Missing Features

**Error:** `Missing required feature: [feature_name]`

**Problem:** The model expects certain features that aren't being sent.

**Solution:** 
1. Check what features the model expects:
   ```python
   from backend.ml_models.model_manager import model_manager
   info = model_manager.get_model_info('diabetes')
   print(info['features'])
   ```

2. Ensure your frontend form includes all required features

### How to Debug

#### 1. Check Server Logs

The server logs will show detailed error messages:
```
INFO: Prediction request received for disease: diabetes
INFO: Features received: ['pregnancies', 'glucose', ...]
ERROR: Missing required feature: glucose
```

#### 2. Test API Directly

Use curl or Postman to test the API:

```bash
curl -X POST "http://localhost:8000/api/predictions/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "diabetes",
    "features": {
      "pregnancies": 6,
      "glucose": 148,
      "bloodPressure": 72,
      "skinThickness": 35,
      "insulin": 0,
      "bmi": 33.6
    }
  }'
```

#### 3. Check Model Status

```bash
curl http://localhost:8000/api/models/list
```

This shows which models are trained and available.

#### 4. Check Browser Console

Open browser DevTools (F12) and check the Console tab for JavaScript errors.

### Quick Fixes

#### Fix 1: Train Models
```bash
python train_all_models.py
```

#### Fix 2: Restart Server
```bash
# Stop the server (Ctrl+C)
python start_server.py
```

#### Fix 3: Check Feature Names

Compare frontend feature names with model expectations:

**Frontend (index.html):**
```javascript
features: [
    { name: "glucose", label: "Glucose Level", ... },
    { name: "bloodPressure", label: "Blood Pressure", ... }
]
```

**Model expects:** Check `backend/ml_models/train_models.py` in `generate_synthetic_data()` function

#### Fix 4: Validate Data Format

Use the validation script:
```bash
python validate_data.py diabetes data/your_data.csv
```

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Model for X not found` | Model not trained | Run `python train_all_models.py` |
| `Missing required feature: X` | Feature name mismatch | Check feature names match exactly |
| `Invalid value for feature` | Non-numeric input | Ensure all inputs are numbers |
| `400 Bad Request` | General validation error | Check server logs for details |
| `500 Internal Server Error` | Server-side error | Check server logs, verify model files exist |

### Still Having Issues?

1. **Check server logs** - They contain detailed error information
2. **Verify models exist** - Check `models/` directory has `.pkl` files
3. **Test with curl** - Isolate frontend vs backend issues
4. **Check browser console** - Look for JavaScript errors
5. **Verify feature names** - Must match exactly (case-sensitive)

### Getting More Details

Enable debug logging in `backend/api/predictions.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed request/response information in the server logs.


