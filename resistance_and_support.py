import pandas as pd
timeframe = 'daily'
statslist = ['Periods', 'Gross winning trade', 'Gross lossing trade', 'No of winning trade', 'No of lossing trade', 'Percent of winning', 'Max profit', 'Max loss', 'Averge risk to reward','Profit Per Trade', 'Max win streak', ' Max loss streak']
backtesttype = 'resistance_and_support/'
backtestpath = 'drive/MyDrive/Trading/backtest/'
systemdata = backtestpath + 'Data/'
systemoutput = backtestpath +  backtesttype
rawdata = pd.read_csv(systemdata + timeframe + '.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
price_high = [0,0,0,0,0,0,0,0,0,0]
date_high = [0,0,0,0,0,0,0,0,0,0]
pivot = []
pivot_date = []
count = 0
for i in rawdata.index:
  currentMax = max(price_high, default=0)
  price_high = price_high[1:10]
  date_high = price_high[1:10]
  price_high.append(rawdata.loc[i]['high'])
  date_high.append(rawdata.loc[i]['date'])
  if currentMax == max(price_high, default=0):
    count +=1
  else:
    count = 0
  if count == 5:
    x = price_high.index(currentMax)
    pivot.append(price_high[x])
    pivot_date.append(date_high[x])
