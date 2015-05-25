# THIS PROGRAM IS USED FOR POSTPROCESSING
# AT THIS STAGE, WE HAVE AN IMAGE OF 477*477 PIXELS THAT CONTAINS ONLY THE
# PUZZLE. USING THE FUNCTIONS IN THIS MODULE, WE EXTRACT EACH OF THE 81 SQUARES
# IN THE PUZZLE GRID. EACH OF THE SQUARES IS THEN PASSED TO THE OCR MODULE WHERE
# THE NUMBERS ARE READ AND SENT TO THE CORE PROGRAM

import cv2
import numpy as np 
import tess_ocr as ocr

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))

# Initially we have the raw puzzle image
# We need to threshold this for proper OCR
def processGrid(grid):
	# Grid is the puzzle image that we work with. It is computed by the core 
	# program

	# First we convert it to grayscale
	grid_gray = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)

	# Blurring
	grid_blur = cv2.GaussianBlur(grid_gray, (11, 11), 0)

	# Adaptive thresholding
	grid_thresh = cv2.adaptiveThreshold(grid_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

	# Inverting to dilate
	grid_tmp_inv = cv2.bitwise_not(grid_thresh)

	# dilating
	grid_dilate = cv2.dilate(grid_tmp_inv, kernel, iterations = 1)

	# Inverting again
	grid_dilate = cv2.bitwise_not(grid_dilate)

	# returning
	return grid_dilate



# After the puzzle is prepared by thresholding an dilating, we need to extract
# each of the individual squares
def extractSquares(puzzle):
	
	# Puzzle is the image from the core program that contains only the puzzle
	# We now extract each of the 81 squares that make up the puzzle

	# squares is a list of 81 elements where each element is a numpy array 
	# corresponding to that particular square
	squares = []
	for i in xrange(9):
		for j in xrange(9):

			# extracting
			squares.append(puzzle[53*i: 53*i+53 , 53*j: 53+53*j])

	# returning
	return squares

def sendOcr(list_of_squares):

	# lis_of_squares is a list of 81 numpy arrays that represent the square

	# Stores the list of the ocr read squares
	string_of_num = ""
	for i in xrange(81):
		string_of_num = string_of_num + str(ocr.readNumber(list_of_squares[i]))

	return string_of_num


