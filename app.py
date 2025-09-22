from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
import joblib
from utils.preprocessing import preprocess_data

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Use project-root paths so the app runs regardless of working directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
KERAS_MODEL_PATH = os.path.join(MODELS_DIR, 'heart_disease_model.h5')
SKLEARN_MODEL_PATH = os.path.join(MODELS_DIR, 'sklearn_model.joblib')

# Load model(s) if available. Import TensorFlow lazily to avoid import errors when it's not installed.
model = None
model_type = None
if os.path.exists(KERAS_MODEL_PATH):
    try:
        # Import here to avoid TensorFlow import at module load when it's not available
        from tensorflow.keras.models import load_model
        model = load_model(KERAS_MODEL_PATH)
        model_type = 'keras'
        print(f"Loaded Keras model from {KERAS_MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load Keras model: {e}")
        model = None
        model_type = None

if model is None and os.path.exists(SKLEARN_MODEL_PATH):
    try:
        model = joblib.load(SKLEARN_MODEL_PATH)
        model_type = 'sklearn'
        print(f"Loaded sklearn model from {SKLEARN_MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load sklearn model: {e}")
        model = None
        model_type = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if model is None:
        return render_template('predict.html', error="Model not loaded. Please train the model first.")
    
    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'age': float(request.form['age']),
                'sex': int(request.form['sex']),
                'smoker': int(request.form['smoker']),
                'years_of_smoking': float(request.form['years_of_smoking']),
                'LDL_cholesterol': float(request.form['LDL_cholesterol']),
                'chest_pain_type': int(request.form['chest_pain_type']),
                'height': float(request.form['height']),
                'weight': float(request.form['weight']),
                'familyhist': int(request.form['familyhist']),
                'activity': int(request.form['activity']),
                'lifestyle': int(request.form['lifestyle']),
                'cardiac_intervention': int(request.form['cardiac_intervention']),
                'heart_rate': int(request.form['heart_rate']),
                'diabets': int(request.form['diabets']),
                'blood_pressure_sys': int(request.form['blood_pressure_sys']),
                'blood_pressure_dias': int(request.form['blood_pressure_dias']),
                'hypertention': int(request.form['hypertention']),
                'Interventricular_septal_end_diastole': int(request.form['Interventricular_septal_end_diastole']),
                'ecg_pattern': int(request.form['ecg_pattern']),
                'Q_wave': int(request.form['Q_wave'])
            }
            
            # Preprocess the data
            processed_data = preprocess_data(form_data)
            
            # Make prediction depending on model type
            if model_type == 'keras':
                prediction = model.predict(processed_data)
                prediction_prob = float(prediction[0][0])
            elif model_type == 'sklearn':
                # sklearn classifiers don't always provide predict_proba; try if available
                if hasattr(model, 'predict_proba'):
                    prob = model.predict_proba(processed_data)
                    prediction_prob = float(prob[0][1])
                else:
                    pred = model.predict(processed_data)
                    prediction_prob = float(pred[0])
            else:
                raise RuntimeError('No prediction model available')
            
            # Determine result
            result = "Heart Disease" if prediction_prob > 0.5 else "Normal"
            confidence = prediction_prob if prediction_prob > 0.5 else 1 - prediction_prob
            
            return render_template('result.html', 
                                 result=result, 
                                 confidence=round(confidence * 100, 2),
                                 probability=round(prediction_prob * 100, 2))
            
        except Exception as e:
            return render_template('predict.html', error=str(e))
    
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 503
    
    try:
        data = request.get_json()
        
        # Preprocess the data
        processed_data = preprocess_data(data)
        
        # Make prediction depending on model type
        if model_type == 'keras':
            prediction = model.predict(processed_data)
            prediction_prob = float(prediction[0][0])
        elif model_type == 'sklearn':
            if hasattr(model, 'predict_proba'):
                prob = model.predict_proba(processed_data)
                prediction_prob = float(prob[0][1])
            else:
                pred = model.predict(processed_data)
                prediction_prob = float(pred[0])
        else:
            return jsonify({'error': 'No prediction model available.'}), 503
        
        return jsonify({
            'prediction': 'Heart Disease' if prediction_prob > 0.5 else 'Normal',
            'probability': round(prediction_prob * 100, 2),
            'confidence': round((prediction_prob if prediction_prob > 0.5 else 1 - prediction_prob) * 100, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)