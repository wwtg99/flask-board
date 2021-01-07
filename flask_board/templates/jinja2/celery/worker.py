import os
from app.application import create_app, make_celery


os.environ.setdefault('FLASK_CONFIG_MODULE', 'app.config')
celery = make_celery(create_app(config_log=False))
