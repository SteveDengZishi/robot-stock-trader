from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm
from forms import LoginForm

app = Flask(__name__)

app.secret_key = "development-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skqtsiamfhxtft:32d113d4b722c701dae458160b179e9c3f06cfab6fd5ccd9e31932afcba018b4@ec2-23-21-121-220.compute-1.amazonaws.com:5432/d14f5uhqoad2g'

# heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
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

@app.route("/portfolio", methods = ['GET', 'POST'])
def portfolio():
	if request.method == 'POST':
		return "Under construction"
	else:
		return render_template("portfolio.html")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
	form = SignupForm();

	if request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html", form=form)
		else:
			risk_level = form.riskLevel.data
			if(risk_level == 'Volatile'):
				risk_level_int = 0
			if(risk_level == 'Moderate'):
				risk_level_int = 1
			if(risk_level == 'Safe'):
				risk_level_int = 2
			newUser = User(form.username.data, form.email.data, form.password.data, form.investment.data, risk_level_int)
			db.session.add(newUser)
			db.session.commit()
			return "success!"

	else:
		return render_template("signup.html", form=form)

@app.route("/", methods = ['GET','POST'])
def login():
	form = LoginForm();

	if request.method == 'POST':
		return ("Connecting to DB")

	else:
		return render_template("login.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)
