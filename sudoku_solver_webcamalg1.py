# THIS PROGRAM APPLIES THE ALGORITHM IN THE CORRESPONDING STATIC PROGRAM
# AND APPLIES THIS TO A MOVING WEBCAM VIDEO

import cv2 
import numpy as np 

cap = cv2.VideoCapture(0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))


while cap.isOpened():

	_, frame = cap.read()

	# converting to grayscale
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# applying gaussian blur to remove sharp edges and changes in pixels
	frame_blur = cv2.GaussianBlur(frame_gray, (11, 11), 0)

	# Now we apply adaptive thresholding
	frame_blur_thresh = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

	# Inverting so that the grid that we need is white
	frame_blur_thresh_inv = cv2.bitwise_not(frame_blur_thresh)

	# Now we dilate
	frame_dil = cv2.dilate(frame_blur_thresh_inv, kernel, iterations = 1)

	# now we make a copy as we need to find the contours in this one
	frame_dil_copy = frame_dil.copy()

	# Finding the contours
	_, contours, _ = cv2.findContours(frame_dil_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# finding the contour with the largest perimeter
	largest_perimeter_val = 0
	largest_perimeter_pos = 0
	for i in xrange(len(contours)):
		p = cv2.arcLength(contours[i], False) # True takes into account only closed curves
		if p > largest_perimeter_val:
			largest_perimeter_val = p
			largest_perimeter_pos = i

	# We now find a bounding rectangle over this
	x,y,w,h = cv2.boundingRect(contours[largest_perimeter_pos])
	# Displaying on the frame itself
	frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (10,200,5), 2)

	# Filling the contour with largest perimeter
	cv2.drawContours(frame, [contours[largest_perimeter_pos]], 0, (100,100,177), -1)


	# displaying
	cv2.imshow('frame', frame)




	if cv2.waitKey(1) & 0xff == 27:
		break

cap.release()
cv2.destroyAllWindows()

