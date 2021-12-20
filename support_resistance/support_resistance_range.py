import pandas as pd
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import numpy as np


def keyLevels(start, end, rawdata):
#collect neccesary data up to time
	data = rawdata[(rawdata['date']<datetime.fromisoformat(end)) & (rawdata['date']>datetime.fromisoformat(start))].reset_index().drop('index', axis =1)
#the average of fluacation of the price
	ave = np.mean(data['high']-data['low'])
	collection = {'bodyhigh': [], 'high': [], 'low': [], 'bodylow': []}

	for i in range(0, len(data)):
		collection['bodyhigh'].append(max(data['open'][i],data['close'][i]))
		collection['high'].append(data['high'][i])
		collection['low'].append(data['low'][i])
		collection['bodylow'].append(min(data['open'][i],data['close'][i]))

	levels = {'high': [], 'bodyhigh': [], 'bodylow': [], 'low': []}
	levelsstate = {'high': [], 'bodyhigh': [], 'bodylow': [], 'low': []}
	nl = 5
	sp = ave + 2
	for bodypart in ['bodyhigh', 'high', 'low', 'bodylow']:
		if bodypart == 'bodyhigh' or bodypart == 'high':
			for m in range(3, len(collection[bodypart])-2):
				if collection[bodypart][m] == max(collection[bodypart][m-2:m+3]):
					levels[bodypart].append(collection[bodypart][m])		
		if bodypart == 'bodylow' or bodypart == 'low':
			for m in range(3, len(collection[bodypart])-2):
				if collection[bodypart][m] == min(collection[bodypart][m-2:m+3]):
					levels[bodypart].append(collection[bodypart][m])
		levels[bodypart] = sorted(levels[bodypart])	

	for level, price in levels.items():
		intertable = pd.DataFrame(price, columns = [level])
		intertable['mean'] = round(intertable[level].rolling(nl, center=True).mean(), 2)
		intertable['sd'] = intertable[level].rolling(nl, center=True).std()
		intertable['sdmin'] = intertable['sd'].rolling(25, center=True).min()
		levelsstate[level] = (intertable[(intertable['sd'] == intertable['sdmin']) | (intertable['sd']>sp)][level].values.tolist())
		for last in range(nl//2, 0, -1):
			levelsstate[level].append(intertable[level].iloc[-last])
	return levelsstate

def range_calculate(x, type):
	if type == 'resistance':
		resistance_range = []
		havepair = True
		upperlv = 0
		while len(x['high'])>0 and len(x['bodyhigh'])>0 and havepair:
			check = len(x['high'])
			for lowerlv in range(len(x['bodyhigh'])):
				if x['bodyhigh'][lowerlv] > x['high'][upperlv]:
					upperlv = upperlv + 1
					if upperlv == len(x['high']):
						havepair = False
					break
				if x['high'][upperlv] - x['bodyhigh'][lowerlv] < 4:
					resistance_range.append([x['high'].pop(upperlv), x['bodyhigh'].pop(lowerlv)])
					break
				if lowerlv == len(x['bodyhigh']) - 1:
					havepair = False
		while len(x['high'])>0:
			var1 = x['high'].pop()
			resistance_range.append([var1, var1])
		while len(x['bodyhigh'])>0:
			var2 = x['bodyhigh'].pop()
			resistance_range.append([var2, var2])
		resistance_range.sort()
		return resistance_range

	if type == 'support':
		upperlv = 0
		havepair = True
		support_range = []

		while len(x['low'])>0 and len(x['bodylow'])>0 and havepair:
			check = len(x['bodylow'])
			for lowerlv in range(len(x['low'])):
				if x['bodylow'][upperlv] < x['low'][lowerlv]:
					upperlv = upperlv + 1
					if upperlv == len(x['bodylow']):
						havepair = False
					break
				if x['bodylow'][upperlv] - x['low'][lowerlv] < 4:
					support_range.append([x['low'].pop(lowerlv), x['bodylow'].pop(upperlv)])
					break
				if lowerlv == len(x['low']) - 1:
					havepair = False
		while len(x['low'])>0:
			var1 = x['low'].pop()
			support_range.append([var1, var1])
		while len(x['bodylow'])>0:
			var2 = x['bodylow'].pop()
			support_range.append([var2, var2])
		support_range.sort()
		return support_range

def support_level(p, levels):
	i = 0
	no = len(levels)
	while True:
		if levels[i][0] <= p:
			i = i + 1
		if i == no or levels[i][0] > p:
			break
	return i - 1

def resistance_level(p, levels):
	i = 0
	while True:
		if levels[i][0] < p:
			i = i + 1
		if levels[i][0] >= p:
			break
	return i
		