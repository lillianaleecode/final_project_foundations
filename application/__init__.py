# from flask_wtf import FlaskForm
# from flask_wtf import Form
# from flask import Flask, render_template, url_for, redirect, flash, request, session
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta
# #for the form:
# from application.forms import RegistrationForm, LoginForm, ContactForm
# from wtforms import StringField, SubmitField, TextField, TextAreaField, SubmitField
# from flask_wtf import Form

# #for login
# from flask_login import LoginManager, login_user

# #for authentication
# from flask_bcrypt import Bcrypt

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime, timedelta

app = Flask(__name__)

#for removing FSADeprecationWarning
SQLALCHEMY_TRACK_MODIFICATIONS = False


#for the form:
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from application import routes