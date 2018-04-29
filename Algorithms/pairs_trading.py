import talib as ta
from talib import MA_Type
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import pytz
import zipline
import zipline.utils.factory as factory
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo
from zipline.api import order, symbol, get_order, record
import statsmodels.tsa.stattools as ts
from zipline.utils.run_algo import load_extensions
import os

def initialize(context):
    context.stock_1 = context.symbol(sec1)
    context.stock_2 = context.symbol(sec2)
    context.days = 150
    context.BB_over = False
    context.BB_under = False
    context.long_converg = False
    context.long_diverg = False

def handle_data(context, data):
  try:
    trailing_window_1 = data.history(context.stock_1, 'price', context.days, '1d')
    trailing_window_2 = data.history(context.stock_2, 'price', context.days, '1d')
    trailing_ratio = trailing_window_1/trailing_window_2
  except:
    return

  if (trailing_window_1[-1] >= trailing_window_2[-1]):
    upper_stock = context.stock_1
    lower_stock = context.stock_2
  else:
    upper_stock = context.stock_2
    lower_stock = context.stock_1

  coint = ts.coint(trailing_window_1,trailing_window_2)
  upper, middle, lower = ta.BBANDS(trailing_ratio.values, timeperiod=20, nbdevup=2, nbdevdn=2)

  crossover_top = False
  crossover_bottom = False

  #Setting flags
  if(trailing_ratio[-1] > upper[-1]):
        context.BB_over = True

  if(trailing_ratio[-1] < lower[-1]):
        context.BB_under = True

  if(trailing_ratio[-1] < upper[-1] and context.BB_over):
        context.BB_over = False
        crossover_top = True

  if(trailing_ratio[-1] > lower[-1] and context.BB_under):
        context.BB_under = False
        crossover_bottom = True

  #Wipe away any extraneous positions and orders
  if (not (context.long_converg or context.long_diverg)):
        context.order_target(context.stock_1, 0)
        context.order_target(context.stock_2, 0)

  #Trading Logic
  if(crossover_top and not (context.long_converg or context.long_diverg)):
        context.order_target_percent(upper_stock, -.5)
        context.order_target_percent(lower_stock, .5)
        context.long_converg = True

  elif(crossover_bottom and not (context.long_converg or context.long_diverg)):
        context.order_target_percent(upper_stock, .5)
        context.order_target_percent(lower_stock, -.5)
        context.long_diverg = True

  if(context.long_converg and trailing_ratio[-1] <= middle[-1]):
       context.order_target(upper_stock, 0)
       context.order_target(lower_stock, 0)
       context.long_converg = False
       context.long_diverg = False

  elif(context.long_diverg and trailing_ratio[-1] >= middle[-1]):
       context.order_target(upper_stock, 0)
       context.order_target(lower_stock, 0)
       context.long_converg = False
       context.long_diverg = False

  record(security_1=trailing_window_1[-1],
        security_2=trailing_window_2[-1],
        coint = coint[0],
        ratio = trailing_ratio[-1],
        up = upper[-1],
        mid = middle[-1],
        lo = lower[-1],
        long_converg = context.long_converg,
        long_diverg = context.long_diverg)
