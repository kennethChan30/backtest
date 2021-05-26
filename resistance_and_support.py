import pandas as pd
timeframe = 'daily'
statslist = ['Periods', 'Gross winning trade', 'Gross lossing trade', 'No of winning trade', 'No of lossing trade', 'Percent of winning', 'Max profit', 'Max loss', 'Averge risk to reward','Profit Per Trade', 'Max win streak', ' Max loss streak']
backtesttype = 'resistance_and_support/'
backtestpath = 'drive/MyDrive/Trading/backtest/'
systemdata = backtestpath + 'Data/'
systemoutput = backtestpath +  backtesttype
rawdata = pd.read_csv(systemdata + timeframe + '.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
pivot = []
date = []

for i in range(2, len(rawdata)-2):
  if rawdata['high'][i-2]<rawdata['high'][i-1] and rawdata['high'][i-1]<rawdata['high'][i] and rawdata['high'][i+2]<rawdata['high'][i+1] and rawdata['high'][i+1]<rawdata['high'][i]:
    pivot.append(rawdata.loc[i]['high'])
    date.append(rawdata.loc[i]['date'])
  if rawdata['low'][i-2]>rawdata['low'][i-1] and rawdata['low'][i-1]>rawdata['low'][i] and rawdata['low'][i+2]>rawdata['low'][i+1] and rawdata['low'][i+1]>rawdata['low'][i]:
    pivot.append(rawdata.loc[i]['high'])
    date.append(rawdata.loc[i]['date'])
