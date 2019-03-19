from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8d5eb5a677fc571260474b96e559afd5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#creates the database
db = SQLAlchemy(app)
#creates an instance to allow us to hash passwords
bcrypt = Bcrypt(app)
#helps with logging in
login_manager = LoginManager(app)
#lets flask know which is the login page to redirect users to
login_manager.login_view = 'login'
#the HTML class you want login message to be displayed as
login_manager.login_message_category = 'danger'

from flaskblog import routes