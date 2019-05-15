import serial
import os
import pickle

arduino=serial.Serial('/dev/cu.usbmodem14101',timeout=1, baudrate=115200)
while(True):
	temp = arduino.readline()
	temp =str(temp)
	
	if len(temp) > 7:
		temp1 = temp.split(':')
		temp2 = temp1[1].split('\\')
		ans = temp2[0].lstrip()
		ans = temp2[0].rstrip()
		print(ans)
		dict1 = {
			'value':ans
		}
		with open('pulse.pkl', 'wb') as f:
			pickle.dump(dict1, f)

# arduino=serial.Serial()
# print(arduino)
# print(arduino.name)
