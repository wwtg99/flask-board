from flask import Blueprint
from flask import current_app as app


# register blueprint
bp = Blueprint('api', __name__, url_prefix='/api')
app.register_blueprint(bp)
