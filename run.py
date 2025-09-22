#!/usr/bin/env python3
"""
Run script for Heart Disease Prediction Project
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        import joblib
        print("✓ Core dependencies found")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run setup.py first")
        return False
    
    try:
        import tensorflow
        print("✓ TensorFlow found")
    except ImportError:
        print("✗ TensorFlow not found")
        print("Please run setup.py first")
        return False
    
    return True

def check_model_files():
    """Check if required model files exist"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        os.path.join(project_root, 'models', 'heart_disease_model.h5'),
        os.path.join(project_root, 'models', 'scaler.pkl'),
        os.path.join(project_root, 'data', 'ECG-Dataset.csv')
    ]

    missing_files = [p for p in required_files if not os.path.exists(p)]
    
    if missing_files:
        print(f"✗ Missing required files: {missing_files}")
        print("Please run setup.py first")
        return False
    else:
        print("✓ All required files found")
        return True

def run_app():
    """Run the Flask application"""
    print("Starting Heart Disease Prediction Web App...")
    print("The app will be available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")

def main():
    """Main run function"""
    print("Heart Disease Prediction Project")
    print("=" * 40)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check model files
    if not check_model_files():
        return False
    
    # Run the application
    run_app()
    return True

if __name__ == "__main__":
    main()