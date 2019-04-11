import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify
import os
import csv
from flask import Flask
from flask import jsonify
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from flask import request
import requests

app = Flask(__name__)

names = ['Time Stamp', 'Age', 'Height',	'Weight', 'B.M.I.', 'Heart Rate', 'Alcohol', 'Body Temperature', 'Eye Aspect Ratio', 'Class']

@app.route('/add_data', methods = ['POST'])
def add_data():
	if request.method == 'POST':			
		data = json.loads(request.data)
		if 'input_string' not in data:
			return 'data is required'

		INPUT_WORD = data['input_string']




df = pd.read_csv('data.csv')
print(df.shape)
print(df.head())

X = df.drop('Class', axis=1)
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

rfc = RandomForestClassifier()
rfc.fit(X_train,y_train)

# predictions
rfc_predict = rfc.predict(X_test)

rfc_cv_score = cross_val_score(rfc, X, y, cv=10, scoring='roc_auc')

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, rfc_predict))
print('\n')
print("=== Classification Report ===")
print(classification_report(y_test, rfc_predict))
print('\n')
print("=== All AUC Scores ===")
print(rfc_cv_score)
print('\n')
print("=== Mean AUC Score ===")
print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())
