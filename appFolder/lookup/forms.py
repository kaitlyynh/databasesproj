from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
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

    username = StringField(label='User Name:', validators=[Length(2,30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(1,6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class ClearLogsButtonForm(FlaskForm):
    submit = SubmitField(label='Clear Log')

class AddAnOfficerForm(FlaskForm):
    firstname1 = StringField(label="Enter a firstname: ", validators=[DataRequired(), Length(1, 10)])
    lastname1 = StringField(label="Enter a lastname: ", validators=[DataRequired(), Length(1,15)])
    precinct = StringField(label="Enter a precinct: ", validators=[DataRequired(), Length(1,4)])
    badge = StringField(label="Enter a badge #: ", validators=[DataRequired(), Length(1,14)])
    phone = StringField(label="Enter a phone #: ", validators=[DataRequired(), Length(1,10)])
    status = StringField(label="Enter a status A/I: ", validators=[DataRequired(), Length(1,1)])
    submit = SubmitField(label='Add an Officer to the System')

class AddACriminalForm(FlaskForm):
    firstname2 = StringField(label="Enter a firstname: ", validators=[DataRequired(), Length(1,10)])
    lastname2 = StringField(label="Enter a lastname: ", validators=[DataRequired(), Length(1,15)])
    street = StringField(label="Enter a street: ", validators=[DataRequired(), Length(1,30)])
    city = StringField(label="Enter a city: ", validators=[DataRequired(), Length(1,20)])
    state = StringField(label="Enter a state: ", validators=[DataRequired(), Length(1,2)])
    zip = StringField(label="Enter a zipcode: ", validators=[DataRequired(), Length(1,5)])
    phone = StringField(label="Enter a phone #: ", validators=[DataRequired(), Length(1,10)])
    v_stat = StringField(label="Enter a violation status N/Y: ", validators=[DataRequired(), Length(1,1)])
    p_stat = StringField(label="Enter a probation status N/Y: ", validators=[DataRequired(), Length(1,1)])
    submit = SubmitField(label='Add a Criminal to the System')

class DeleteAnOfficerForm(FlaskForm):
    firstname3 = StringField(label="Enter a firstname: ", validators=[DataRequired()])
    lastname3 = StringField(label="Enter a lastname: ", validators=[DataRequired()])
    submit = SubmitField(label='Delete an Officer from the System')

class DeleteACriminalForm(FlaskForm):
    firstname4 = StringField(label="Enter a firstname: ", validators=[DataRequired()])
    lastname4 = StringField(label="Enter a lastname: ", validators=[DataRequired()])
    submit = SubmitField(label='Delete a Criminal from the System')


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

class CrimeSearchForm(FlaskForm):
    crime_id=StringField(label="Enter a Case ID: ")
    submit = SubmitField(label='Begin search for case')

class OfficerUpdateForm(FlaskForm):
    id1 = StringField(label="Enter Officer ID to edit")
    columns1 = ['Last', 'First', 'Precinct', 'Badge', 'Phone', 'Status']
    target1 = SelectField(label="Pick a column to edit", choices = columns1)
    new_data1 = StringField(label="Enter data to populate this column with")
    submit1 = SubmitField(label="Submit")

class CriminalUpdateForm(FlaskForm):
    id2 = StringField(label="Enter Officer ID to edit")
    columns2 = ['Last', 'First', 'Street', 'City', 'State', 'Zip', 'Phone', 'Violation Status', 'Probation Status']
    target2 = SelectField(label="Pick a column to edit", choices = columns2)
    new_data2 = StringField(label="Enter data to populate this column with")
    submit2 = SubmitField(label="Submit")
