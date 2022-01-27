# Raw Package
import numpy as np
import pandas as pd

#Data Source
from yahoofinancials import YahooFinancials
import yfinance as yf
#Data viz
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pandas_datareader import data as pdr
import warnings

d={'high':0,
   'low':0,
   'open':0,
   'close':0,
   'volume':0,
   'adj Close':0}

class CM(pd.DataFrame):
    """For init treat this as standard Pandas DataFrame.
        rename: Default to false. Renames columns in standard way.
            d={ 'high':0,
                'low':0,
                'open':0,
                'close':0,
                'volume':0,
                'adj Close':0}
            Use this dict or manually insert the name of your Panda columns that are different from this
    """
    def __init__(self,t):
        super().__init__(t)
        self.drop('date', axis=1).set_index('formatted_date')
        self.k=4
        self.compute_CM()
        return

    def compute_key(self):
        # ricordati di fare il reverse dell'array
        # mk=data['close'].rolling(k).apply(lambda x: x.cumsum().sum() * 2 / k / (k + 1))
        # m3k=data['close'].rolling(3*k).apply(lambda x: x.cumsum().sum() * 2 / 3*k / (3*k + 1))
        weights = np.arange(1, self.k + 1)
        weights3 = np.arange(1, 3 * self.k + 1)
        mk = self['close'].rolling(self.k).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
        m3k = self['close'].rolling(3 * self.k).apply(lambda prices: np.dot(prices, weights3) / weights3.sum(), raw=True)
        momentum = (mk - m3k) / mk

        momentum = (momentum - momentum.min()) / (momentum.max() - momentum.min()) * 100

        temp1 = np.zeros(momentum.values.shape)
        temp2 = np.zeros(momentum.values.shape)
        diffMOM = momentum.diff()
        temp1[np.where(diffMOM > 0)] = diffMOM[diffMOM > 0]
        temp2[np.where(diffMOM < 0)] = diffMOM[diffMOM < 0]

        temp1 = pd.Series(temp1)
        temp1.index = diffMOM.index
        temp2 = pd.Series(temp2)
        temp2.index = diffMOM.index
        diffMOM = pd.Series(diffMOM)

        sumtemp1 = temp1.rolling(5).sum()
        sumtemp2 = temp2.rolling(5).sum()
        abssumdiff = diffMOM.abs().rolling(5).sum()
        aa = ((sumtemp1.shift(1) - (sumtemp1.shift(1) / 5) + temp1) / (
                    abssumdiff.shift(1) - (abssumdiff.shift(1) / 5) + diffMOM.abs()) * 100)
        bb = ((sumtemp2.shift(1) - (sumtemp2.shift(1) / 5) + temp2) / (
                    abssumdiff.shift(1) - (abssumdiff.shift(1) / 5) + diffMOM.abs()) * 100)
        cc = aa - abs(bb)

        self['key'] = cc.ewm(span=3, adjust=True).mean()

        return

    def compute_xtl(self):
        self['L5'] = self['low'].rolling(window=5).min()
        # Create the "H14" column in the DataFrame
        self['H5'] = self['high'].rolling(window=5).max()
        # Create the "%K" column in the DataFrame
        self['%K'] = 100 * ((self['close'] - self['L5']) / (self['H5'] - self['L5']))
        # Create the "%D" column in the DataFrame
        self['%D'] = self['%K'].rolling(3).mean()

        self['xtl'] = self['%D'].rolling(3).apply(lambda prices: np.dot(prices, np.arange(1, 4)) / np.arange(1, 4).sum(),
                                          raw=True)*2 -100

        return

    def compute_CM(self):
        if 'xtl' not in self.keys():
            self.compute_xtl()
        if 'key' not in self.keys():
            self.compute_key()

        self['CM'] = ((self['key'] * 2 + self['xtl']) / 3).rolling(2).apply(lambda prices: np.dot(prices, [1, 2]) / 3,
                                                                            raw=True)



    def visualize(self):
        fig = go.Figure()
        fig.add_trace( go.Candlestick(  x=self.index,
                                        open=self['open'],
                                        high=self['high'],
                                        low=self['low'],
                                        close=self['close'],
                                        name='market_data'))
        fig.show()
        return
        # data=yf.download(stock,start="2004-01-01", end="2014-12-31", interval='1wk' )
        # data.columns=['high','low','open','close','volume','adj Close']


if __name__ == '__main__':
    stock = 'BTC-USD'
    yahoofinancials = YahooFinancials(stock)
    # forse response si può cassare? cioè non aggiungere a self
    response = yahoofinancials.get_historical_price_data(start_date='2020-01-01', end_date='2022-01-24',
                                                                    time_interval='weekly')
    cm=CM(response[stock]['prices'])
