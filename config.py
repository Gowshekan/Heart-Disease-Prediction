import os

# Secret key for session management
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'