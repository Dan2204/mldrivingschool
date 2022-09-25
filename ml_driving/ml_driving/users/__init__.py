from flask import Blueprint

bp = Blueprint('users', __name__)

from ml_driving.users import views