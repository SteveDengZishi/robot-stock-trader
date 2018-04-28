from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import SignupForm, LoginForm, UpdateForm
import numpy as np
import pandas as pd
import zipline
from datetime import datetime
from six import viewkeys
from zipline.api import (
    attach_pipeline,
    date_rules,
    order_target_percent,
    pipeline_output,
    record,
    schedule_function,
)
from zipline.finance import commission, slippage
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import RSI
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as off
import plotly.tools as tls

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

    def run(self, start, end, capital):
        return zipline.run_algorithm(
            start=start,
            end=end,
            initialize=initialize,
            capital_base=capital,
            handle_data=None,
            before_trading_start=before_trading_start
        )

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
        # df = setup_zipline()
        # contentP = plot_portfolio(df)
        # contentS = plot_returns(df)
        # return render_template("portfolio.html", contentP=contentP, contentS=contentS)
        return render_template("portfolio.html")

@app.route("/backtest", methods = ['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        return "Under construction"
    else:
        df = setup_zipline()
        contentP = plot_portfolio(df)
        contentS = plot_returns(df)
        return render_template("backtest.html", contentP=contentP, contentS=contentS)

def make_pipeline():
    rsi = RSI()
    return Pipeline(
        columns={
            'longs': rsi.top(3),
            'shorts': rsi.bottom(3),
        },
    )


def rebalance(context, data):

    # Pipeline data will be a dataframe with boolean columns named 'longs' and
    # 'shorts'.
    pipeline_data = context.pipeline_data
    all_assets = pipeline_data.index

    longs = all_assets[pipeline_data.longs]
    shorts = all_assets[pipeline_data.shorts]

    record(universe_size=len(all_assets))

    # Build a 2x-leveraged, equal-weight, long-short portfolio.
    one_third = 1.0 / 3.0
    for asset in longs:
        order_target_percent(asset, one_third)

    for asset in shorts:
        order_target_percent(asset, -one_third)

    # Remove any assets that should no longer be in our portfolio.
    portfolio_assets = longs | shorts
    positions = context.portfolio.positions
    for asset in viewkeys(positions) - set(portfolio_assets):
        # This will fail if the asset was removed from our portfolio because it
        # was delisted.
        if data.can_trade(asset):
            order_target_percent(asset, 0)


def initialize(context):
    attach_pipeline(make_pipeline(), 'my_pipeline')

    # Rebalance each day.  In daily mode, this is equivalent to putting
    # `rebalance` in our handle_data, but in minute mode, it's equivalent to
    # running at the start of the day each day.
    schedule_function(rebalance, date_rules.every_day())

    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def before_trading_start(context, data):
    context.pipeline_data = pipeline_output('my_pipeline')

def setup_zipline():
    investment = session['investment'][1:-3]
    capital = ""
    for ch in investment:
        if ch.isdigit():
            capital+=ch

    capital = float(capital)
    zp = Zipliner.getInstance()
    start = pd.to_datetime('2017-01-01').tz_localize('US/Eastern')
    end = pd.to_datetime('2017-05-01').tz_localize('US/Eastern')
    df = zp.run(start, end, capital)
    return df

def get_fig(data, layout):
    fig = dict(data=data, layout=layout)
    content = off.plot(fig, output_type='div')
    return content

def plot_portfolio(df):
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

def plot_returns(df):
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
