from flask import Flask
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cd4c2fe74a950d17489a03f6ef274114'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artistry.db'


# create db sqlalchamey instance
db = SQLAlchemy(app)

# hashing password
bcrypt = Bcrypt(app)
# login -> auth user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # function name of the route
login_manager.login_message_category = 'info'

from artistry import routes
