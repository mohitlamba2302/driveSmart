
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# right_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')
# left_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')

cap = cv2.VideoCapture(0)


##############    eyes inside a face
while True:
	ret, img = cap.read()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color, (ex, ey), (ex+ew,ey+eh), (0,255,0), 2)

	cv2.imshow('img', img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

################# ear only
# while True:
# 	ret, img = cap.read()
# 	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 	r_ear = right_ear_cascade.detectMultiScale(gray, 1.3, 5)
# 	# l_ear = left_ear_cascade.detectMultiScale(gray, 1.3, 5)

# 	for (x,y,w,h) in r_ear:
# 		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
# 		roi_gray = gray[y:y+h, x:x+w]
# 		roi_color = img[y:y+h, x:x+w]

# 	# for (x,y,w,h) in l_ear:
# 	# 	cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
# 	# 	roi_gray = gray[y:y+h, x:x+w]
# 	# 	roi_color = img[y:y+h, x:x+w]		

# 	cv2.imshow('img', img)
# 	k = cv2.waitKey(30) & 0xff
# 	if k == 27:
# 		break



cap.release()
cv2.destroyAllWindows()

'''


from scipy.spatial import distance
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import dlib
import sys
import cv2
import time

def eye_aspect_ratio(eye):
  A = distance.euclidean(eye[1], eye[5])
  B = distance.euclidean(eye[2], eye[4])  
  C = distance.euclidean(eye[0], eye[3])
  ear = (A+B) / (2.0 * C)
  return ear

# Get CMD Command

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", help = "path to facial landmark predictor")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.3
COUNTER = 0
TOTAL = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
                                                 
vs = VideoStream(src = 0).start()
currentCount = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
  frame = vs.read()
  frame = imutils.resize(frame, width=450)
  height, width, c = frame.shape

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  face = face_cascade.detectMultiScale(gray, 1.15)

  min_dis = 100000
  x=0
  y=0
  w=0
  h=0
  for (mx, my, mw, mh) in face:
    d = distance.euclidean((mx+w/2, my+h/2), (width/2, height/2))
    if(d < min_dis):
      min_dis = d
      x = mx
      y = my
      w = mw
      h = mh

  rects = detector(gray, 0)
  prevcount = 0
  for rect in rects:
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    danger = 0
    ear = (leftEAR + rightEAR) / 2.0
    leftEyeHull = cv2.convexHull(leftEye)
    rightEyeHull = cv2.convexHull(rightEye)
    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [rightEyeHull],  -1, (0, 255, 0), 1)




  cv2.imshow("Frame", frame)
  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    break

cv2.destroyAllWindows()
vs.stop()

'''