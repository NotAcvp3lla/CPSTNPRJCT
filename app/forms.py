from flask_wtf import FlaskForm,Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields import TextField,TextAreaField,SelectField,PasswordField,BooleanField, StringField, SubmitField
from wtforms import validators, ValidationError
import hashlib


class LoginForm(Form):
    user_name = TextField('Username: ', [validators.Required("(Required)")])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember me: ')

class SearchForm(Form):
    search = TextField('Enter Search: ', [validators.Required("(Required)")])

class ProfileForm(Form):
    first_name = TextField('First Name: ', [validators.Required("(Required)")])
    last_name = TextField('Last Name: ', [validators.Required("(Required)")])
    user_name = TextField('Username: ', [validators.Required("(Required)")])
    password = PasswordField('Password: ', validators=[DataRequired()])
    gender = SelectField(label='Gender: ', choices=[("Select Gender", "Select Gender"), ("Male", "Male"), ("Female", "Female")])
    email = TextField('Email: ',[validators.Required("(Required)")])
    role = SelectField(label='Role: ', choices=[("Select Role", "Select Role"), ("Driver", "Driver"), ("Commuter", "Commuter")])
    
    photo= FileField('Profile Photo: ', validators=[
        FileRequired(),
        FileAllowed(['jpg','png','Images Only!'])])