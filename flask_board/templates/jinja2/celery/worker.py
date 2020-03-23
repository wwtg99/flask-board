from application import create_app, init_celery


celery = init_celery(create_app(config_log=False))
