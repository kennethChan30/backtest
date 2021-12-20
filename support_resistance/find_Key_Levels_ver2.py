import pandas as pd
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import numpy as np
from support_resistance_range import keyLevels
 
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


def key_levels():
	levels = {'high': [], 'bodyhigh': [], 'bodylow': [], 'low': []}
	levelsstate = {'high': [], 'bodyhigh': [], 'bodylow': [], 'low': []}
	keylevels = {}
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

		intertable[(intertable['sd'] == intertable['sdmin']) | (intertable['sd']>sp)].to_excel(level+'.xlsx', sheet_name='resistance', index=False)
		levelsstate[level] = (intertable[(intertable['sd'] == intertable['sdmin']) | (intertable['sd']>sp)][level].values.tolist())
		for last in range(nl//2, 0, -1):
			levelsstate[level].append(intertable[level].iloc[-last])
	return levelsstate






rawdata4hr = pd.read_csv('Data/4hr.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata4hr['date'] = rawdata4hr['date'] + ' ' + rawdata4hr['time']
rawdata4hr  = rawdata4hr.drop('time',axis =1)
rawdata4hr['date'] = pd.to_datetime(rawdata4hr['date'], format="%Y.%m.%d %H:%M")

rawdata30mins = pd.read_csv('Data/30mins.csv', names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
rawdata30mins['date'] = rawdata30mins['date'] + ' ' + rawdata30mins['time']
rawdata30mins  = rawdata30mins.drop('time',axis =1)
rawdata30mins['date'] = pd.to_datetime(rawdata30mins['date'], format="%Y.%m.%d %H:%M")
rawdata30mins['reference_date'] = rawdata30mins['date'].dt.date
midpiont = (rawdata30mins['open']+rawdata30mins['close'])/2
rawdata30mins['past25'] = round(midpiont.ewm(span=25, adjust=False).mean(), 2).shift(5)



#reference for opening position

maxhigh = 0
 #check for position just open
# breakout_count = 0

columns_names = [ 'date', 'price' , 'support1', 'support2', 'resistance1', 'resistance2']
# tradesheet = pd.DataFrame(columns=columns_names)
start = '2010-12-30 17:00'

end = (rawdata30mins['reference_date'][0]).strftime("%Y-%m-%d")
end_reference = rawdata30mins['reference_date'][0]
collecdata(start, end)
price = rawdata30mins['close'][0]


nearlevels_count = {}

print(key_levels())
print(keyLevels(start, end,rawdata4hr))

# signifcant = findSandR(price)
# support = support_level(price)


# for i in range(20, len(rawdata30mins)):
# 	print(i)
# 	if rawdata30mins['reference_date'][i] != end_reference:
# 		end = (rawdata30mins['date'].dt.date[i]).strftime("%Y-%m-%d")
# 		end_reference = rawdata30mins['reference_date'][i]
# 		collecdata(start, end)

# 	if rawdata30mins['high'][i] > maxhigh:
# 		maxhigh = rawdata30mins['high'][i]

# 	price = rawdata30mins['close'][i-1]
# 	date = rawdata30mins['date'][i-1]
# 	if rawdata30mins['low'][i-1] > signifcant[support+1][1] or rawdata30mins['high'][i-1] < signifcant[support][0]:
# 		breakout_count = breakout_count+1
# 		if breakout_count == 5:
# 			signifcant = findSandR(price)
# 			support = support_level(price)
# 			trading_range = [signifcant[support][0] - awayfromlevel, signifcant[support][1]+ awayfromlevel/2, signifcant[support+1][0]- awayfromlevel/2,signifcant[support+1][1]+ awayfromlevel]
# 			breakout_count = 0
	
# 	else:
# 		breakout_count = 0

# 	trade = pd.DataFrame([[date ,price, signifcant[support][0], signifcant[support][1], signifcant[support+1][0], signifcant[support+1][1]]], columns=columns_names)
# 	tradesheet = tradesheet.append(trade, ignore_index=True)
# tradesheet.to_excel('tradesheet.xlsx', sheet_name='resistance', index=False)