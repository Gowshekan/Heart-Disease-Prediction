#!/usr/bin/env python3
"""
Setup script for Heart Disease Prediction Project
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Successfully installed all requirements")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def check_data_exists():
    """Check if dataset exists"""
    if os.path.exists('data/ECG-Dataset.csv'):
        print("✓ Dataset found")
        return True
    else:
        print("! Dataset not found, generating synthetic data...")
        return False

def generate_synthetic_data():
    """Generate synthetic data if dataset doesn't exist"""
    try:
        subprocess.check_call([sys.executable, "generate_synthetic_data.py"])
        print("✓ Synthetic data generated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating synthetic data: {e}")
        return False

def train_model():
    """Train the machine learning model"""
    print("Training the model...")
    try:
        # Change to project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.check_call([sys.executable, "models/train_model.py"])
        print("✓ Model trained successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error training model: {e}")
        return False

def check_model_exists():
    """Check if trained model exists"""
    if os.path.exists('models/heart_disease_model.h5'):
        print("✓ Trained model found")
        return True
    else:
        print("! Trained model not found")
        return False

def main():
    """Main setup function"""
    print("Heart Disease Prediction Project Setup")
    print("=" * 40)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation")
        return False
    
    # Step 2: Check/generate data
    if not check_data_exists():
        if not generate_synthetic_data():
            print("Setup failed at data generation")
            return False
    
    # Step 3: Check/train model
    if not check_model_exists():
        if not train_model():
            print("Setup failed at model training")
            return False
    
    print("\n" + "=" * 40)
    print("✓ Setup completed successfully!")
    print("You can now run the application with: python app.py")
    return True

if __name__ == "__main__":
    main()