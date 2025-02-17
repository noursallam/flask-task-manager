from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField    ,IntegerField
from wtforms.fields import DateField  # Import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import date  # Import date for default value

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    deadline = DateField('Deadline', validators=[DataRequired()], default=date.today)  # Use DateField and set default to today
    Priority = IntegerField('Priority')
    submit = SubmitField('Create Task')
    
    