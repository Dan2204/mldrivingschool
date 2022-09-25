from flask import Blueprint

bp = Blueprint('reviews', __name__)

from ml_driving.reviews import views