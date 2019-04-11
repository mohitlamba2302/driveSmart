
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