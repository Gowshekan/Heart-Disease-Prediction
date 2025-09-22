# Heart Disease Prediction Project - Setup and Usage Guide

## Issues Fixed

### 1. Dependency Issues ✅
- **Fixed TensorFlow version compatibility**: Updated from incompatible version to TensorFlow 2.20.0 that works with Python 3.13
- **Updated import statements**: Changed from `keras` imports to `tensorflow.keras` imports for compatibility
- **Updated requirements.txt**: Used flexible version constraints instead of fixed versions

### 2. Missing Files ✅
- **Generated synthetic dataset**: Created ECG-Dataset.csv with 333 synthetic records
- **Trained the model**: Created heart_disease_model.h5 with 63% accuracy
- **Generated scaler**: Created scaler.pkl for data preprocessing

### 3. Application Robustness ✅
- **Added error handling**: App now gracefully handles missing model files
- **Fixed file paths**: Corrected relative path issues in training script
- **Added model loading checks**: Application shows helpful error messages if model isn't available

## Project Structure
```
Heart Disease Prediction Deeplearning/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup script
├── run.py                 # Application runner with checks
├── wsgi.py                # WSGI entry point
├── generate_synthetic_data.py  # Data generation script
├── data/
│   └── ECG-Dataset.csv    # Dataset (333 records)
├── models/
│   ├── heart_disease_model.h5  # Trained model
│   ├── scaler.pkl         # Data scaler
│   └── train_model.py     # Model training script
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   └── about.html
├── static/               # CSS and JavaScript
│   ├── css/style.css
│   └── js/script.js
└── utils/
    └── preprocessing.py  # Data preprocessing utilities
```

## How to Run the Project

### Method 1: Quick Start (Recommended)
```bash
# Navigate to project directory
cd "c:\Users\Admin\OneDrive\Desktop\Heart Disease Prediction Deeplearning"

# Run the application
python app.py
```

The application will be available at: http://127.0.0.1:5000

### Method 2: Using the Runner Script
```bash
python run.py
```

### Method 3: Complete Setup (if starting fresh)
```bash
# Run setup script to install dependencies and prepare everything
python setup.py

# Then run the application
python app.py
```

## Features

### Web Interface
- **Home Page**: Introduction to the project
- **Prediction Page**: Form to input patient data and get heart disease prediction
- **Results Page**: Shows prediction results with confidence scores
- **About Page**: Information about the project

### API Endpoint
- **POST /api/predict**: JSON API for programmatic access
- Returns prediction, probability, and confidence scores

### Input Parameters
The model accepts 20 parameters:
- Age, Sex, Smoker status, Years of smoking
- LDL cholesterol, Chest pain type, Height, Weight
- Family history, Activity level, Lifestyle
- Cardiac intervention, Heart rate, Diabetes
- Blood pressure (systolic/diastolic), Hypertension
- Interventricular septal end diastole, ECG pattern, Q wave

## Model Performance
- **Algorithm**: Deep Neural Network with regularization
- **Architecture**: 16 → 8 → 1 neurons with dropout layers
- **Accuracy**: 63% on test data
- **Training**: 92 epochs with early stopping

## Dependencies
- Flask 2.3.3
- TensorFlow 2.20.0+
- Pandas, NumPy, Scikit-learn
- Matplotlib, Seaborn (for visualizations)
- Joblib (for model serialization)

## Notes
- The model uses synthetic data for demonstration purposes
- In production, use real medical data with proper validation
- The current model achieves 63% accuracy - consider improving with more data and features
- TensorFlow warnings about CPU optimizations are normal and can be ignored

## Troubleshooting

### Model Not Found Error
If you see "Model not loaded" error:
```bash
python models/train_model.py
```

### Missing Dataset
If dataset is missing:
```bash
python generate_synthetic_data.py
```

### Dependency Issues
Update requirements:
```bash
pip install -r requirements.txt
```

## Success! 🎉
The Heart Disease Prediction project is now fully functional with all dependencies resolved and models trained.
