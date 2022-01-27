from trading.core.composite_momentum import CM
from trading.utils.utils import rename_df
from datetime import datetime
import pandas_datareader as web
import yfinance as yf

d={ 'date':'Date',
    'high':'High',
    'low':'Low',
    'open':'Open',
    'close':'Close',
    'volume':'Volume',
    'adj Close':'Adj Close'}

#declare your stock and time frame
stock = 'AAPL'
start_date='2020-01-01'
end_date=datetime.now().strftime('%Y-%m-%d')
#GET data WEEKLY
response = rename_df(yf.download(tickers=[stock],period='max',interval='1wk'),**d)
print(response)
weekly=CM(response)
#GET data MONTHLY
response = rename_df(yf.download(tickers=[stock],period='max',interval='1mo'),**d)
monthly=CM(response)
#GET data TRIM
response = rename_df(yf.download(tickers=[stock],period='max',interval='3mo'),**d)
trim=CM(response)


trim.visualize()

