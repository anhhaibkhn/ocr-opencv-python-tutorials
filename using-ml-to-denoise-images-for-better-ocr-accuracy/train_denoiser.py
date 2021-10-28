""" this file trains the actual RFR model and serializes it to disk as denoiser.pickle

    - RandomForestRegressor: The scikit-learn implementation of the regression model we’ll use to predict pixel values
    - mean_squared_error: Our error/loss function — the lower this value, the better job we are doing at denoising our images
    - train_test_split: Used to create a training/testing split from our features.csv file
    - pickle: Used to serialize our trained RFR to disk

 """
# import the necessary packages
from config import denoise_config as config
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

# initialize lists to hold our features and target predicted values
print("[INFO] loading dataset...")
features = []
targets = []

# loop over the rows in our features CSV files
for row in open(config.FEATURES_PATH):
    # parse the row and extract (1) the target pixel value to predict 
    # and (2) the 5x5 pixels which serve as feature vector
    row = row.strip().split(",")
    row = [float(x) for x in row]
    target, pixels = row[0], row[1:]

    # update our features and targets lists, respectively
    features.append(pixels)
    targets.append(target)

# convert the features and targets to NumPy arrays
features = np.array(features, dtype="float")
target = np.array(targets, dtype="float")
# construct our training and testing split, using 75% for training, 25% for testing
(trainX, testX, trainY, testY) = train_test_split(features, target, test_size=0.25, random_state=42)   

# train a random forest regressor on our data
print("[INFO] training model...")
model = RandomForestRegressor(n_estimators=10)
model.fit(trainX, trainY)
# compute the root mean squared error on the testing set
print("[INFO] evaluating model...")
preds = model.predict(testX)
rmse = np.sqrt(mean_squared_error(testY, preds))
print("[INFO] rmse: {}".format(rmse))
# serialize our random forest regressor to disk
with open(config.MODEL_PATH, "wb") as f:
    f.write(pickle.dumps(model))
