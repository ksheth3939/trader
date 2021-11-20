import numpy as np
import pandas as pd

def RSI_Adj(df,n, comp = None): 
  def rma(x, n, y0):
    a = (n-1) / n
    ak = a**np.arange(len(x)-1, -1, -1)
    return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

  if not comp:
    change = df['Adj Close'].diff()
  else:
    change = df[comp]['Adj Close'].diff()
  
  gain = change.mask(change < 0, 0.0)
  loss = -change.mask(change > 0, -0.0)
  avg_gain = rma(gain[n+1:].to_numpy(), n, np.nansum(gain.to_numpy()[:n+1])/n)
  avg_loss = rma(loss[n+1:].to_numpy(), n, np.nansum(loss.to_numpy()[:n+1])/n)
  avg_loss =np.where(avg_loss == 0, 0.000001, avg_loss)
  # if avg_loss == 0:
  #   df['RSI Adj'] = 100
  # else:
  if not comp:
    df['RSI Adj'] = 100 - (100 / (1 + (avg_gain / avg_loss)))
  else:
    df.loc[:, (comp, 'RSI Adj')] = 100 - (100 / (1 + (avg_gain / avg_loss)))
  # return df

def MACD(df, fast, slow, signal, comp = None):
  if not comp:
    ex1 = df['Adj Close'].ewm(span = fast, adjust = False).mean()
    ex2 = df['Adj Close'].ewm(span = slow, adjust = False).mean()
    df['MACD'] = ex1 - ex2
    df['Signal'] = df['MACD'].ewm(span = signal, adjust = False).mean()

  else:
    ex1 = df[comp]['Adj Close'].ewm(span = fast, adjust = False).mean()
    ex2 = df[comp]['Adj Close'].ewm(span = slow, adjust = False).mean()
    df.loc[:, (comp, 'MACD')] = ex1 - ex2
    df.loc[:, (comp, 'Signal')] = df[comp]['MACD'].ewm(span = signal, adjust = False).mean()

def Stochastic(df, w, m, comp = None):
  if not comp:
    high14 = df['High'].rolling(window = w).max()
    low14 = df['Low'].rolling(window = w).min()
    df['%K'] = 100*(df['Adj Close'] - low14)/(high14 - low14)
    df['%D'] = df['%K'].rolling(window = m).mean()

  else:
    high14 = df[comp]['High'].rolling(window = w).max()
    low14 = df[comp]['Low'].rolling(window = w).min()
    df.loc[:, (comp, '%K')] = 100*(df[comp]['Adj Close'] - low14)/(high14 - low14)
    df.loc[:, (comp, '%D')] = df[comp]['%K'].rolling(window = m).mean()   

# RSI_Adj(df,14)
# MACD(df,12,26,9)
# Stochastic(df,14,3)

# df
