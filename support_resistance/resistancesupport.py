import pandas as pd
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import numpy as np


def ATR(data):
#indicator ATR
	high_low = data['high'] - data['low']
	high_close = np.abs(data['high'] - data['close'].shift())
	low_close = np.abs(data['low'] - data['close'].shift())

	ranges = pd.concat([high_low, high_close, low_close], axis=1)
	true_range = np.max(ranges, axis=1)
	atr = true_range.rolling(14).sum()/14
	return atr

 
def collecdata(start, end):
#collect neccesary data up to time
	data = rawdata4hr[(rawdata4hr['date']<datetime.fromisoformat(end)) & (rawdata4hr['date']>datetime.fromisoformat(start))].reset_index().drop('index', axis =1)
	global ave, collection
#the average of fluacation of the price
	ave = np.mean(data['high']-data['low'])
	collection = {'bodyhigh': [], 'high': [], 'low': [], 'bodylow': []}

	for i in range(0, len(data)):
		collection['bodyhigh'].append(max(data['open'][i],data['close'][i]))
		collection['high'].append(data['high'][i])
		collection['low'].append(data['low'][i])
		collection['bodylow'].append(min(data['open'][i],data['close'][i]))


def key_levels(bodypart):
	levels = {}
	levelsstate = {}
	keylevels = {}
	if bodypart == 'bodyhigh' or bodypart == 'high':
		for m in range(3, len(collection[bodypart])-2):
			if collection[bodypart][m] == max(collection[bodypart][m-2:m+3]):
				if np.sum([abs(collection[bodypart][m] - level) < ave for level in levels]) == 0:
					levels[collection[bodypart][m]] = [collection[bodypart][m]]
				else:
					for level in levels:
						if abs(collection[bodypart][m] - level) < ave:
							levels[level].append(collection[bodypart][m])
	if bodypart == 'bodylow' or bodypart == 'low':
		for m in range(3, len(collection[bodypart])-2):
			if collection[bodypart][m] == min(collection[bodypart][m-2:m+3]):
				if np.sum([abs(collection[bodypart][m] - level) < ave for level in levels]) == 0:
					levels[collection[bodypart][m]] = [collection[bodypart][m]]
				else:
					for level in levels:
						if abs(collection[bodypart][m] - level) < ave:
							levels[level].append(collection[bodypart][m])
	for level, price in levels.items():
		levelsstate[level] = {'No.': len(price), 'mean': np.median(price).round(decimals=2)}
		if len(price)>10:
			keylevels[np.median(price).round(decimals=2)] = len(price)
	keylevels[maxhigh] = 1
	return keylevels

def findSandR(p):
	bodypart = ['bodyhigh', 'high', 'low', 'bodylow']
	nearlevels_count = {}
	for part in bodypart:
		xkeylevel = key_levels(part)
		xprice = sorted(xkeylevel.keys())

		for i in range(0,len(xprice)-1):
			if xprice[i] < p and xprice[i+1] >  p:
				for x in range(i-2, i+4):
					try:
						nearlevels_count[xprice[x]] = xkeylevel[xprice[x]]
					except:
						break
				break
	nearlevels = sorted(nearlevels_count.keys())
	different = 3
	sig_levels = []
	sig_ranges = []
	for l in range(0, len(nearlevels)):
		h = l
		lower = l
		upper = l
		while h < len(nearlevels) and nearlevels[h] - nearlevels[l] < different:
			upper = h
			h = h+1
		if lower != upper:
			if np.sum([upper ==level[1] for level in sig_levels]) == 0:
				if sig_levels != [] and lower <= sig_levels[-1][1]:
					if nearlevels[upper] - nearlevels[lower] < nearlevels[sig_levels[-1][1]] - nearlevels[sig_levels[-1][0]]:
						sig_levels[-1] = [lower, upper]

				else:
					sig_levels.append([lower, upper])
		else:
			if (sig_levels == [] or lower != sig_levels[-1][1]):
				sig_levels.append([lower, upper])
	for l in sig_levels:
		sig_ranges.append([nearlevels[l[0]], nearlevels[l[1]]])

	return(sig_ranges)

