import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify
import os
import csv
from flask import Flask
import time
import pickle
from flask import jsonify
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from flask import request
import requests
import json
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, render_template

app = Flask(__name__)

names = ['Age', 'Height',	'Weight', 'B.M.I.', 'Heart Rate', 'Alcohol', 'Body Temperature', 'Eye Aspect Ratio', 'Class']


df = pd.read_csv('data.csv')
print(df.shape)
print(df.head())

X = df.drop('Class', axis=1)
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

rfc = RandomForestClassifier()
# rfc.fit(X_train,y_train)
rfc.fit(X, y)
# predictions
def checks(pulse, COUNTER):
	if pulse>150:
		return 0
	if COUNTER>100:
		return 0
	return 1

rfc_predict = rfc.predict(X_test)
print(rfc_predict)
# rfc_cv_score = cross_val_score(rfc, X, y, cv=10, scoring='roc_auc')

# print("=== Confusion Matrix ===")
# print(confusion_matrix(y_test, rfc_predict))
# print('\n')
# print("=== Classification Report ===")
# print(classification_report(y_test, rfc_predict))
# print('\n')
# print("=== All AUC Scores ===")
# print(rfc_cv_score)
# print('\n')
# print("=== Mean AUC Score ===")
# print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())

# Age = 20 
# Height = 1.70
# Weight = 70
# BMI = 21
# HeartRate = 55
# Alcohol = 0
# BodyTemperature = 98
# EyeAspectRatio = 0


# row = [Age, Height, Weight, BMI, HeartRate, Alcohol, BodyTemperature, EyeAspectRatio]
# names = ['Age', 'Height', 'Weight', 'BMI', 'Heart Rate', 'Alcohol', 'Body Temperature', 'Eye Aspect Ratio']
# # df = pd.DataFrame(row, columns = names) 
# # print(df)
# testing = [[Age, Height, Weight, BMI, HeartRate, Alcohol, BodyTemperature, EyeAspectRatio]]
# rfc_predict = rfc.predict(testing)
# print(rfc_predict)

def test_data():
	while(True):
		time.sleep(1) 
		with open('pulse.pkl', 'rb') as f:
			var1 = pickle.load(f)
			pulse = var1['value']
		with open('vision.pkl', 'rb') as f:
			var2 = pickle.load(f)
			COUNTER = var2['value']

		
		pulse = int(pulse)
		ear = 0
		if COUNTER>100:
			ear = 1

		payload = {
			"Age":20,
			"Height":180,
			"Weight":65,
			"BMI":21,
			"Heart Rate":pulse,
			"Alcohol":0,
			"Body Temperature":99,
			"Eye Aspect Ratio":ear
		}

		# row = [Age, Height, Weight, BMI, HeartRate, Alcohol, BodyTemperature, EyeAspectRatio]
		testing = [[20,180,65,21,pulse,0,99,ear]]
		rfc_predict = rfc.predict(testing)
		
		list(rfc_predict)
		rfc_prediction = checks(pulse, COUNTER)
		if rfc_predict[0]==1 or rfc_prediction==1:
			print('Safe')
		else:
			return render_template('alert.html')
		

# test_data()

'''
@app.route('/add_data', methods = ['POST'])
def add_data():
	if request.method == 'POST':			
		data = json.loads(request.data)
		Age = data['Age'] 
		Height = data['Height']
		Weight = data['Weight']
		BMI = data['BMI']
		HeartRate = data['Heart Rate']
		Alcohol = data['Alcohol']
		BodyTemperature = data['Body Temperature']
		EyeAspectRatio = data['Eye Aspect Ratio']

		# Age = 20 
		# Height = 1.70
		# Weight = 70
		# BMI = 21
		# HeartRate = 55
		# Alcohol = 0
		# BodyTemperature = 98
		# EyeAspectRatio = 32


		row = [Age, Height, Weight, BMI, HeartRate, Alcohol, BodyTemperature, EyeAspectRatio]
		rfc_predict = rfc.predict([row])
		ans = {
			'value':rfc_predict
		}
		return jsonify(ans)
	else:
		return jsonify({'name':'mohit'})




'''


@app.route('/test_data')
def test_data():
	while(True):
		time.sleep(1) 
		with open('pulse.pkl', 'rb') as f:
			var1 = pickle.load(f)
			pulse = int(var1['value'])
		with open('vision.pkl', 'rb') as f:
			var2 = pickle.load(f)
			COUNTER = int(var2['value'])


		ear = 0
		if COUNTER>100:
			ear = 1

		payload = {
			"Age":20,
			"Height":180,
			"Weight":65,
			"BMI":21,
			"Heart Rate":pulse,
			"Alcohol":0,
			"Body Temperature":99,
			"Eye Aspect Ratio":ear
		}

		# row = [Age, Height, Weight, BMI, HeartRate, Alcohol, BodyTemperature, EyeAspectRatio]
		testing = [[20,180,65,21,pulse,0,99,ear]]
		rfc_predict = rfc.predict(testing)
		
		list(rfc_predict)
		rfc_prediction = checks(pulse, COUNTER)
		if rfc_predict[0]==1 and rfc_prediction==1:
			print('Safe: ', pulse, ', ', COUNTER, ', ', rfc_prediction)
			continue
		else:
			print('unsafe: ', pulse, ', ', COUNTER)
			break

	return render_template('alert.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='4999')

