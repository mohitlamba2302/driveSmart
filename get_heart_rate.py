'''
	send a requent to thinkspeak server
	while(True):
		fetch the data in a python variable
		save the data required in a pkl file
	end()
'''
import time 
import pickle
from random import randint
while(True):
	time.sleep(1)
	value = randint(70, 122)
	print(value)
	dict1 = {
		'pulse':value
	}
	with open('pulse.pkl', 'wb') as f:
		pickle.dump(dict1, f)