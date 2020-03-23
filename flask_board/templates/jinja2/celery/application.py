import os
from werkzeug.utils import import_string
from logging.config import dictConfig
from flask import Flask
from celery import Celery


# Environment key to config flask instance path
ENV_INSTANCE_PATH = 'FLASK_INSTANCE_PATH'
# Environment key to config flask config module
ENV_CONFIG_MODULE = 'FLASK_CONFIG_MODULE'


def config_logger(app):
    if 'LOGGER' in app.config:
        dictConfig(app.config['LOGGER'])


def register_app(app):
    """
    Import blueprints module in REGISTERED_APP config.

    :param app: flask app
    """
    with app.app_context():
        for a in app.config['REGISTERED_APP']:
            bp = '{}.blueprints'.format(a)
            import_string(bp)


def create_app_by_config(conf=None, config_log=True, register=True):
    """
    Create flask app by config object.

    :param conf: config object
    :param config_log: whether to config logger
    :param register: whether to register apps
    :return: flask app
    """
    # check instance path
    instance_path = os.environ.get(ENV_INSTANCE_PATH) or None
    # create app
    app = Flask(__name__, instance_path=instance_path)
    # ensure the instance folder exists
    if app.instance_path:
        try:
            os.makedirs(app.instance_path, exist_ok=True)
        except OSError:
            pass
    # configure app
    if conf:
        app.config.from_object(conf)
    # config logger
    if config_log:
        config_logger(app)
    # register app
    if register:
        register_app(app)
    return app


def create_app(config_log=True, register=True):
    """
    Create flask app by config module.

    :param config_log: whether to config logger
    :param register: whether to register apps
    :return: flask app
    """
    config = os.environ.get(ENV_CONFIG_MODULE) or 'config'
    return create_app_by_config(conf=config, config_log=config_log, register=register)


def init_celery(app):
    cel = Celery(app.name)
    cel.conf.update(app.config['CELERY_CONFIG'])
    # register tasks
    with app.app_context():
        register_apps = app.config['REGISTERED_APP']
        for app in register_apps:
            import_string('{}.tasks'.format(app), silent=True)
    return cel
