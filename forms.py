from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# StringField is used for forms with a String input
# passwordfield used for registering a password
# allows for submitting the form
from wtforms.validators import DataRequired, Length, Email, EqualTo
# Datarequired to make sure field is not empty, Length constraints the lenght
# Email ensures the email entered is valid


class RegistrationForm (FlaskForm):
    # validators are constraints on the username to make sure it's a valid username
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # could potentially add more validators for password like length
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