def support_level(p):
	if rawdata30mins['past25'].iloc[0] > p:
		sr = 0
		while signifcant[sr][0] < p:
			sr = sr+1
		support = sr - 1
	else:
		sr = len(signifcant) - 1
		while signifcant[sr][1] > p:
			sr = sr-1
		support = sr 
	return support

def longposition(i, data):
	global pos, trade_position, entry_price, date, profit, stoploss, execute_profit, execute_stoploss, risk, reward, risk_to_reward
	pos = 1
	trade_position = 'Long'
	entry_price = data['open'].loc[i] + spread
	date = data['date'].loc[i]
	profit = signifcant[support+1][1]
	stoploss = round(signifcant[support][0] - data['ATR'].loc[i-1], 2)
	execute_profit = profit
	execute_stoploss = stoploss
	risk = abs(entry_price - execute_stoploss)
	reward = abs(entry_price - execute_profit)
	risk_to_reward = round(reward/risk, 2)

def shortposition(i, data):
	global pos, trade_position, entry_price, date, profit, stoploss, execute_profit, execute_stoploss, risk, reward, risk_to_reward
	pos = 1
	trade_position = 'Short'
	entry_price = data['open'].loc[i]
	date = data['date'].loc[i]
	profit = signifcant[support][0]
	stoploss = round(signifcant[support+1][1] + data['ATR'].loc[i-1], 2)
	execute_profit = profit + spread
	execute_stoploss = stoploss + spread
	risk = abs(entry_price - execute_stoploss)
	reward = abs(entry_price - execute_profit)
	risk_to_reward = round(reward/risk, 2)

def hitptofit(i, data, position):
	global pos, trade_position, tradesheet
	pos = 0
	exit_trigger = 'Hit Profit'
	exit_date = data['date'].loc[i]
	if position=='Long':
		exit_price = profit
		profit_loss = exit_price - entry_price

	if position=='Short':
		exit_price = profit + spread
		profit_loss = entry_price - exit_price
		

	trade = pd.DataFrame([[trade_position, date ,entry_price, risk, execute_stoploss, execute_profit, risk_to_reward, exit_date, exit_price, exit_trigger, profit_loss, signifcant[support][0], signifcant[support][1], signifcant[support+1][0], signifcant[support+1][1]]], columns=columns_names)
	tradesheet = tradesheet.append(trade, ignore_index=True)
	trade_position = ''
	exit_trigger = ''
def hitstoploss(i, data, position):
	global pos, trade_position, tradesheet
	pos = 0
	exit_trigger = 'Stop Loss'
	exit_date = data['date'].loc[i]
	if position=='Long':
		exit_price = stoploss
		profit_loss = exit_price - entry_price

	if position=='Short':
		exit_price = stoploss + spread
		profit_loss = entry_price - exit_price

	trade = pd.DataFrame([[trade_position, date ,entry_price, risk, execute_stoploss, execute_profit, risk_to_reward, exit_date ,exit_price, exit_trigger, profit_loss, signifcant[support][0], signifcant[support][1], signifcant[support+1][0], signifcant[support+1][1]]], columns=columns_names)
	tradesheet = tradesheet.append(trade, ignore_index=True)
	trade_position = ''
	exit_trigger = ''

