""" 
As with all CNNs, SudokuNet needs to be trained with data. 
This train_digit_classifier.py script will train a digit OCR model on the MNIST dataset.
"""
# Usage: python train_digit_classifier.py --model output/pyimagesearch_sequential.h5
import sys 
sys.path.append('pyimagesearch\models\Sudokunet.py')
from pyimagesearch.models import Sudokunet as sdk
SudokuNet = sdk.SudokuNet()

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
import argparse
from pathlib import Path

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to output model after training")
args = vars(ap.parse_args())


# initialize the initial learning rate, number of epochs to train
# for, and batch size
INIT_LR = 1e-3
### 10 EPOCHS was not enough to get a good accuracy for 8 and 9 pics
EPOCHS = 30
BS = 128
# grab the MNIST dataset
print("[INFO] accessing MNIST...")
((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()
# add a channel (i.e., grayscale) dimension to the digits
trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
testData = testData.reshape((testData.shape[0], 28, 28, 1))
# scale data to the range of [0, 1]
trainData = trainData.astype("float32") / 255.0
testData = testData.astype("float32") / 255.0
# convert the labels from integers to vectors
le = LabelBinarizer()
trainLabels = le.fit_transform(trainLabels)
testLabels = le.transform(testLabels)


# initialize the optimizer and model
print("[INFO] compiling model...")
opt = Adam(lr=INIT_LR)
model = SudokuNet.build(width=28, height=28, depth=1, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])
# train the network
print("[INFO] training network...")
H = model.fit(
	trainData, trainLabels,
	validation_data=(testData, testLabels),
	batch_size=BS,
	epochs=EPOCHS,
	verbose=1)


# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testData)
print(classification_report(
	testLabels.argmax(axis=1),
	predictions.argmax(axis=1),
	target_names=[str(x) for x in le.classes_]))
# serialize the model to disk
print("[INFO] serializing digit model...")

# save model and its name 
model._name = Path(args["model"]).name
model.save(args["model"], save_format="h5")