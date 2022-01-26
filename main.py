from trading.core.composite_momentum import CM
from datetime import datetime
import pandas_datareader as web
import yfinance as yf
import nasdaqdatalink
nasdaqdatalink.read_key('.nasdaq/data_link_apikey.txt')
mydata = nasdaqdatalink.get("EOD/AAPL",api_key='sUkyt3uNut7e8JsHzbo8')
print(mydata)
#declare your stock and time frame
stock = 'AAPL'
start_date='2020-01-01'
end_date=datetime.now().strftime('%Y-%m-%d')
#GET data WEEKLY
response = web.DataReader(stock, start="2004-01-01", end="2014-12-31")
weekly=CM(response[stock]['prices'])
#GET data MONTHLY
response = web.DataReader(stock, start="2004-01-01", end="2014-12-31", interval='m')
monthly=CM(response[stock]['prices'])
#GET data TRIM
response = web.DataReader(stock, start="2004-01-01", end="2014-12-31", interval='3mo')
trim=CM(response[stock]['prices'])


trim.visualize()

