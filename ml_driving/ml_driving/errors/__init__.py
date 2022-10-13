from flask import Blueprint

bp = Blueprint('errors', __name__)

from ml_driving.errors import handlers