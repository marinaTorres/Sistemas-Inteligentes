from datetime import datetime
from statistics import median
from statistics import variance
from statistics import mean
import numpy as np

# Calculates linnear regression given 2 set of data
def linnear_regression(x_values, y_values):
	m = (((mean(x_values)*mean(y_values)) - mean(x_values*y_values)) /
         ((mean(x_values)*mean(x_values)) - mean(x_values*x_values)))
	b = mean(y_values) - m*mean(x_values)
	return (m, b)

# CONSTANTS
FILE = open("SECURITY_5_CLEAN.txt", "r") 
FILE_2_WRITE = open("SECURITY_5_ANALYSIS.csv", "w+")
DELTA_SECONDS = 15
EPSILON = 0.0005

# Global variables
minute_to_analyse = 30
for_second = 0
trick_list = []
started = False


for count, line in enumerate(FILE):
	if count == 0:
		FILE_2_WRITE.write('minute:second, X1, X2, X3(m), X4(b), Y, ticks\r')
		continue
	if count%10000 == 0:
		print(count/10000)
	actual_values = line.split('|')
	trick_value = actual_values[3]
	strDate = actual_values[2]
	date = datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S.000')
	
	# Time variables
	hour = date.hour
	minute = date.minute
	second = date.second

	# Time Control
	if date.hour >= 10:
		continue
	if not started and (minute >= 30 and hour >= 9):
		started = True
	else:
		if not started:
			continue

	if minute == minute_to_analyse and second < (for_second + DELTA_SECONDS):
		trick_list.append(float(trick_value))
	else:
		# Time Control
		if len(trick_list) < 2:
			for_second += DELTA_SECONDS
			if for_second >= 60:
				for_second = 0
				minute_to_analyse = minute
			trick_list = []
			continue

		# Analysis
		x1 = median(trick_list)
		x2 = variance(trick_list)
		x_values = np.array(list(range(1, len(trick_list)+1)), dtype=np.float64)
		y_values = np.array(trick_list, dtype=np.float64)
		m, b = linnear_regression(x_values, y_values)
		y = 0
		if m > EPSILON:
			y = 1
		elif m < (-1*EPSILON):
			y = -1
		line2write = '{}:{}, {}, {}, {}, {}, {},{}\r'.format(minute_to_analyse, for_second, x1, x2, m, b, y,len(trick_list))
		FILE_2_WRITE.write(line2write)
		
		# Time Control
		trick_list = []
		trick_list.append(float(trick_value))
		for_second += DELTA_SECONDS
		if for_second >= 60:
			for_second = 0
			minute_to_analyse = minute
