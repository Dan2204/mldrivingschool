from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)

#-------------------
#---- CONFIGURE ----
#-------------------

app.config.from_object(Config)


moment = Moment(app)


#------------------------
#---- DATABASE SETUP ----
#------------------------

db = SQLAlchemy(app)
Migrate(app, db, render_as_batch=True)


#-----------------------------
#---- LOGIN MANAGER SETUP ----
#-----------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'


#-------------------------
#---- BLUEPRINT SETUP ----
#-------------------------

from ml_driving.core.views import bp as core
from ml_driving.users.views import bp as users
from ml_driving.admin.views import bp as admin
from ml_driving.reviews.views import bp as reviews
from ml_driving.errors.handlers import bp as errors


app.register_blueprint(core)
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(errors)
app.register_blueprint(reviews)

