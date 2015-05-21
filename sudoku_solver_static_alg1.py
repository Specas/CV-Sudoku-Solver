import cv2
import numpy as np 

# THIS PROGRAM IS TO TEST OUT ALGORITHMS FOR READING THE SUDOKU PUZZLE
# IT WORKS ON AN IMAGE, AND NOT ON THE WEBCAM VIDEO

img = cv2.imread("sudoku.jpg")
imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# kernel for morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

# blurring the image
blur = cv2.GaussianBlur(imggray, (11, 11), 0)
# adaptive thresholding
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

# bitwise not to invert, so that the grid that we need is white
inv = cv2.bitwise_not(thresh)

# dilating to fill up the pores
dil = cv2.dilate(inv, kernel, iterations = 1)

# making copy to find the contours
base = dil.copy()

# finding contours
_, contours, _ = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# finding contour with largest perimeter as this gives the bounding grid
largest_perimeter_value = 0
largest_perimeter_pos = 0
for i in xrange(len(contours)):
	per = cv2.arcLength(contours[i], True)
	if per>largest_perimeter_value:
		largest_perimeter_value = per
		largest_perimeter_pos = i 

# drawing bounding rect over this
x,y,w,h = cv2.boundingRect(contours[largest_perimeter_pos])
img = cv2.rectangle(img, (x, y), (x+w, y+h), (50,200,30), 2)

print largest_perimeter_pos
cv2.drawContours(img, [contours[33]],0, (100,100,200), -1)



cv2.imshow("pic", base)
cv2.imshow("cont", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print img.shape