rawdata4hr = pd.read_csv('Data/4hr.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata4hr['date'] = rawdata4hr['date'] + ' ' + rawdata4hr['time']
rawdata4hr  = rawdata4hr.drop('time',axis =1)
rawdata4hr['date'] = pd.to_datetime(rawdata4hr['date'], format="%Y.%m.%d %H:%M")

rawdata30mins = pd.read_csv('Data/30mins.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata30mins['date'] = rawdata30mins['date'] + ' ' + rawdata30mins['time']
rawdata30mins  = rawdata30mins.drop('time',axis =1)
rawdata30mins['date'] = pd.to_datetime(rawdata30mins['date'], format="%Y.%m.%d %H:%M")
rawdata30mins['reference_date'] = rawdata30mins['date'].dt.date
rawdata30mins['ATR'] = ATR(rawdata30mins)
midpiont = (rawdata30mins['open']+rawdata30mins['close'])/2
rawdata30mins['past25'] = round(midpiont.ewm(span=25, adjust=False).mean(), 2).shift(5)



#reference for opening position
pos = 0
spread = 0.7
maxhigh = 0
 #check for position just open
justopen = 0
breakout_count = 0
awayfromlevel = 2
trade_position = ''
columns_names = ['position', 'date', 'entry price', 'risk', 'stop loss', 'profit target', 'risk to reward', 'exit date', 'exit price', 'exit trigger', 'profit and loss', 'support1', 'support2', 'resistance1', 'resistance2']
tradesheet = pd.DataFrame(columns=columns_names)
start = '2010-12-30 17:00'

end = (rawdata30mins['reference_date'][0]).strftime("%Y-%m-%d")
end_reference = rawdata30mins['reference_date'][0]
collecdata(start, end)
price = rawdata30mins['close'][0]
signifcant = findSandR(price)
support = support_level(price)
trading_range = [signifcant[support][0] - awayfromlevel, signifcant[support][1]+ awayfromlevel/2, signifcant[support+1][0]- awayfromlevel/2,signifcant[support+1][1]+ awayfromlevel]

for i in range(20, len(rawdata30mins)):
	print(i)
	if rawdata30mins['reference_date'][i] != end_reference:
		end = (rawdata30mins['date'].dt.date[i]).strftime("%Y-%m-%d")
		end_reference = rawdata30mins['reference_date'][i]
		collecdata(start, end)

	if rawdata30mins['high'][i] > maxhigh:
		maxhigh = rawdata30mins['high'][i]

	price = rawdata30mins['close'][i-1]
	if rawdata30mins['low'][i-1] > signifcant[support+1][1] or rawdata30mins['high'][i-1] < signifcant[support][0]:
		breakout_count = breakout_count+1
		if breakout_count == 5:
			signifcant = findSandR(price)
			support = support_level(price)
			trading_range = [signifcant[support][0] - awayfromlevel, signifcant[support][1]+ awayfromlevel/2, signifcant[support+1][0]- awayfromlevel/2,signifcant[support+1][1]+ awayfromlevel]
			breakout_count = 0
	
	else:
		breakout_count = 0

	lowIswithinTradingRange = rawdata30mins['low'][i-2] > trading_range[0] and rawdata30mins['low'][i-2] < trading_range[1]
	isRedbodyAtSupport = rawdata30mins['close'][i-2] < rawdata30mins['open'][i-2]
	isGreenbodyAtSupport = rawdata30mins['close'][i-1] > rawdata30mins['open'][i-1]

	HighIswithinTradingRange = rawdata30mins['high'][i-2] < trading_range[3] and rawdata30mins['high'][i-2] > trading_range[2]
	isRedbodyAtResistance = rawdata30mins['close'][i-1] < rawdata30mins['open'][i-1]
	isGreenbodyResistance = rawdata30mins['close'][i-2] > rawdata30mins['open'][i-2]
	if pos == 0:
		if lowIswithinTradingRange and isRedbodyAtSupport and isGreenbodyAtSupport:
			longposition(i, rawdata30mins)
		if HighIswithinTradingRange and isRedbodyAtResistance and isGreenbodyResistance:
			shortposition(i, rawdata30mins)
			
	else:
		if trade_position == 'Long':
			if rawdata30mins['high'][i] > profit:
				hitptofit(i, rawdata30mins, trade_position)
			elif rawdata30mins['low'][i] < stoploss:
				hitstoploss(i, rawdata30mins, trade_position)
		if trade_position == 'Short':
			if rawdata30mins['low'][i] < profit:
				hitptofit(i, rawdata30mins, trade_position)
			elif rawdata30mins['high'][i] > stoploss:
				hitstoploss(i, rawdata30mins, trade_position)

tradesheet.to_excel('tradesheet.xlsx', sheet_name='resistance', index=False)



