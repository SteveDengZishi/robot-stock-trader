from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField

class SignupForm(Form):
	risks = [('Volatile', 'Volatile, High risk with high reward'),('Moderate', 'Moderate, Move at a relatively steady pace'),('Safe', 'Safe, Move little and minimize risk')]
	username = StringField('Username')
	email = StringField('Email')
	password = PasswordField('Enter your password')
	password1 = PasswordField('Re-type your password')
	investment = IntegerField('Enter your investment in USD')
	riskLevel = SelectField('Select the level of risk you can afford', choices=risks)
	submit = SubmitField('Get Started')