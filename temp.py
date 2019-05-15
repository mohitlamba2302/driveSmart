import cv2
import numpy as np

left_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
right_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')

if left_ear_cascade.empty():
  raise IOError('Unable to load the left ear cascade classifier xml file')

if right_ear_cascade.empty():
  raise IOError('Unable to load the right ear cascade classifier xml file')

cap = cv2.VideoCapture(0)


#eyes inside a face
while True:
 ret, img = cap.read()
		
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
left_ear = left_ear_cascade.detectMultiScale(gray, 1.3, 5)
right_ear = right_ear_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in left_ear:
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)

for (x,y,w,h) in right_ear:
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 3)

cv2.imshow('Ear Detector', img)
k = cv2.waitKey(30) & 0xff
if k == 27:
	break
cv2.waitKey()
cv2.destroyAllWindows()