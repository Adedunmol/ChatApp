from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), validators.email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('This email already taken.Please choose another email')

    def validate_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError('This username already taken.Please choose another username')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), validators.email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
