from flask import Blueprint

bp = Blueprint('admin', __name__)

from ml_driving.admin import views