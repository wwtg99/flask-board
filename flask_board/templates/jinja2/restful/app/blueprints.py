from flask import Blueprint, jsonify
from flask import current_app as app
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from app import views


# register blueprint
bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

# add restful resources
api.add_resource(views.Health, '/health')


# handle exceptions, change to your own exception
@bp.errorhandler(HTTPException)
def handle_api_exception(error):
    data = error.to_dict()
    response = jsonify(data)
    response.status_code = error.status_code
    return response


app.register_blueprint(bp)
