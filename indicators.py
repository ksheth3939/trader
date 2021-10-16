import numpy as np
import pandas as pd

def RSI_Adj(df,n): 
  def rma(x, n, y0):
    a = (n-1) / n
    ak = a**np.arange(len(x)-1, -1, -1)
    return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

  change = df['Adj Close'].diff()
  gain = change.mask(change < 0, 0.0)
  loss = -change.mask(change > 0, -0.0)
  avg_gain = rma(gain[n+1:].to_numpy(), n, np.nansum(gain.to_numpy()[:n+1])/n)
  avg_loss = rma(loss[n+1:].to_numpy(), n, np.nansum(loss.to_numpy()[:n+1])/n)
  # df['rs'] =
  avg_loss =np.where(avg_loss == 0, 0.000001, avg_loss)
  # if avg_loss == 0:
  #   df['RSI Adj'] = 100
  # else:
  df['RSI Adj'] = 100 - (100 / (1 + (avg_gain / avg_loss)))
  # return df

def MACD(df, fast, slow, signal):
  ex1 = df['Adj Close'].ewm(span = fast, adjust = False).mean()
  ex2 = df['Adj Close'].ewm(span = slow, adjust = False).mean()
  df['MACD'] = ex1 - ex2
  df['Signal'] = df['MACD'].ewm(span = signal, adjust = False).mean()

def Stochastic(df, w, m):
  high14 = df['High'].rolling(window = w).max()
  low14 = df['Low'].rolling(window = w).min()
  df['%K'] = 100*(df['Adj Close'] - low14)/(high14 - low14)
  df['%D'] = df['%K'].rolling(window = m).mean()
