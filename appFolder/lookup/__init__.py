from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_ngrok import run_with_ngrok
import os

app = Flask(__name__)
# run_with_ngrok(app)  # Set up ngrok but only activate when app.run() is called

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'market.db')
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# ATTEMPT Connect to MySQL Workbench Database
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "2003"
app.config["MYSQL_DB"] = "milestone3"

# ATTEMPT Connect to MySQL Workbench Database

from lookup import routes