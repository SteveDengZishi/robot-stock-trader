import numpy as np
from zipline.api import set_slippage, set_commission, order, symbol
from zipline.finance import slippage, commission

def initialize(context):
    # http://money.usnews.com/funds/etfs/rankings/small-cap-funds
    context.stocks = [symbol('SLY'),symbol('EES'),symbol('SCHA'),symbol('IJR'),symbol('PSCH'),symbol('VB'),symbol('VTWO'),symbol('IWM'),symbol('SCHC'),symbol('JKJ')]
    context.m = len(context.stocks)
    context.price = {}
    context.b_t = np.ones(context.m) / context.m
    context.eps = 2.5  #change epsilon here
    context.init = False

    set_slippage(slippage.VolumeShareSlippage(volume_limit=0.25,price_impact=0))
    set_commission(commission.PerShare(cost=0))

def handle_data(context, data):

    if get_avg(data,context.stocks[0]) == None:
       return

    if not context.init:
        rebalance_portfolio(context, data, context.b_t)
        context.init = True
        return

    m = context.m

    x_tilde = np.zeros(m)

    b = np.zeros(m)

    # find relative moving average price for each security
    for i, stock in enumerate(context.stocks):
        price = data[stock].price
        x_tilde[i] = get_avg(data,stock)/price

    ###########################
    # Inside of OLMAR (algo 2)

    x_bar = x_tilde.mean()

    # Calculate terms for lambda (lam)
    dot_prod = np.dot(context.b_t, x_tilde)
    num = context.eps - dot_prod
    denom = (np.linalg.norm((x_tilde-x_bar)))**2

    # test for divide-by-zero case
    if denom == 0.0:
        lam = 0 # no portolio update
    else:
        lam = max(0, num/denom)

    b = context.b_t + lam*(x_tilde-x_bar)

    b_norm = simplex_projection(b)

    rebalance_portfolio(context, data, b_norm)

    # update portfolio
    context.b_t = b_norm

    #log.debug(b_norm)

@batch_transform(refresh_period=1, window_length=5) #set globals R_P & W_L above
def get_avg(datapanel,sid):
    prices = datapanel['price']
    avg = prices[sid].mean()
    return avg

def rebalance_portfolio(context, data, desired_port):
    #rebalance portfolio
    current_amount = np.zeros_like(desired_port)
    desired_amount = np.zeros_like(desired_port)

    if not context.init:
        positions_value = context.portfolio.starting_cash
    else:
        positions_value = context.portfolio.positions_value + context.portfolio.cash

    for i, stock in enumerate(context.stocks):
        current_amount[i] = context.portfolio.positions[stock].amount
        desired_amount[i] = desired_port[i]*positions_value/data[stock].price

    diff_amount = desired_amount - current_amount

    for i, stock in enumerate(context.stocks):
        order(stock, diff_amount[i]) #order_stock

def simplex_projection(v, b=1):
    """Projection vectors to the simplex domain

Implemented according to the paper: Efficient projections onto the
l1-ball for learning in high dimensions, John Duchi, et al. ICML 2008.
Implementation Time: 2011 June 17 by Bin@libin AT pmail.ntu.edu.sg
Optimization Problem: min_{w}\| w - v \|_{2}^{2}
s.t. sum_{i=1}^{m}=z, w_{i}\geq 0

Input: A vector v \in R^{m}, and a scalar z > 0 (default=1)
Output: Projection vector w

:Example:
>>> proj = simplex_projection([.4 ,.3, -.4, .5])
>>> print proj
array([ 0.33333333, 0.23333333, 0. , 0.43333333])
>>> print proj.sum()
1.0

Original matlab implementation: John Duchi (jduchi@cs.berkeley.edu)
Python-port: Copyright 2012 by Thomas Wiecki (thomas.wiecki@gmail.com).
"""

    v = np.asarray(v)
    p = len(v)

    # Sort v into u in descending order
    v = (v > 0) * v
    u = np.sort(v)[::-1]
    sv = np.cumsum(u)

    rho = np.where(u > (sv - b) / np.arange(1, p+1))[0][-1]
    theta = np.max([0, (sv[rho] - b) / (rho+1)])
    w = (v - theta)
    w[w<0] = 0
    return w
