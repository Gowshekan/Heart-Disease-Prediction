import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os

# Resolve project root and data/model paths reliably
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'ECG-Dataset.csv')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

def create_model():
    """
    Create and return the heart disease prediction model
    """
    model = Sequential()
    model.add(Dense(16, input_dim=20, activation='relu', 
                    kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.2))
    model.add(Dense(8, activation='relu', 
                    kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy', 
                  optimizer=Adam(learning_rate=0.001), 
                  metrics=['accuracy'])
    
    return model

def load_data():
    """
    Load and preprocess the heart disease dataset
    """
    # Load data
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run generate_synthetic_data.py or place the CSV in data/")
    data = pd.read_csv(DATA_PATH)
    
    # Rename columns
    data.columns = ['age','sex','smoker','years_of_smoking','LDL_cholesterol','chest_pain_type',
                    'height','weight', 'familyhist','activity', 'lifestyle', 'cardiac_intervention', 
                    'heart_rate', 'diabets', 'blood_pressure_sys', 'blood_pressure_dias', 
                    'hypertention', 'Interventricular_septal_end_diastole', 'ecg_pattern', 'Q_wave', 'target']
    
    return data

def train_model():
    """
    Train the heart disease prediction model
    """
    # Load data
    data = load_data()
    
    # Split features and target
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    # Save scaler for later use
    os.makedirs(MODELS_DIR, exist_ok=True)
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    joblib.dump(sc, scaler_path)
    
    # Create model
    model = create_model()
    
    # Define early stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    # Train model
    history = model.fit(X_train, y_train, 
                        validation_data=(X_test, y_test),
                        epochs=100, 
                        batch_size=16, 
                        callbacks=[early_stop],
                        verbose=1)
    
    # Evaluate model
    y_pred = (model.predict(X_test) > 0.5).astype("int32")
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Accuracy:", accuracy)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, 'heart_disease_model.h5')
    model.save(model_path)
    print(f"Model saved successfully to {model_path}!")
    
    return model, history, accuracy

if __name__ == '__main__':
    train_model()