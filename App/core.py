# THIS IS THE CORE PROGRAM
# IT CALLS ALL THE OTHER HELPER FUNCTIONS
# IT TAKES THE WEBCAM INPUT. ITS FINAL OUTPUT ARE THE INDIVIDUAL SQUARES
# OCR IS IMPLEMENTED BY ANOTHER MODULE

import cv2 
import numpy as np
import preprocess as pr

# webcam input
cap = cv2.VideoCapture(0)

while cap.isOpened():

	_, frame = cap.read()

	# calling the init function to give the dilated frame
	initial_dil = pr.init(frame)



	# display and close
	cv2.imshow('frame', initial_dil)

	if cv2.waitKey(1) & 0xff == 27:
		break

cap.release()
cv2.destroyAllWindows()
