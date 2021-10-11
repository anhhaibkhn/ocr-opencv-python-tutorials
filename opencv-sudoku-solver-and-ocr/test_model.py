# run this to test the ocr digits model 
# python test_model.py --image failed_9.png --model output/digit_classifier.h5 --debug 1
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist as mnist
from sklearn.metrics import classification_report

import argparse
import imutils
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from pyimagesearch.Sudoku.puzzle import extract_digit

from pathlib import Path



def loading_model(model_path, trainData, trainLabels,testData, testLabels):
	# load the digit classifier from disk
	print("[INFO] ==================== loading digit classifier... ====================")
	# print(model_path)
	model = load_model(model_path)

	print("[INFO] ==================== Model Summary... ====================")
	
	print(model.name)
	# preprocessing input data for the model input
	if model.name == "pyimagesearch_sequential.h5":
		# add a channel (i.e., grayscale) dimension to the digits
		trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
		testData = testData.reshape((testData.shape[0], 28, 28, 1))
		# scale data to the range of [0, 1]
		trainData = trainData.astype("float32") / 255.0
		testData = testData.astype("float32") / 255.0

	model.summary()
	for layer in model.layers:
		print(layer.get_output_at(0).get_shape().as_list())

	# Make prediction from test data
	prediction_probability = model.predict(testData)
	prediction = np.array([np.argmax(pred) for pred in prediction_probability])

	# Display the model performance
	print(classification_report(testLabels, prediction))

	return model

def change_model_name(model_path, new_name):
	"""changing model name"""
	print("[INFO] ==================== changing model name...====================")
	model = load_model(model_path)
	# changing model name
	model._name = new_name

	# replace the old model. 
	old_name = Path(model_path).name

	new_path = Path(str(model_path).replace(old_name,new_name))
	model.save(new_path)

	print("[INFO] Model new name", new_path)
	


def process_image(image_path, debug=0):
	print("[INFO] ==================== processing image...====================")
	digit = cv2.imread(image_path)
	# convert RGB image to grayscale
	digit = digit[:,:,0]

	if debug > 0:
		cv2.imshow("failed image", digit)
		cv2.waitKey(0)

	# digit = extract_digit(image, debug=args["debug"] > 0)
	return digit


def identify_number(image, model):
	print("[INFO] =================== Identifying Number... ===================")
	image_resize = cv2.resize(image, (28,28))    # For plt.imshow
	
	roi = image_resize.astype("float") / 255.0
	roi = img_to_array(roi)
	roi = np.expand_dims(roi, axis=0)
	print(roi.shape)

	pred = model.predict(roi).argmax(axis=1)[0]
	return pred




if __name__ == "__main__":

	# 1 construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-m", "--model", required=True,
		help="path to trained digit classifier")
	ap.add_argument("-i", "--image", required=True,
		help="path to input Sudoku puzzle image")
	ap.add_argument("-d", "--debug", type=int, default=-1,
		help="whether or not we are visualizing each step of the pipeline")
	args = vars(ap.parse_args())
	print(args)


	# 2: load model and show performance
	# grab the MNIST dataset
	print("[INFO] accessing MNIST...")
	((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()
	loaded_model = loading_model(args["model"], trainData, trainLabels,testData, testLabels)

	# 3: # 2: load the input image from disk and resize it
	digit = process_image(args["image"], args["debug"])
	
	# 4: identify the number
	pred = identify_number(digit, loaded_model)
	print(pred)


	# # only use when model name needs to be changed
	# change_model_name(args["model"], "pyimagesearch_sequential.h5")