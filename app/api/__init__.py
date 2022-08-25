from flask import current_app, Blueprint

bp = Blueprint('api', __name__)

from app.api import queries
