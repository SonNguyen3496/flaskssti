from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from jinja2 import Environment
#Jinja2 = Environment()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1ea2cfbe60bb6d94b632ff859c9b28e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from flaskblog import routes