# import the necessary packages
from transform import four_point_transform
from skimage.filters import threshold_local
import matplotlib.pyplot as plt

import numpy as np
import argparse
import cv2
import imutils
import pytesseract
import re 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())


# --------------------------------Step 1: Edge Detection--------------------------------
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(6000)
cv2.destroyAllWindows()

# ----------------------------------Step 2: Finding Contours----------------------------------
""" assume that the largest contour in the image with exactly four points is 
our piece of paper to be scanned."""
# find the contours in the edged image, keeping only the
# largest ones, and initialize the receipt outline contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# initialize a contour that corresponds to the receipt outline
receiptCnt = None

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our receipt outline
	if len(approx) == 4:
		receiptCnt = approx
		break

# if the receipt contour is empty then our script could not find the
# outline and we should be notified
if receiptCnt is None:
	raise Exception(("Could not find receipt outline. "
		"Try debugging your edge detection and contour steps."))


# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [receiptCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(6000)
cv2.destroyAllWindows()


#----------------------------Step 3: Apply a Perspective Transform & Threshold-----------------------
# apply the four point transform to obtain a top-down
# view of the original image
receipt  = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)
# convert the receipt  image to grayscale, then threshold it
# to give it that 'black and white' paper effect
receipt  = cv2.cvtColor(receipt , cv2.COLOR_BGR2GRAY)
T = threshold_local(receipt , 11, offset = 10, method = "gaussian")
receipt  = (receipt  > T).astype("uint8") * 255
# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(receipt , height = 650))
cv2.waitKey(6000)
cv2.destroyAllWindows()


#----------------------------Step 4: Given the top-down view -> OCR it ----------------------------
# apply OCR to the receipt image by assuming column data, ensuring
# the text is *concatenated across the row* (additionally, for your
# own images you may need to apply additional processing to cleanup
# the image, including resizing, thresholding, etc.)

# tesseract--psm 4, allows us to OCR the receipt line-by-line
options = "--psm 4"
text = pytesseract.image_to_string(
	cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
	config=options)
# show the raw output of the OCR process
print("[INFO] raw output:")
print("==================")
print(text)
print("\n")

# define a regular expression that will match line items that include
# a price component
pricePattern = r'([0-9]+\.[0-9]+)'
# show the output of filtering out *only* the line items in the
# receipt
print("[INFO] price line items:")
print("========================")
# loop over each of the line items in the OCR'd receipt
for row in text.split("\n"):
	# check to see if the price regular expression matches the current
	# row
	if re.search(pricePattern, row) is not None:
		print(row)