from trading.core.composite_momentum import CM
from datetime import datetime
import pandas_datareader as web
import yfinance as yf
import numpy as np

d={ 'high':'High',
    'low':'Low',
    'open':'Open',
    'close':'Close',
    'volume':'Volume',
    'adj Close':'Adj Close'}
index_name='fromatted_date'
#declare your stock and time frame
stock = 'AAPL'
start_date='2020-01-01'
end_date=datetime.now().strftime('%Y-%m-%d')
period='5y'
#GET data WEEKLY
response = yf.download(tickers=[stock],period=period,interval='1wk')
response.rename(str.lower,axis='columns',inplace=True)
weekly=CM(response,**d)
#GET data MONTHLY
response = yf.download(tickers=[stock],period=period,interval='1mo')
response.rename(str.lower,axis='columns',inplace=True)
monthly=CM(response,True,**d)
#GET data TRIM
response = yf.download(tickers=[stock],period=period,interval='3mo')
response.rename(str.lower,axis='columns',inplace=True)
trim=CM(response,True,**d)







