from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.config['SECRET_KEY'] = "FGHJK^&(GHJK&*GHUJBNMHJ&^%#$%&*FGHJCVBJIUYT"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:password@localhost/database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBpR7ifpmENecBIWXWMyZ2Xmin7FoHDaIE"

UPLOAD_FOLDER = './app/static/uploads'

GoogleMaps(app)

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
