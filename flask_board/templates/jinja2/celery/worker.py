import os
from app.application import create_app, init_celery


os.environ.setdefault('FLASK_CONFIG_MODULE', 'app.config')
celery = init_celery(create_app(config_log=False))
