import pandas as pd
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import numpy as np
from support_resistance_range import range_calculate, support_level, resistance_level, keyLevels

def ATR(data):
#indicator ATR
	high_low = data['high'] - data['low']
	high_close = np.abs(data['high'] - data['close'].shift())
	low_close = np.abs(data['low'] - data['close'].shift())

	ranges = pd.concat([high_low, high_close, low_close], axis=1)
	true_range = np.max(ranges, axis=1)
	atr = true_range.rolling(14).sum()/14
	return atr

def longposition(i, data):
	global pos, trade_position, entry_price, date, profit, stoploss, execute_profit, execute_stoploss, risk, reward, risk_to_reward, entry_keyLevels
	entry_keyLevels = [support_levels[support].copy(), resistance_levels[resistance].copy()]
	gap = entry_keyLevels[1][1] - entry_keyLevels[0][1]
	trade_position = 'Long'
	entry_price = data['open'].loc[i] + spread
	date = data['date'].loc[i]
	profit = resistance_levels[resistance][0]
	stoploss = round(support_levels[support][0] - data['ATR'].loc[i-1], 2)
	execute_profit = profit
	execute_stoploss = stoploss
	risk = entry_price - execute_stoploss
	reward = execute_profit - entry_price
	risk_to_reward = round(reward/risk, 2)
	if gap > 0 and risk_to_reward >= 1 and risk <= 4:
		pos = 1

def shortposition(i, data):
	global pos, trade_position, entry_price, date, profit, stoploss, execute_profit, execute_stoploss, risk, reward, risk_to_reward, entry_keyLevels
	entry_keyLevels = [support_levels[support].copy(), resistance_levels[resistance].copy()]
	gap = entry_keyLevels[1][1] - entry_keyLevels[0][1]
	trade_position = 'Short'
	entry_price = data['open'].loc[i]
	date = data['date'].loc[i]
	profit = support_levels[support][0]
	stoploss = round(resistance_levels[resistance][0] + 1.5*data['ATR'].loc[i-1], 2)
	execute_profit = profit + spread
	execute_stoploss = stoploss + spread
	risk = execute_stoploss - entry_price
	reward = entry_price - execute_profit
	risk_to_reward = round(reward/risk, 2)
	if gap > 0 and risk_to_reward >= 1 and risk <= 4:
		pos = 1

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
		

	trade = pd.DataFrame([[trade_position, date ,entry_price, risk, execute_stoploss, execute_profit, risk_to_reward, exit_date, exit_price, exit_trigger, profit_loss, entry_keyLevels[0][0], entry_keyLevels[0][1], entry_keyLevels[1][1], entry_keyLevels[1][0]]], columns=columns_names)
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

	trade = pd.DataFrame([[trade_position, date ,entry_price, risk, execute_stoploss, execute_profit, risk_to_reward, exit_date ,exit_price, exit_trigger, profit_loss, entry_keyLevels[0][0], entry_keyLevels[0][1], entry_keyLevels[1][1], entry_keyLevels[1][0]]], columns=columns_names)
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

#reference for opening position
pos = 0
spread = 0.7
maxhigh = 0
 #check for position just open
breakout_count = 0
awayfromlevel = 2
trade_position = ''
columns_names = ['position', 'date', 'entry price', 'risk', 'stop loss', 'profit target', 'risk to reward', 'exit date', 'exit price', 'exit trigger', 'profit and loss', 'support1', 'support2', 'resistance1', 'resistance2']
tradesheet = pd.DataFrame(columns=columns_names)
start = '2010-12-30 17:00'
end = (rawdata30mins['reference_date'][0]).strftime("%Y-%m-%d")
end_reference = rawdata30mins['reference_date'][0]

x = keyLevels(start, end,rawdata4hr)
price = rawdata30mins['close'][0]

resistance_levels = range_calculate(x, 'resistance')
support_levels = range_calculate(x, 'support')
support = support_level(price, support_levels)
resistance = resistance_level(price, resistance_levels)
trading_range = [support_levels[support][0] - awayfromlevel, support_levels[support][1]+ awayfromlevel/2, resistance_levels[resistance][1]- awayfromlevel/2, resistance_levels[resistance][0]+ awayfromlevel]
print(trading_range)


for i in range(20, len(rawdata30mins)):
# for i in range(51000, 52500):
	print(i)
	price = rawdata30mins['close'][i-1]
	if rawdata30mins['high'][i] > maxhigh:
		maxhigh = rawdata30mins['high'][i]

	if rawdata30mins['reference_date'][i] != end_reference:
		end = (rawdata30mins['date'].dt.date[i]).strftime("%Y-%m-%d")
		end_reference = rawdata30mins['reference_date'][i]
		x = keyLevels(start, end,rawdata4hr)
		resistance_levels = range_calculate(x, 'resistance')
		support_levels = range_calculate(x, 'support')
		support = support_level(price, support_levels)
		try:
			resistance = resistance_level(price, resistance_levels)
		except IndexError:
			print("Use the highest high as resistance")
			resistance_levels.append([maxhigh,maxhigh])
			resistance = -1

	print(resistance, support, len(resistance_levels), len(support_levels))
	if rawdata30mins['low'][i-1] > resistance_levels[resistance][0] or rawdata30mins['high'][i-1] < support_levels[support][0]:
		breakout_count = breakout_count+1
		if breakout_count == 5:
	
			support = support_level(price, support_levels)

			try:
				resistance = resistance_level(price, resistance_levels)
			except IndexError:
				print("Use the highest high as resistance")
				resistance_levels.append([maxhigh,maxhigh])
				resistance = -1
			trading_range = [support_levels[support][0] - awayfromlevel, support_levels[support][1]+ awayfromlevel/2, resistance_levels[resistance][1]- awayfromlevel/2, resistance_levels[resistance][0]+ awayfromlevel]
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