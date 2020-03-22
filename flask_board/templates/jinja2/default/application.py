import os
from werkzeug.utils import import_string
from logging.config import dictConfig
from flask import Flask


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


def create_app_by_config(conf=None):
    """
    Create flask app by config object.

    :param conf: config object
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
    config_logger(app)
    # register app
    register_app(app)
    return app


def create_app():
    """
    Create flask app by config module.

    :return: flask app
    """
    config = os.environ.get(ENV_CONFIG_MODULE) or 'config'
    return create_app_by_config(config)
