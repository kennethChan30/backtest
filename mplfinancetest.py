import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import mplfinance as mpf


timeframe = 'daily'
statslist = ['Periods', 'Gross winning trade', 'Gross lossing trade', 'No of winning trade', 'No of lossing trade', 'Percent of winning', 'Max profit', 'Max loss', 'Averge risk to reward','Profit Per Trade', 'Max win streak', ' Max loss streak']
backtesttype = 'resistance_and_support/'
backtestpath = 'drive/MyDrive/Trading/backtest/'
systemdata = backtestpath + 'Data/'
systemoutput = backtestpath +  backtesttype
rawdata = pd.read_csv(timeframe + '.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata['ema5'] = rawdata.iloc[:, 5].ewm(span=5, adjust=False).mean()
rawdata['ema10'] = rawdata.iloc[:, 5].ewm(span=10, adjust=False).mean()
rawdata['ema15'] = rawdata.iloc[:, 5].ewm(span=15, adjust=False).mean()
rawdata['ema65'] = rawdata.iloc[:, 5].ewm(span=65, adjust=False).mean()
rawdata['ema200'] = rawdata.iloc[:, 5].ewm(span=200, adjust=False).mean()
#MACD
MACD_calculate_table = pd.DataFrame(rawdata['time'])
for periods in [12,26]:
  MACD_calculate_table["EMA"+str(periods)] = rawdata.iloc[:, 5].ewm(span=periods, adjust=False).mean()
MACD_calculate_table['MACD'] = round(MACD_calculate_table['EMA12'] - MACD_calculate_table['EMA26'], 3)
MACD_calculate_table['MACD Signal'] = round(MACD_calculate_table['MACD'].rolling(window=9).mean(), 3)
rawdata[['MACD', 'MACD Signal']] = MACD_calculate_table[['MACD', 'MACD Signal']]
print(rawdata.head())
rawdata['date'] = pd.to_datetime(rawdata['date'])
rawdata.set_index('date', inplace=True)
print(rawdata.head())
ewm5 = mpf.make_addplot(rawdata['ema5'], type='line')
ewm10 = mpf.make_addplot(rawdata['ema10'], type='line')
ewm15 = mpf.make_addplot(rawdata['ema15'], type='line')
ewm65 = mpf.make_addplot(rawdata['ema65'], type='line')
ewm200 = mpf.make_addplot(rawdata['ema200'], type='line')
MACD = mpf.make_addplot(rawdata['MACD'], type='bar', panel=1)
MACD_Signal = mpf.make_addplot(rawdata['MACD Signal'], panel=1)
add_plot = [ewm5, ewm10, ewm15, ewm65,ewm200, MACD, MACD_Signal]
mpf.plot(rawdata, type='candle', style='charles', addplot=add_plot, scale_width_adjustment=dict(candle=3))
