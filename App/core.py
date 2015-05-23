# THIS IS THE CORE PROGRAM
# IT CALLS ALL THE OTHER HELPER FUNCTIONS
# IT TAKES THE WEBCAM INPUT. ITS FINAL OUTPUT ARE THE INDIVIDUAL SQUARES
# OCR IS IMPLEMENTED BY ANOTHER MODULE

import cv2 
import numpy as np
import preprocess as pr

# webcam input
cap = cv2.VideoCapture(0)

# points on the perspective transformed puzzle
puzzle_corner = np.float32([[0,0], [477,0], [0,477], [477,477]])

# initial and final values
# initial after normal operation
# final after angle correction
initial_frame = final_frame = []
initial_dil = final_dil = []
initial_corner = final_corner = []
initial_pers_trans = final_pers_trans = []
initial_puzzle_frame = final_puzzle_frame = []

# The rotation matrix
rot_matrix = []

while cap.isOpened():

	_, frame = cap.read()

	# frame copy for initial processes
	initial_frame = frame
	final_frame = frame


	# finding initial corner points ------------------------------------------------------------------

	# calling the init function to give the dilated frame
	initial_dil = pr.init(frame)

	# we get the corners of the sudoku grid. 
	# This is the first run, hence there is no angle correction
	initial_corner = pr.contourEndPoints(initial_dil)

	# proceed only if there are contours
	if initial_corner != 0:
		initial_corner = np.float32(initial_corner)

		# perspective transformation
		initial_pers_trans = cv2.getPerspectiveTransform(initial_corner, puzzle_corner)
		initial_puzzle_frame = cv2.warpPerspective(initial_frame, initial_pers_trans, (477,477))
		final_puzzle_frame = initial_puzzle_frame # inital value


		# now we find the angle correction and hence the new corners ----------------------------------

		# finding the hough lines. First we use canny edge detection
		edges = cv2.Canny(initial_puzzle_frame, 50, 200, 3)
		lines = cv2.HoughLines(edges, 1, np.pi/180, 150, 0, 0)

		# The inclination of the puzzle is stored in degrees
		gridAngleDeg = -1

		# proceed if lines exist
		if lines != None:

			for i in xrange(len(lines)):

				# Each line is a list of 2 points which is in a list itself
				lin = lines[i][0]

				# getting rho and theta values and finding the end points of the line
				rho = lin[0]
				theta = lin[1] # theta is in radians
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho
				pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*a))
				pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*a))

				# The maximum inclination of the puzzle that we allow is +/- 25 degrees
				if theta >= (np.pi/180.0)* 65 and theta <= (np.pi/180.0)*115: 

					# theta is the inclination of the line
					# for horizontal lines, theta is 90. It decreases while turning anticlockwise
					# and vice versa
					# hence for vertical lines, theta is zero
					gridAngleDeg = (theta*180)/np.pi

					# As soon as we encounter such an angle, we break as this much 
					# information is sufficient

					# vertical lines cannot make such angles, unless the puzzle is
					# inclined way too much
					break

		# Now that we have the inclination of the line, we can just rotate our image

		# Proceed only if the angle is found
		if gridAngleDeg != -1:


			# If the angle is less than 90, then we need to rotate it clockwise to 
			# balance and vice versa for anticlockwise
			# gridAngleDeg - 90 automatically takes care of the direction of rotation
			# as a negative values means clockwise rotation
			# We rotate about the center without scaling
			rot_matrix = cv2.getRotationMatrix2D((240, 320), gridAngleDeg-90, 1)
			# rotating the frame
			final_frame = cv2.warpAffine(final_frame, rot_matrix, (640,480))

			# calling the preprocess functions again to apply angle correction
			final_dil = pr.init(final_frame)
			final_corner = pr.contourEndPoints(final_dil)

			# proceed if there is a contour
			if final_corner != 0:

				final_corner = np.float32(final_corner)

				# perspective transformation
				final_pers_trans = cv2.getPerspectiveTransform(final_corner, puzzle_corner)
				final_puzzle_frame = cv2.warpPerspective(final_frame, final_pers_trans, (477,477))










	# display and close
	cv2.imshow('frame', initial_frame)
	# cv2.imshow('dil frame', initial_dil)
	# cv2.imshow('initial persp', initial_puzzle_frame)
	cv2.imshow('final persp', final_puzzle_frame)

	if cv2.waitKey(1) & 0xff == 27:
		break

cap.release()
cv2.destroyAllWindows()
