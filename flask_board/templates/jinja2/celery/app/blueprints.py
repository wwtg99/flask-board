import logging
from flask import Blueprint
from flask import current_app as app, jsonify
from app.exceptions import APIException


# register blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# add your routes here
# bp.add_url_rule('health', view_func=views)


# handle exceptions, change to your own exception
@bp.errorhandler(APIException)
def handle_api_exception(error):
    logging.error(error)
    data = error.to_dict()
    response = jsonify(data)
    response.status_code = error.status_code
    return response


# @bp.errorhandler(Exception)
# def handle_exception(e):
#     logging.error(e)
#     return {'message': 'internal server error'}, 500

app.register_blueprint(bp)
