from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import googlemaps
from flask import Flask, jsonify
from flask_googlemaps import GoogleMaps, Map
from flask_simple_geoip import SimpleGeoIP
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "FGHJK^&(GHJK&*GHUJBNMHJ&^%#$%&*FGHJCVBJIUYT"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tester:password@localhost/thedb"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://super:password@localhost/data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

app.config['GOOGLEMAPS_KEY'] = "keyhere"
app.config['GEOIPIFY_API_KEY'] = "keyhere"

UPLOAD_FOLDER = './app/static/uploads'

simple_geoip = SimpleGeoIP(app)
GoogleMaps(app)


db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
