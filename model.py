import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify
import os
import csv

names = ['Time Stamp', 'Age', 'Height',	'Weight',	'B.M.I.', 'Heart Rate',	'Alcohol',	'Body Temperature',	'Eye Aspect Ratio',	'Class']

df = pd.read_csv('data.csv')
print(df.shape)
print(df.head())