# THIS PROGRAM MAKES USE OF THE PYTHON TESSERACT LIBRARY FOR OPTICAL CHARACTER
# RECOGNITION (OCR)

# THE SUDOKU FILE THAT WAS POSTPROCESSED IS SENT TO THIS CODE WHICH THEN RETURNS
# THE NUMBERS TO THE CORE PROGRAM


import Image
import pytesseract as pt
import cv2

def readNumber(img):

	# square is the image which is to be subjected to ocr
	# but img is a numpy array. Thus we first convert it to a PIL image
	# and then use pytesseract
	return pt.image_to_string(Image.fromarray(img))



