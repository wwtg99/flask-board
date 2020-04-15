import os
from app.application import create_app


os.environ.setdefault('FLASK_CONFIG_MODULE', 'app.config')
app = create_app()
