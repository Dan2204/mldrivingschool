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

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'users.login'


#-------------------------
#---- BLUEPRINT SETUP ----
#-------------------------

from ml_driving.core.views import bp as core


app.register_blueprint(core)

