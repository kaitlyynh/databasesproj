from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# ATTEMPT Connect to XAMPP Database
# app.config['MYSQL_HOST'] = 'localhost'
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "2003"
# app.config["MYSQL_DB"] = "milestone3"

# ATTEMPT Connect to XAMPP Database

from lookup import routes