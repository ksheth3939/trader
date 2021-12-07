import pandas as pd
import numpy as np
import robin_stocks.robinhood as robin
import yfinance as yf
import datetime as dt
import indicators
import credentials
import pyotp
import pickle
from csv import writer

companies=list(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'])

def json_to_list(json):
  tim = dt.datetime.strptime(json['begins_at'], '%Y-%m-%dT%H:%M:%SZ') - dt.timedelta(hours = 5)
  return [json['symbol'], tim, float(json['close_price']), int(json['volume'])]

def get_data(comp):
  data = robin.stocks.get_stock_historicals(comp, interval='hour', span='3month', bounds='regular', info=None)
  data = list(map(json_to_list, data))
  df = pd.DataFrame(data, columns = ['Ticker','Timestamp', 'Adj Close', 'Volume'])

  data = float(robin.stocks.get_latest_price(comp)[0])
  df = df.append({'Ticker' : comp, 'Timestamp' : 0, 'Adj Close' : data, 'Volume': 0}, ignore_index=True)
  indicators.RSI_Adj(df, 14)
  indicators.MACD(df,12,26,9)
  indicators.Stochastic(df,14,3)
  return df

def trade():
  totp = pyotp.TOTP(credentials.mfa).now()
  robin.login(credentials.username, credentials.password, mfa_code = totp)
  owned = robin.build_holdings()

  for i, comp in enumerate(companies):

    df = get_data(comp)

    last_row = df.iloc[-1]

    if last_row['RSI Adj'] < 25 and last_row['RSI Adj'] > 0.0 and (comp not in owned):

      print('Buy',comp,last_row['Adj Close'])
      bought = robin.orders.order_buy_market(comp, round(50/last_row['Adj Close'],4), timeInForce='gfd')
      print(bought,'bought',type(bought))

    if last_row['RSI Adj'] > 75 and (comp in owned):

      print('Sell',comp,last_row['Adj Close'])
      sold = robin.orders.order_sell_fractional_by_quantity(comp, owned[comp]['quantity'])
      print(sold, 'sold',type(sold))

  robin.logout()
