
import os
from flask import Flask
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'static/uploads'
 # this DEBUG config here will be overridden by FLASK_DEBUG shell environment
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '4c4e82067c705665274f8d1d33d5fd847622416172c2f7ef'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID", None)
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET", None)
app.config['GOOGLE_DISCOVERY_URL'] = os.getenv("GOOGLE_DISCOVERY_URL", None)

if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
oauth = OAuth(app)
oauth.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'homepage_login'
login_manager.init_app(app)

from app import views  # noqa