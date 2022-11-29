
from flask import Blueprint

from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, PasswordField, BooleanField, EmailField, SelectField, TelField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
forms = Blueprint('forms', __name__)

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')