from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from lookup.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username is taken. Enter a different one.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('This email address is taken. Enter a different one.')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class ButtonForm(FlaskForm):
    submit = SubmitField(label='Press this button')
    
class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class FullNameForm(FlaskForm):
    # firstname = StringField(label="Enter a firstname: ", validators=[DataRequired()])
    # lastname = StringField(label="Enter a lastname: ", validators=[DataRequired()])
    firstname = StringField(label="Enter a firstname: ")
    lastname = StringField(label="Enter a lastname: ")
    submit = SubmitField(label='Begin search for person')