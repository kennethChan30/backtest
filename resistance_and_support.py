!pip install mpl_finance
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from datetime import datetime
timeframe = 'daily'
statslist = ['Periods', 'Gross winning trade', 'Gross lossing trade', 'No of winning trade', 'No of lossing trade', 'Percent of winning', 'Max profit', 'Max loss', 'Averge risk to reward','Profit Per Trade', 'Max win streak', ' Max loss streak']
backtesttype = 'resistance_and_support/'
backtestpath = 'drive/MyDrive/Trading/backtest/'
systemdata = backtestpath + 'Data/'
systemoutput = backtestpath +  backtesttype
rawdata = pd.read_csv(systemdata + timeframe + '.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
date_format = []
for i in rawdata.index:
  date_format.append(datetime.strptime(rawdata['date'][i], "%Y.%m.%d"))
rawdata['Date'] = date_format
rawdata['Date'] = rawdata['Date'].apply(mpl_dates.date2num)
df = rawdata.loc[:,['Date', 'open', 'high', 'low', 'close']]
s =  np.mean(df['high'] - df['low'])
pivot = []


for i in range(2, len(rawdata)-2):
  if rawdata['high'][i-2]<rawdata['high'][i-1] and rawdata['high'][i-1]<rawdata['high'][i] and rawdata['high'][i+2]<rawdata['high'][i+1] and rawdata['high'][i+1]<rawdata['high'][i]:
    l = rawdata.loc[i]['high']
    if np.sum([abs(l-x) < s  for x in pivot]) == 0:
      pivot.append((i, l))
  if rawdata['low'][i-2]>rawdata['low'][i-1] and rawdata['low'][i-1]>rawdata['low'][i] and rawdata['low'][i+2]>rawdata['low'][i+1] and rawdata['low'][i+1]>rawdata['low'][i]:
    l = rawdata.loc[i]['low']
    if np.sum([abs(l-x) < s  for x in pivot]) == 0:
      pivot.append((i, l))
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)
fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
fig.tight_layout()

for p in pivot:
  plt.hlines(p[1],xmin=df['Date'][p[0]], xmax=max(df['Date']),colors='blue')
fig.show()
