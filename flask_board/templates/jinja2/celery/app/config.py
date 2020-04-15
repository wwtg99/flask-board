import os
from dotenv import load_dotenv


# Load env file
# The file path is set by environment FLASK_ENV_FILE
env_file_key = 'FLASK_ENV_FILE'
env_file = os.getenv(env_file_key) or '.env'
if os.path.exists(env_file):
    load_dotenv(env_file)


# All uppercase attributes will be load to flask config

SECRET_KEY = os.getenv('SECRET_KEY') or '{{ secret }}'
DEBUG = os.getenv('DEBUG') == 'on'
TESTING = os.getenv('TESTING') == 'on'

# Logger configuration
log_level = os.getenv('LOG_LEVEL') or 'INFO'
LOGGER = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        },
        'detail': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': log_level,
            'stream': 'ext://flask.logging.wsgi_errors_stream'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detail',
            'filename': os.getenv('LOG_FILE') or 'app.log',
            'level': log_level,
            'maxBytes': 5000000,
            'backupCount': 5,
            'delay': True
        }
    },
    'root': {
        'level': log_level,
        'handlers': (os.getenv('LOG_HANDLERS') or 'console,file').split(',')
    }
}

# Celery
CELERY_CONFIG = {
    'broker_url': os.getenv('CELERY_BROKER_URL'),
    'result_backend': os.getenv('CELERY_RESULT_BACKEND'),
}
