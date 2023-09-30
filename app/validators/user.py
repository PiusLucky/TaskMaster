from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])

class UserForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    