from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import StringIO
import zipline
import datetime
from zipline.api import order, record, symbol

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

def initialize(context):
    pass

def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))

def make_fig(perf):
    fig = Figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value')
    # ax2 = plt.subplot(112, sharex=ax1)
    # perf.AAPL.plot(ax=ax2)
    # ax2.set_ylabel('AAPL stock price')
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/", methods = ['GET', 'POST'])
def login():
    form = SignupForm()
    if(request.method == 'POST'):
	if form.validate() == False:
	    return render_template("login.html", form=form)
	else:
	    risk_level = form.riskLevel.data
	    capex = form.investment.data
	    if(risk_level == 'Volatile'):
                risk_level_int = 0
            if(risk_level == 'Moderate'):
                risk_level_int = 1
            if(risk_level == 'Safe'):
                risk_level_int = 2
            newUser = User(form.username.data, form.email.data, form.password.data, form.investment.data, risk_level_int)
            db.session.add(newUser)
            db.session.commit()
            start = datetime.date(2015, 1, 1)
            end = datetime.date(2017, 1, 1)
            perf = zipline.run_algorithm(start, end, initialize, capex, handle_data)
            myplot = make_fig(perf)
            return render_template("portfolio.html", myplot=myplot)
	else:
	    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
