from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField

class SignupForm(Form):
	risks = ['Volatile, High risk with high reward','Moderate, Move at a relatively steady pace','Safe, Move little and minimize risk']
	username = StringField('Username')
	email = StringField('Email')
	password = PasswordField('Password')
	password1 = PasswordField('Re-type Password')
	investment = IntegerField('Investment Amount in USD')
	riskLevel = SelectField('Select the level of risk you can afford', choices=risks)
	submit = SubmitField('Get Started')