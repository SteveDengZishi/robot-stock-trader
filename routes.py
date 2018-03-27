from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm

# from flask.ext.heroku import Heroku

app = Flask(__name__)

app.secret_key = "development-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skqtsiamfhxtft:32d113d4b722c701dae458160b179e9c3f06cfab6fd5ccd9e31932afcba018b4@ec2-23-21-121-220.compute-1.amazonaws.com:5432/d14f5uhqoad2g'

# heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "Users"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(100))
    inv_amount = db.Column(db.Integer)
    risk_level = db.Column(db.Integer)

    def __init__(self, username, email, password, inv_amount, risk_level):
        self.username = username
        self.email = email
        self.password = password
        self.inv_amount = inv_amount
        self.risk_level = risk_level

    def __repr__(self):
        return '<User %r>' % self.username

# Set "homepage" to login.html
@app.route("/", methods = ['GET', 'POST'])
def login():
	form = SignupForm();

	if request.method == 'POST':
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			username = request.form['username']
			email = request.form['Email']
			password = request.form['pwd']
			asset = request.form['Asset']
			risk_level = request.form['Risk Level']
			if(risk_level == 'Volatile'):
				risk_level_int = 0
			if(risk_level == 'Moderate'):
				risk_level_int = 1
			if(risk_level == 'Safe'):
				risk_level_int = 2
			newUser = User(username, email, password, asset, risk_level_int)
			db.session.add(newUser)
			return "success!"

	else:
		return render_template("login.html", form=form)

# Save e-mail to database and send to success page
# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['Email']
#         password = request.form['psw']
#         asset = request.form['Asset']
#         risk_level = request.form['Risk Level']
#
#     if(risk_level == 'Volatile'):
#         risk_level_int = 0
#     if(risk_level == 'Moderate'):
#         risk_level_int = 1
#     if(risk_level == 'Safe'):
#         risk_level_int = 2
#
#     newUser = User(username, email, password, asset, risk_level_int)
#     db.session.add(newUser)
#
#     return render_template('login.html')

if __name__ == "__main__":
	app.run(debug=True)
