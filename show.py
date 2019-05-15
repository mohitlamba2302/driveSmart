import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify
import os
import pickle
from flask import Flask, render_template
import datetime

import csv
from flask import Flask
from flask import jsonify
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from flask import request
import requests
import json
import time 
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/test_data', methods=['POST'])
def test_data():
	data = request.data
	dataDict = json.loads(data)
	print(dataDict)
	# return jsonify({"success":1})
	# while(True):
	# 	time.sleep(1) 
	# 	with open('pulse.pkl', 'rb') as f:
	# 		var1 = pickle.load(f)
	# 		pulse = var1['value']
	# 	with open('vision.pkl', 'rb') as f:
	# 		var2 = pickle.load(f)
	# 		COUNTER = var2['value']


	# 	ear = 0
	# 	if COUNTER>100:
	# 		ear = 1




		# payload = {
		# 	"Age":20,
		# 	"Height":180,
		# 	"Weight":65,
		# 	"BMI":21,
		# 	"Heart Rate":pulse,
		# 	"Alcohol":0,
		# 	"Body Temperature":99,
		# 	"Eye Aspect Ratio":ear
		# }

		# url = 'http://0.0.0.0:4999' + '/add_data'
		# headers = {'content-type': 'application/json'}
		# response = requests.post(url, data=json.dumps(payload), headers=headers)
		# results = json.loads(response.text)

		# print(results)


@app.route("/vivi")
def show_data():

	with open("vision.json", "r") as read_file:
		data = json.load(read_file)

	print(data)

	return jsonify(data)

@app.route("/hell")
def hello():

    # now = datetime.datetime.now()
    # timeString = now.strftime("%Y-%m-%d %H:%M")
    # templateData = {
    #    'title' : 'HELLO!',
    #    'time': timeString
    # }
    # return jsonify(templateData)
    # return render_template('index.html', **templateData)
    print('hello')
    return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='4998')




# def test_data():
# 	while(True):
# 		time.sleep(1) 
# 		with open('pulse.pkl', 'rb') as f:
# 			var1 = pickle.load(f)
# 			pulse = var1['value']
# 		with open('vision.pkl', 'rb') as f:
# 			var2 = pickle.load(f)
# 			COUNTER = var2['value']


# 		ear = 0
# 		if COUNTER>100:
# 			ear = 1

# 		payload = {
# 			"Age":20,
# 			"Height":180,
# 			"Weight":65,
# 			"BMI":21,
# 			"Heart Rate":pulse,
# 			"Alcohol":0,
# 			"Body Temperature":99,
# 			"Eye Aspect Ratio":ear
# 		}

# 		