from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import SignupForm, LoginForm, UpdateForm
import numpy as np
import pandas as pd
import zipline
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as off
import plotly.tools as tls
import Algorithms.momentum_based as high_risk
import Algorithms.momentum_based as mid_risk
import Algorithms.momentum_based as low_risk


app = Flask(__name__)
bcrypt = Bcrypt(app)

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

class Zipliner:
    __instance = None
    plotP = ['', '', '', '']
    plotR = ['', '', '', '']
    dates = (
                pd.to_datetime('2016-07-01').tz_localize('US/Eastern'),
                pd.to_datetime('2016-10-01').tz_localize('US/Eastern'),
                pd.to_datetime('2017-01-01').tz_localize('US/Eastern'),
                pd.to_datetime('2017-04-01').tz_localize('US/Eastern'),
                pd.to_datetime('2017-07-01').tz_localize('US/Eastern')
            )

    def run(self, capital, risk_level, quarter):
        start = dates[quarter-1]
        end = dates[quarter]
        df = None

        if (risk_level == 2):
            df = zipline.run_algorithm(
                start=start,
                end=end,
                initialize=low_risk.initialize,
                capital_base=capital,
                handle_data=None,
                before_trading_start=low_risk.before_trading_start
            )
        elif (risk_level == 1):
            df = zipline.run_algorithm(
                start=start,
                end=end,
                initialize=mid_risk.initialize,
                capital_base=capital,
                handle_data=mid_risk.handle_data,
                before_trading_start=None
            )
        elif (risk_level == 0):
            df = zipline.run_algorithm(
                start=start,
                end=end,
                initialize=high_risk.initialize,
                capital_base=capital,
                handle_data=high_risk.handle_data,
                before_trading_start=None
            )

        return df

    def get_fig(self, data, layout):
        fig = dict(data=data, layout=layout)
        content = off.plot(fig, output_type='div')
        return content

    def plot_portfolio(self, df):
        trace0 = go.Scatter(
            x=df.columns[0],
            y=df['portfolio_value'],
            name='Current Portfolio',
            line = dict(color = ('rgb(22, 96, 167)'), width = 1)
        )

        layout = dict(title = 'Portfolio Value 2016',
                  xaxis = dict(title = 'Days Since 1/1/2015'),
                  yaxis = dict(title = 'Net Value (USD)'),
                 )

        data = [trace0]
        return get_fig(data, layout)

    def plot_returns(self, df):
        trace0 = go.Scatter(
            x=df.columns[0],
            y=df['algorithm_period_return']*100,
            name='Algorithm',
            line = dict(color = ('rgb(22, 96, 167)'), width = 1)
        )

        trace1 = go.Scatter(
            x=df.columns[0],
            y=df['benchmark_period_return']*100,
            name='IEX Benchmark',
            line = dict(color = ('rgb(205, 12, 24)'), width = 1)
        )

        layout = dict(title = 'Portfolio Period Returns 2016',
                  xaxis = dict(title = 'Days Since 1/1/2015'),
                  yaxis = dict(title = 'Returns (%)'),
                 )

        data = [trace0, trace1]
        return get_fig(data, layout)

    def getPlot(self, quarter, type_p):
        quarter = quarter - 1
        if (plotP[quarter] == '' or plotR[quarter] == ''):
            risk_level = session['risk_level']
            investment = session['investment'][1:-3]
            capital = ""
            for ch in investment:
                if ch.isdigit():
                    capital+=ch

            capital = float(capital)
            df = run(capital, risk_level, quarter)
            plotP[quarter] = plot_portfolio(df)
            plotR[quarter] = plot_returns(df)

        if (type_p == 1):
            return plotP[quarter]
        else:
            return plotR[quarter]

    def resetPlots(self):
        for i in range(0,4):
            plotP[i] = ''
            plotR[i] = ''

    @staticmethod
    def getInstance():
        if Zipliner.__instance == None:
            Zipliner()
        try:
            zipline.data.bundles.load('quantopian-quandl')
        except:
            zipline.data.bundles.ingest('quantopian-quandl')
        return Zipliner.__instance

    def __init__(self):
        if Zipliner.__instance != None:
            raise Exception("should be singleton")
        else:
            Zipliner.__instance = self
            zipline.data.bundles.ingest('quantopian-quandl')



@app.route("/portfolio", methods = ['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        return "Under construction"
    else:
        zp = Zipliner.getInstance()
        contentP = zp.getPlot(1, 1)
        contentS = zp.getPlot(1, 2)
        return render_template("portfolio.html", contentP=contentP, contentS=contentS)


@app.route("/changePref", methods = ['GET', 'POST'])
def changePref():
    form = UpdateForm();
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("changePref.html", form=form)
        else:
            risk_level = form.riskLevel.data
            if(risk_level == 'Volatile'):
                risk_level_int = 0
            elif(risk_level == 'Moderate'):
                risk_level_int = 1
            elif(risk_level == 'Safe'):
                risk_level_int = 2
            userName = session['username']
            change_user = User.query.filter_by(username=userName).first()
            change_user.inv_amount = form.investment.data
            change_user.risk_level = risk_level_int
            db.session.commit()
            change_user = User.query.filter_by(username=userName).first()
            session['username'] = change_user.username
            session['email'] = change_user.email
            session['investment'] = change_user.inv_amount
            session['risk_level'] = change_user.risk_level
            return redirect(url_for('portfolio'))
    else:
        return render_template("changePref.html", form=form)

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
            elif(risk_level == 'Moderate'):
                risk_level_int = 1
            elif(risk_level == 'Safe'):
                risk_level_int = 2
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            newUser = User(form.username.data, form.email.data, hashed_password, form.investment.data, risk_level_int)
            db.session.add(newUser)
            db.session.commit()

            session['username'] = newUser.username
            session['email'] = newUser.email
            session['investment'] = newUser.inv_amount
            session['risk_level'] = newUser.risk_level
            zp = Zipliner.getInstance()
            zp.resetPlots()
            return redirect(url_for('portfolio'))
    else:
        return render_template("signup.html", form=form)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('login'))

@app.route("/", methods = ['GET','POST'])
def login():
    form = LoginForm();
    if request.method == 'POST':
        userName = form.username.data
        password = form.password.data
        userLogin = User.query.filter_by(username=userName).first()
        if(userLogin != None):
            hashed_password = userLogin.password
            if(bcrypt.check_password_hash(hashed_password, password)):
                session['username'] = userName
                session['email'] = userLogin.email
                session['investment'] = userLogin.inv_amount
                session['risk_level'] = userLogin.risk_level
                return redirect(url_for('portfolio'))
        else:
            return redirect(url_for('login'))

    else:
        return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
