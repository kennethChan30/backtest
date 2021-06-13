import pandas as pd
import numpy as np
import plotly.graph_objects as go
timeframe = 'daily'
statslist = ['Periods', 'Gross winning trade', 'Gross lossing trade', 'No of winning trade', 'No of lossing trade', 'Percent of winning', 'Max profit', 'Max loss', 'Averge risk to reward','Profit Per Trade', 'Max win streak', ' Max loss streak']
backtesttype = 'resistance_and_support/'
backtestpath = 'drive/MyDrive/Trading/backtest/'
systemdata = backtestpath + 'Data/'
systemoutput = backtestpath +  backtesttype
rawdata = pd.read_csv(systemdata + timeframe + '.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata = rawdata.set_index(pd.DatetimeIndex(rawdata['date'].values))
figure = go.Figure(
    data = [
            go.Candlestick(
                x = rawdata.index,
                low = rawdata['low'],
                high = rawdata['high'],
                close = rawdata['close'],
                open = rawdata['open'],
                increasing_line_color = 'green',
                decreasing_line_color = 'red'
            )
    ]
)
figure.show()