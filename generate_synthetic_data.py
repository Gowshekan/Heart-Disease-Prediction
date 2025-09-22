import pandas as pd
import numpy as np
import os

def generate_synthetic_data():
    """Generate synthetic heart disease dataset"""
    np.random.seed(42)
    n_samples = 333
    
    # Generate synthetic data
    data = {
        'age': np.random.randint(20, 90, n_samples),
        'sex': np.random.randint(0, 2, n_samples),
        'smoker': np.random.randint(0, 2, n_samples),
        'years_of_smoking': np.random.randint(0, 50, n_samples),
        'LDL_cholesterol': np.random.uniform(26, 260, n_samples),
        'chest_pain_type': np.random.randint(1, 5, n_samples),
        'height': np.random.randint(128, 192, n_samples),
        'weight': np.random.uniform(41, 134, n_samples),
        'familyhist': np.random.randint(0, 2, n_samples),
        'activity': np.random.randint(0, 2, n_samples),
        'lifestyle': np.random.randint(1, 4, n_samples),
        'cardiac_intervention': np.random.randint(0, 2, n_samples),
        'heart_rate': np.random.randint(40, 140, n_samples),
        'diabets': np.random.randint(0, 2, n_samples),
        'blood_pressure_sys': np.random.randint(80, 220, n_samples),
        'blood_pressure_dias': np.random.randint(40, 140, n_samples),
        'hypertention': np.random.randint(0, 2, n_samples),
        'Interventricular_septal_end_diastole': np.random.randint(0, 2, n_samples),
        'ecg_pattern': np.random.randint(1, 5, n_samples),
        'Q_wave': np.random.randint(0, 2, n_samples),
        'target': np.random.randint(0, 2, n_samples)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create directories if they don't exist
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Save to CSV
    csv_path = os.path.join(data_dir, 'ECG-Dataset.csv')
    df.to_csv(csv_path, index=False)
    print(f"Synthetic dataset with {n_samples} records created successfully!")
    
    return df

if __name__ == '__main__':
    generate_synthetic_data()