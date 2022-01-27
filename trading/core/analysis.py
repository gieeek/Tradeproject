import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
class Analysis:
    def __init__(self,weekly=pd.DataFrame([]),monthly=pd.DataFrame([]),trim=pd.DataFrame([])):
        self.weekly=weekly
        self.monthly=monthly
        self.trim=trim
        return

    def visualize(self):
        fig=make_subplots(rows=2,cols=1,shared_xaxes=True)
        fig.add_trace(go.Candlestick(x=self.weekly.index,
                                     open=self.weekly['open'],
                                     high=self.weekly['high'],
                                     low=self.weekly['low'],
                                     close=self.weekly['close'],
                                     name='market_data'),row=1,col=1)
        #fig.add_trace(go.Bar(x=self.weekly.index,y=self.weekly['CM']),row=2,col=1)
        #fig.add_trace(go.Bar(x=self.monthly.index,y=self.monthly['CM']), row=2, col=1)

        fig.add_trace(go.Bar(x=self.trim.index, y=self.trim['CM']), row=2, col=1)

        fig.show()
        return
