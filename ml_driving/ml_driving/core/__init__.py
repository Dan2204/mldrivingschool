from flask import Blueprint

bp = Blueprint('core', __name__)

from ml_driving.core import views
