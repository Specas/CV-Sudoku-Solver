# THIS PROGRAM TAKES THE FINAL OUTPUT FROM THE CORE PROGRAM
# THE FINAL PERSPECTIVE TRANSFORMED PUZZLE GRID IS NOW SPLIT UP INTO ITS INDIVIDUAL SQUARES
# THE INDIVIDUAL SQUARES ARE PASSED TO ANOTHER PROGRAM FOR OCR

import numpy as np 
import cv2 

def drawGrid(grid):

	# grid is the input that is perspective transformed
	# drawing the 9*9 grid on this image
	# another array to draw on as we dont want to draw on the original
	gr = grid.copy()
	for i in xrange(9):

		square_width = 477/9
		# Drawing columns
		cv2.line(gr, (i*square_width, 0), (i*square_width, 477), (150,10,100), 1)

		# Drawing rows
		cv2.line(gr, (0, i*square_width), (477, i*square_width), (150, 10, 100), 1)

	# returning 
	return gr
