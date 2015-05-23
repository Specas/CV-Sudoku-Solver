# THIS PROGRAM TAKES IN THE DILATED FRAME FROM THE MAIN PROGRAM.
# IT THEN RETURNS THE 4 END POINTS OF THE GRID

# WHEN THIS PROGRAM IS FIRST USED, IT IS TO GET THE ROUGH VALUE OF THE 4 GRID POINTS
# THE SECOND TIME, IT IS USED TO APPLY THE ROTATION CORRECTION, TO GET A PERFECT
# PERSPECTIVE TRANSFORM

import cv2 
import numpy 


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

# Function to do the initial processing of blurring, thresholding and dilating. It 
# returns the dilated value
def init(frame):

	# convert to grayscale
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Gaussian blur
	frame_gray_blur = cv2.GaussianBlur(frame_gray, (11,11), 0)

	# Adaptive thresholding
	frame_thresh = cv2.adaptiveThreshold(frame_gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

	# Inverting to get the grid as white
	frame_thresh_inv = cv2.bitwise_not(frame_thresh)

	# dilating
	frame_dil = cv2.dilate(frame_thresh_inv, kernel, iterations = 1)

	# returning dilated image
	return frame_dil





# Finding the 4 outer grid points and returning it
def contourEndPoints(dil):

	_, contours, _ = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	largest_bounding_rect_val = 0
	largest_bounding_rect_pos = 0

	cont_empty = False
	# cont is the largest contour by bounded rectangle area
	cont = [] 

	for i in xrange(len(contours)):
		# bounding rectangle and its are
		x,y,w,h = cv2.boundingRect(contours[i])
		area = w*h
		# finding contour with maximum bounding area
		if area > largest_bounding_rect_val:
			largest_bounding_rect_val = area
			largest_bounding_rect_pos = i 

	if len(contours):
		cont = contours[largest_bounding_rect_pos]
	else:
		# No contours present
		cont_empty = True


	# returns the list of the 4 grid points
	if not cont_empty:

		# Extreme ends of the contour
		leftmost = tuple(cont[cont[:,:,0].argmin()][0])
		rightmost = tuple(cont[cont[:,:,0].argmax()][0])
		topmost = tuple(cont[cont[:,:,1].argmin()][0])
		botmost = tuple(cont[cont[:,:,1].argmax()][0])

		# Finding the corners of the grid using these
		topleft = (leftmost[0], topmost[1])
		topright = (rightmost[0], topmost[1])
		botleft = (leftmost[0], botmost[1])
		botright = (rightmost[0], botmost[1])

		# returning
		return [topleft, topright, botleft, botright]
	else:

		return 0



