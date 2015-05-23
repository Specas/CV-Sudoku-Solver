# THIS PROGRAM APPLIES THE ALGORITHM IN THE CORRESPONDING STATIC PROGRAM
# AND APPLIES THIS TO A MOVING WEBCAM VIDEO
# JUST A CRUDE PROGRAM TO TEST

import cv2 
import numpy as np 
import math

cap = cv2.VideoCapture(0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))


while cap.isOpened():

	_, frame = cap.read()

	frame_copy = frame.copy()  # a copy

	frame_rot = frame.copy()


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

	frame_dil_rot = frame_dil.copy() # a copy for rotating

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

	# signify if contours are empty
	contempty = False


	

	# contour with largest perimeter
	if len(contours)!=0:
		cont = contours[largest_bounding_pos]
	else:
		contempty = True





	# Filling the contour with largest perimeter
	if not contempty:
		# Dont compute if no contours found

		# Display the contour if needed
		# cv2.drawContours(frame, [contours[largest_bounding_pos]], 0, (100,100,177), -1)

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
		cv2.circle(frame, leftmost, 5, (0,200,100), -1)
		cv2.circle(frame, rightmost, 5, (0,200,100), -1)
		cv2.circle(frame, topmost, 5, (0,200,100), -1)
		cv2.circle(frame, botmost, 5, (0,200,100), -1)
		# drawing corners
		cv2.circle(frame, topleft, 5, (0,0, 255), -1)
		cv2.circle(frame, topright, 5, (0,0, 255), -1)
		cv2.circle(frame, botleft, 5, (0,0, 255), -1)
		cv2.circle(frame, botright, 5, (0,0, 255), -1)


	# Applying a perspective transform to get only the grid on the frame
	# This is the first rough perspective transform. No angle correction is added

	# Points on the main frame
	grid_points = np.float32([list(topleft), list(topright), list(botleft), list(botright)])
	# Corresponding points on the puzzle frame
	puzzle_points = np.float32([[0,0], [477,0], [0,477], [477,477]])

	P = cv2.getPerspectiveTransform(grid_points, puzzle_points)
	# The puzzle frame
	puzzle_frame = cv2.warpPerspective(frame_copy, P, (477, 477))

	# another copy to find the edges
	puzzle = cv2.warpPerspective(frame_copy, P, (477, 477))


	# Now we have a 477*477 frame that contains only the puzzle

	# We take a 477*477 frame as 477 is divisible by 9 (9 elements)

	


	# hough line transform
	edges = cv2.Canny(puzzle, 50, 200, 3)
	lines = cv2.HoughLines(edges, 1, np.pi/180, 150, 0, 0)

	gridAngleRad = -1
	gridAngleDeg = -1

	if lines != None:
		for i in xrange(len(lines)):
			lin = lines[i][0] # as it is a list of a list
			rho = lin[0]
			theta = lin[1]
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*a))
			pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*a))

			# If we need to draw the edges
			# cv2.line(puzzle, pt1, pt2, (10,200,100), 2)

			
			if theta >= (np.pi/180.0)* 65 and theta <= (np.pi/180.0)*115:
				# If the horizontal makes a slightly inclined angle between
				# 65 and 115 degrees, then store this angle

				# Because of the angle constrictions, none of the vertical lines
				# will be included
				gridAngleDeg = (theta*180)/np.pi
				gridAngleRad = theta

				# now break as we have the required slope for slope correction
				break

	# Now we rotate the main image

	# first we rotate the frame_dil_rot 

	# if gridAngle is less than 90, then the angle becomes negative and rotation
	# is clockwise as needed.
	# similarly for anticlockwise
	if gridAngleDeg != -1:
		rot = cv2.getRotationMatrix2D((240, 320), gridAngleDeg-90,1 )
		frame_dil_rot = cv2.warpAffine(frame_dil_rot, rot, (640,480))
		frame_dil_rot_copy = frame_dil_rot.copy()
		frame_rot = cv2.warpAffine(frame_rot, rot, (640, 480))

		# Now we find the contours and perspective points again


		# ---------------------------------------------------------------------------------

		_, contours, _ = cv2.findContours(frame_dil_rot_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

		# signify if contours are empty
		contempty = False


		

		# contour with largest perimeter
		if len(contours)!=0:
			cont = contours[largest_bounding_pos]
		else:
			contempty = True





		# Filling the contour with largest perimeter
		if not contempty:
			# Dont compute if no contours found

			# Display the contour if needed
			cv2.drawContours(frame_rot, [contours[largest_bounding_pos]], 0, (100,100,177), -1)

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


			# drawing corners
			cv2.circle(frame_rot, topleft, 5, (0,0, 255), -1)
			cv2.circle(frame_rot, topright, 5, (0,0, 255), -1)
			cv2.circle(frame_rot, botleft, 5, (0,0, 255), -1)
			cv2.circle(frame_rot, botright, 5, (0,0, 255), -1)


		# Applying a perspective transform to get only the grid on the frame
		# This is the first rough perspective transform. No angle correction is added

		# Points on the main frame
		grid_points = np.float32([list(topleft), list(topright), list(botleft), list(botright)])
		# Corresponding points on the puzzle frame
		puzzle_points = np.float32([[0,0], [477,0], [0,477], [477,477]])

		P = cv2.getPerspectiveTransform(grid_points, puzzle_points)
		# The puzzle frame
		puzzle_frame = cv2.warpPerspective(frame_rot, P, (477, 477))

		# another copy to find the edges
		puzzle = cv2.warpPerspective(frame_rot, P, (477, 477))
	


	# We can now draw the 9 grids to separate the numbers.
	for i in xrange(9):

		square_width = 477/9
		# Drawing columns
		cv2.line(puzzle_frame, (i*square_width, 0), (i*square_width, 477), (150,10,10), 1)

		# Drawing rows
		cv2.line(puzzle_frame, (0, i*square_width), (477, i*square_width), (150, 10, 10), 1)













	# displaying
	# cv2.imshow('frame', frame)
	# cv2.imshow('puzzle', puzzle_frame)
	# cv2.imshow('puzzle', puzzle)
	# cv2.imshow('edges', edges)
	# cv2.imshow('rot', frame_dil_rot)
	cv2.imshow('frame rot', puzzle)




	if cv2.waitKey(1) & 0xff == 27:
		break

cap.release()
cv2.destroyAllWindows()

