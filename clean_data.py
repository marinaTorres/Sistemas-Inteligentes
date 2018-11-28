from datetime import datetime


file = open("SECURITY_4.txt", "r") 
file2write = open("SECURITY_4_CLEAN.txt", "w+")

for count, line in enumerate(file):
	if count == 0:
		file2write.write(line)
		continue
	strDate = line.split('|')[2]
	date = datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S.000')
	if date.weekday() == 0:
		file2write.write(line)
	if count%10000 == 0:
		print(count/10000)