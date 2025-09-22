import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler

# Resolve project root and models path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')


def preprocess_data(input_data):
    """
    Preprocess input data for prediction
    """
    # Load the scaler
    try:
        scaler = joblib.load(SCALER_PATH)
    except Exception:
        raise Exception(f"Scaler not found at {SCALER_PATH}. Please train the model first.")
    
    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Ensure all columns are in correct order
    expected_columns = [
        'age', 'sex', 'smoker', 'years_of_smoking', 'LDL_cholesterol', 
        'chest_pain_type', 'height', 'weight', 'familyhist', 'activity', 
        'lifestyle', 'cardiac_intervention', 'heart_rate', 'diabets', 
        'blood_pressure_sys', 'blood_pressure_dias', 'hypertention', 
        'Interventricular_septal_end_diastole', 'ecg_pattern', 'Q_wave'
    ]
    
    # Reorder columns if necessary
    missing = [c for c in expected_columns if c not in input_df.columns]
    if missing:
        raise ValueError(f"Missing input fields: {missing}")

    input_df = input_df[expected_columns]

    # Scale the data
    scaled_data = scaler.transform(input_df)

    return scaled_data