import robin_stocks.robinhood as robin
import datetime as dt
import credentials
import pyotp
import pickle
import yfinance as yf
from csv import writer

totp = pyotp.TOTP(credentials.mfa).now()
robin.login(credentials.username, credentials.password, mfa_code = totp)
owned = robin.build_holdings()
start_date = '20' + (dt.datetime.now() - dt.timedelta(days = 60)).strftime(('%y-%m-%d'))

stoch_owned = []
with open('stoch.pkl', 'rb') as f:
  stoch_owned = pickle.load(f)

with open('trades.csv', 'a') as f:
  writ = writer(f)

  for comp in owned.keys():
    if comp == 'DAL' or comp == 'XOM':
      continue
    df = yf.download(tickers= comp, start= start_date, interval="1h", threads=False).reset_index()
    last_row = df.iloc[-1]

    sold = robin.orders.order_sell_fractional_by_quantity(comp, owned[comp]['quantity'])
    print(sold, 'sold',type(sold))

    if sold != None and sold != {}:
      writ.writerow([dt.datetime.now() - dt.timedelta(hours=4), comp, 'SELL',sold['quantity'], float(sold['quantity']) * last_row['Adj Close'],last_row['Adj Close'],'RSI'])


  robin.logout()    

with open('stoch.pkl', 'wb') as f:
  pickle.dump([],f)


f.close()
