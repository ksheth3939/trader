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

def trade():
  totp = pyotp.TOTP(credentials.mfa).now()
  robin.login(credentials.username, credentials.password, mfa_code = totp)
  owned = robin.build_holdings()

  start_date = '20' + (dt.datetime.now() - dt.timedelta(days = 60)).strftime(('%y-%m-%d'))
  # print(start_date)
  stoch_owned = []
  with open('stoch.pkl', 'rb') as f:
    stoch_owned = pickle.load(f)

  with open('trades.csv', 'a') as f:
    writ = writer(f)

    # bought = 0
    for i, comp in enumerate(companies):
      print(comp)
      df = yf.download(tickers= comp, start= start_date, interval="1h", threads=False).reset_index()
      df = df[['Adj Close','High','Low','Volume']]

      indicators.RSI_Adj(df,14)
      indicators.MACD(df,12,26,9)
      indicators.Stochastic(df,14,3)
      # print(len(df))
      # print(i) if i%25 == 0 else _

      stoch_buy = False
      for index, row in df[::-1].iterrows():
        if row['%K'] < 20 and row['%D'] < 20:
          stoch_buy = True
          break
        elif row['%K'] > 80 or row['%D'] > 80:
          stoch_buy = False
          break

      last_row = df.iloc[-1]
      print(last_row['RSI Adj'])
      if stoch_buy and last_row['RSI Adj'] > 50 and last_row['MACD'] > last_row['Signal'] and (comp not in stoch_owned):
        #buy
        cost = last_row['Adj Close']
        #writ.writerow([dt.datetime.now() - dt.timedelta(hours=4), comp, 'BUY', last_row['RSI Adj'], 0, cost,'Stoch'])
        stoch_owned.append(comp)
        # print(last_row['Adj Close'])
        # print(bought)

      if last_row['RSI Adj'] < 25 and last_row['RSI Adj'] > 0.0 and (comp not in owned):

        print('Buy',comp,last_row['Adj Close'])
        #bought = robin.orders.order_buy_market(comp, round(50/last_row['Adj Close'],4), timeInForce='gfd')
        #print(bought,'bought',type(bought))
        #if bought != None and bought != {}:
        #  writ.writerow([dt.datetime.now() - dt.timedelta(hours=4), comp, 'BUY',bought['quantity'], float(bought['quantity']) * last_row['Adj Close'],last_row['Adj Close'],'RSI'])
        


      stoch_sell = False
      for index,row in df[::-1].iterrows():
        if row['%K'] > 80 and row['%D'] > 80:
          stoch_sell = True
          break
        elif row['%K'] < 20 or row['%D'] < 20:
          stoch_sell = False
          break

      if (comp in stoch_owned and stoch_sell and last_row['RSI Adj'] < 50 and last_row['MACD'] < last_row['Signal']):
        #sell
        cost = last_row['Adj Close']
        #writ.writerow([dt.datetime.now() - dt.timedelta(hours=4), comp, 'SELL', last_row['RSI Adj'], 0, cost,'Stoch'])
        stoch_owned.remove(comp)
        
      if last_row['RSI Adj'] > 75 and (comp in owned):

        print('Sell',comp,last_row['Adj Close'])
        #sold = robin.orders.order_sell_fractional_by_quantity(comp, owned[comp]['quantity'])
        #print(sold, 'sold',type(sold))
        #if sold != None and sold != {}:
        #  writ.writerow([dt.datetime.now() - dt.timedelta(hours=4), comp, 'SELL',sold['quantity'], float(sold['quantity']) * last_row['Adj Close'],last_row['Adj Close'],'RSI'])

        

  

    robin.logout()

  with open('stoch.pkl', 'wb') as f:
    pickle.dump(stoch_owned,f)

  f.close()
