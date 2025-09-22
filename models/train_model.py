import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Try to import TensorFlow; if not available, we'll fall back to scikit-learn
TF_AVAILABLE = True
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras import regularizers
    from tensorflow.keras.callbacks import EarlyStopping
except Exception:
    TF_AVAILABLE = False
    # Import sklearn fallback components
    from sklearn.linear_model import LogisticRegression
    print("TensorFlow not available; will use scikit-learn LogisticRegression fallback for training.")

# Resolve project root and data/model paths reliably
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'ECG-Dataset.csv')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

def load_and_preprocess_data():
    # Load data
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run generate_synthetic_data.py or place the CSV in data/")
    data = pd.read_csv(DATA_PATH)
    
    # Rename columns
    data.columns = ['age','sex','smoker','years_of_smoking','LDL_cholesterol','chest_pain_type',
                    'height','weight', 'familyhist','activity', 'lifestyle', 'cardiac_intervention', 
                    'heart_rate', 'diabets', 'blood_pressure_sys', 'blood_pressure_dias', 
                    'hypertention', 'Interventricular_septal_end_diastole', 'ecg_pattern', 'Q_wave', 'target']
    
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
    
    return X_train, X_test, y_train, y_test

def create_model(input_dim):
    if TF_AVAILABLE:
        model = Sequential()
        model.add(Dense(16, input_dim=input_dim, activation='relu', 
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
    else:
        # sklearn fallback does not need this function's architecture
        return None

def train_and_save_model():
    # Load and preprocess data
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    # If TensorFlow is available, train a Keras model; otherwise train a sklearn model
    if TF_AVAILABLE:
        # Create model
        model = create_model(X_train.shape[1])
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
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        # Save model
        os.makedirs(MODELS_DIR, exist_ok=True)
        model_path = os.path.join(MODELS_DIR, 'heart_disease_model.h5')
        model.save(model_path)
        print(f"Keras model saved successfully to {model_path}!")
        return model, history
    else:
        # Train a simple Logistic Regression classifier as a fallback
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Sklearn fallback Accuracy:", accuracy)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        # Save sklearn model
        os.makedirs(MODELS_DIR, exist_ok=True)
        skl_model_path = os.path.join(MODELS_DIR, 'sklearn_model.joblib')
        joblib.dump(clf, skl_model_path)
        print(f"Sklearn model saved successfully to {skl_model_path}!")
        return clf, None

if __name__ == '__main__':
    train_and_save_model()