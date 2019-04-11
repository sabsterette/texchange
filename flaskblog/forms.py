from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField
from wtforms import SubmitField, BooleanField, TextAreaField, DecimalField
# StringField is used for forms with a String input
# passwordfield used for registering a password
# allows for submitting the form
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# Datarequired to make sure field is not empty, Length constraints the lenght
# Email ensures the email entered is valid
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm (FlaskForm):
    # validators are constraints on the username to make sure it's a valid username
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # could potentially add more validators for password like length
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password')])
    submit = SubmitField('REGISTER')
    #overwrite the validate method for username and email to make suer it's unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken oops!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken oops!')


class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateForm (FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    edition = StringField('Edition')
    authors = StringField('Authors', validators=[DataRequired()])
    price = DecimalField('Price', places=3, validators=[DataRequired()])
    course = StringField('Class Name', validators=[DataRequired()])
    quality = SelectField('Quality', choices=[('Brand New', 'Brand New'), ('Lightly Used', 'Lightly Used'), ('Used', 'Used'), ('Old', 'Old')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=140)])
    submit = SubmitField('Create Item!')

    def validate_price(self, price):
        if isinstance(price.data, str):
            raise ValidationError('Must be a number')


class CreateReview (FlaskForm):
    rating = SelectField('Rating',choices=[(1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')],validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Leave Review!')

    # class UpdateAccountForm (FlaskForm):
    #     # validators are constraints on the username to make sure it's a valid username
    #     username = StringField('Username',
    #                            validators=[DataRequired(), Length(min=2, max=20)])
    #     email = StringField('Email', validators=[DataRequired(), Email()])
    #     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    #     submit = SubmitField('Update')

    #     def validate_username(self, username):
    #         if username.data != current_user.username:
    #             user = User.query.filter_by(username=username.data).first()
    #             if user:
    #                 raise ValidationError('Oops! Username already taken!')

    #     def validate_email(self, email):
    #         if email.data != current_user.email:
    #             user = User.query.filter_by(email=email.data).first()
    #             if user:
    #                 raise ValidationError('Oops! That email is already linked to an account!')

class SearchForm(FlaskForm):
    title=StringField('Title')
    authors=StringField('Author')
    sort_by=SelectField('Sort By: ', choices=[('select one', '--Select One--'), ('price', 'Price'),
        ('classid', 'Class'), ('condition', 'Condition'), ('date', 'Date Posted'),
        ('edition', 'Edition')])
    submit=SubmitField('Search')

class editItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    edition = StringField('Edition')
    authors = StringField('Authors', validators=[DataRequired()])
    price = DecimalField('Price', places=3, validators=[DataRequired()])
    course = StringField('Class Name', validators=[DataRequired()])
    quality = SelectField('Quality', choices=[('Brand New', 'Brand New'), ('Lightly Used', 'Lightly Used'),
    ('Used', 'Used'), ('Old', 'Old')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=140)])
    submit = SubmitField('Update Item')
