import os
import pickle

def func1(COUNTER):
	while(True):
		COUNTER += 1
		dict1 = {
			'value' : COUNTER
		}
		with open('temp.pkl', 'wb') as f:
			pickle.dump(dict1, f)

COUNTER = 1
func1(COUNTER)