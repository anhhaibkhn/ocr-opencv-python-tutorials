
from tensorflow.keras.models import load_model
import argparse
import imutils
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from pyimagesearch.Sudoku.puzzle import extract_digit


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained digit classifier")
ap.add_argument("-i", "--image", required=True,
	help="path to input Sudoku puzzle image")
ap.add_argument("-d", "--debug", type=int, default=-1,
	help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())


# load the digit classifier from disk
print("[INFO] loading digit classifier...")
model = load_model(args["model"])
# load the input image from disk and resize it
print("[INFO] processing image...")
digit = cv2.imread(args["image"])
# image = imutils.resize(image, width=600)
cv2.imshow("failed image", image)
cv2.waitKey(0)

# digit = extract_digit(image, debug=args["debug"] > 0)


roi = cv2.resize(digit, (28, 28))
roi = roi.astype("float") / 255.0
roi = img_to_array(roi)
roi = np.expand_dims(roi, axis=0)
# classify the digit and update the Sudoku board with the
# prediction
pred = model.predict(roi).argmax(axis=1)[0]
print(pred)