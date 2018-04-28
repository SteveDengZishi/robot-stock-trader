from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, DataRequired, NumberRange, EqualTo, Email

class SignupForm(FlaskForm):
	risks = [('Volatile', 'Volatile, High risk with high reward'),('Moderate', 'Moderate, Move at a relatively steady pace'),('Safe', 'Safe, Move little and minimize risk')]
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email("Please enter a vaild email address")])
	password = PasswordField('Enter your password', validators=[DataRequired(), Length(min=6)])
	password1 = PasswordField('Re-type your password', validators=[DataRequired(), Length(min=6), EqualTo(fieldname='password', message='Passwords do not match')])
	investment = IntegerField('Enter your investment in USD', validators=[DataRequired(), NumberRange(min=100)])
	riskLevel = SelectField('Select the level of risk you can afford', choices=risks)
	submit = SubmitField('Get Started')


class LoginForm(FlaskForm):
	username = StringField('Username')
	password = PasswordField('Enter your password')

class UpdateForm(FlaskForm):
	risks = [('Volatile', 'Volatile, High risk with high reward'),('Moderate', 'Moderate, Move at a relatively steady pace'),('Safe', 'Safe, Move little and minimize risk')]
	investment = IntegerField('Update your investment in USD', validators=[DataRequired(), NumberRange(min=100)])
	riskLevel = SelectField('Update the level of risk', choices=risks)