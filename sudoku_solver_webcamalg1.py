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
	largest_bounding_area = 0
	largest_bounding_pos = 0
	for i in xrange(len(contours)):
		p = cv2.arcLength(contours[i], True) # True takes into account only closed curves

		# bounding rect
		x,y,w,h = cv2.boundingRect(contours[i])
		a = w*h
		# Finding contour with maximum bounding rectangle area
		if a > largest_bounding_area:
			largest_bounding_area = a
			largest_bounding_pos = i


	

	# contour with largest perimeter
	cont = contours[largest_bounding_pos]



	# Filling the contour with largest perimeter
	cv2.drawContours(frame, [contours[largest_bounding_pos]], 0, (100,100,177), -1)

	# Finding the extreme ends of the contour
	leftmost = tuple(cont[cont[:,:,0].argmin()][0])
	rightmost = tuple(cont[cont[:,:,0].argmax()][0])
	topmost = tuple(cont[cont[:,:,1].argmin()][0])
	botmost = tuple(cont[cont[:,:,1].argmax()][0])

	# Finding the corners of the grid using these
	topleft = (leftmost[0], topmost[1])
	topright = (rightmost[0], topmost[1])
	botleft = (leftmost[0], botmost[1])
	botright = (rightmost[0], botmost[1])

	# Drawing the extremem points as circles
	frame = cv2.circle(frame, leftmost, 5, (0,200,100), -1)
	frame = cv2.circle(frame, rightmost, 5, (0,200,100), -1)
	frame = cv2.circle(frame, topmost, 5, (0,200,100), -1)
	frame = cv2.circle(frame, botmost, 5, (0,200,100), -1)
	frame = cv2.circle(frame, topleft, 5, (0,0, 255), -1)
	frame = cv2.circle(frame, topright, 5, (0,0, 255), -1)
	frame = cv2.circle(frame, botleft, 5, (0,0, 255), -1)
	frame = cv2.circle(frame, botright, 5, (0,0, 255), -1)



	


	# displaying
	cv2.imshow('frame', frame)




	if cv2.waitKey(1) & 0xff == 27:
		break

cap.release()
cv2.destroyAllWindows()

