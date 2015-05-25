# THIS PROGRAM MAKES USE OF THE PYTHON TESSERACT LIBRARY FOR OPTICAL CHARACTER
# RECOGNITION (OCR)

# THE SUDOKU FILE THAT WAS PREPROCESSED IS SENT TO THIS CODE WHICH THEN RETURNS
# THE NUMBERS TO THE CORE PROGRAM


import Image
import pytesseract as pt

def readNumbers():

	# img is the image which is to be subjected to ocr
	return pt.image_to_string(Image.open('numForOCR.jpg'))



