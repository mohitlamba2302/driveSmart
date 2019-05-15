
from scipy.spatial import distance
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import dlib
import json
import sys
import cv2
import time
import pickle
# import memcache
import simpleaudio as sa

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

EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 100
 
# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
COUNTER = 0
ALARM_ON = False
TOTAL = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
																								 
vs = VideoStream(src = 0).start()
currentCount = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
	dict1 = {
		'value':COUNTER
	}
	with open('vision.pkl', 'wb') as f:
		pickle.dump(dict1, f)
	
	
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
		cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull],  -1, (255, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1
 
			# if the eyes were closed for a sufficient number of
			# then sound the alarm
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				# if the alarm is not on, turn it on
				if not ALARM_ON:
					ALARM_ON = True
 
					# check to see if an alarm file was supplied,
					# and if so, start a thread to have the alarm
					# sound played in the background
					# if args["alarm"] != "":
					#   t = Thread(target=sound_alarm,
					#     args=(args["alarm"],))
					#   t.deamon = True
					#   t.start()

					# if ALARM_ON:


					# 	wave_obj = sa.WaveObject.from_wave_file("audio.wav")
					# 	play_obj = wave_obj.play()

						# play_obj.wait_done()


 
				# draw an alarm on the frame
				cv2.putText(frame, "DROWSINESS ALERT!!!!!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			COUNTER = 0
			ALARM_ON = False

			cv2.putText(frame, "AR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 0), 2)




	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()