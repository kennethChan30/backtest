#pylint:disable=E0001
x = {'high': [1095.4, 1109.82, 1141.68, 1174.51, 1191.67, 1197.31, 1209.02, 1214.96, 1223.05, 1238.61, 1244.02, 1257.68, 1266.75, 1288.22, 1293.83, 1303.58, 1313.89, 1324.41, 1331.99, 1339.04, 1352.96, 1376.3, 1392.34, 1416.46, 1439.05, 1478.85, 1533.57, 1586.75, 1601.05, 1618.5, 1647.08, 1665.94, 1694.94, 1714.86, 1732.85, 1752.19, 1779.34, 1839.6, 1844.38, 1870.28, 1876.66, 1885.84, 1894.53, 1902.7, 1911.63, 1920.61], 'bodyhigh': [1078.85, 1094.25, 1120.43, 1140.73, 1164.53, 1171.95, 1177.8, 1188.66, 1198.03, 1202.81, 1209.58, 1217.72, 1229.39, 1234.41, 1242.1, 1246.52, 1255.03, 1265.43, 1272.38, 1287.11, 1292.75, 1296.98, 1311.8, 1317.97, 1321.9, 1327.19, 1337.1, 1351.03, 1374.58, 1393.79, 1416.44, 1435.32, 1476.8, 1531.2, 1579.67, 1593.81, 1604.93, 1614.11, 1623.81, 1652.15, 1664.54, 1703.05, 1715.3, 1729.2, 1750.09, 1774.0, 1813.55, 1821.64, 1861.88, 1868.77, 1883.14, 1907.64, 1912.4], 'bodylow': [1068.91, 1085.65, 1094.96, 1116.89, 1153.93, 1164.98, 1171.83, 1182.43, 1186.96, 1194.3, 1206.15, 1216.94, 1228.13, 1243.46, 1256.9, 1276.14, 1282.45, 1285.67, 1291.13, 1307.33, 1312.82, 1322.91, 1332.01, 1366.31, 1393.81, 1423.54, 1489.45, 1536.07, 1568.54, 1585.85, 1596.67, 1612.98, 1636.38, 1643.35, 1655.19, 1661.07, 1670.24, 1690.05, 1708.48, 1725.99, 1769.95, 1785.25, 1786.48, 1812.06, 1815.05, 1822.5, 1829.31, 1842.07, 1851.5, 1862.85], 'low': [1066.37, 1082.74, 1093.75, 1111.3, 1151.74, 1163.61, 1175.19, 1185.59, 1192.52, 1201.38, 1208.85, 1221.7, 1227.34, 1240.99, 1251.29, 1277.66, 1287.68, 1305.61, 1310.24, 1318.76, 1322.83, 1337.56, 1357.74, 1364.72, 1391.78, 1413.37, 1495.63, 1540.68, 1567.7, 1583.23, 1603.32, 1608.82, 1634.54, 1652.76, 1662.81, 1685.96, 1704.73, 1720.5, 1732.53, 1770.41, 1794.28, 1826.22, 1838.55, 1858.04, 1858.38]}
havepair = True
resistance_range = []
ol = 0
while len(x['high'])>0 and len(x['bodyhigh'])>0 and havepair:
	check = len(x['high'])
	print('a')
	for il in range(len(x['bodyhigh'])):
		if x['bodyhigh'][il] > x['high'][ol]:
			ol = ol + 1
			print(ol)
			if ol == len(x['high']):
				havepair = False
			break
		if x['high'][ol] - x['bodyhigh'][il] < 4:
			resistance_range.append([x['high'].pop(ol), x['bodyhigh'].pop(il)])
			break
		if il == len(x['bodyhigh']) - 1:
			havepair = False
while len(x['high'])>0:
	var1 = x['high'].pop()
	resistance_range.append([var1, var1])
while len(x['bodyhigh'])>0:
	var2 = x['bodyhigh'].pop()
	resistance_range.append([var2, var2])
resistance_range.sort()
ol = 0
havepair = True
support_range = []

while len(x['low'])>0 and len(x['bodylow'])>0 and havepair:
	check = len(x['low'])
	print('a')
	for il in range(len(x['bodylow'])):
		if x['bodylow'][il] < x['low'][ol]:
			ol = ol + 1
			print(ol)
			if ol == len(x['low']):
				havepair = False
			break
		if x['bodylow'][ol] - x['low'][il] < 4:
			support_range.append([x['low'].pop(ol), x['bodylow'].pop(il)])
			break
		if il == len(x['bodylow']) - 1:
			havepair = False
while len(x['low'])>0:
	var1 = x['low'].pop()
	support_range.append([var1, var1])
while len(x['bodylow'])>0:
	var2 = x['bodylow'].pop()
	support_range.append([var2, var2])
support_range.sort()

	
print(x)
print(resistance_range, support_range)
		