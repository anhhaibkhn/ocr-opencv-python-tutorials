### This model could not recognize the digit in the failed_9.png image even after training with 50 epochs.
from tensorflow import keras
from sklearn.metrics import classification_report
import numpy as np

# Load data provided by keras
data = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = data.load_data()

# Create model using sequential API
model = keras.Sequential([
    # Input Layers
    keras.layers.Flatten(input_shape=(28, 28, )),
	# Hidden Layers
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    # Output Layers
    keras.layers.Dense(10, activation='softmax')
])

# Compile model
model.compile(
    optimizer = keras.optimizers.Adam(),
    loss = keras.losses.SparseCategoricalCrossentropy(),
    metrics = ['accuracy']
)

# Model training
model.fit(x_train, y_train, verbose=1, epochs=50, batch_size=32)

# Make prediction from test data
prediction_probability = model.predict(x_test)
prediction = np.array([np.argmax(pred) for pred in prediction_probability])

# Display the model performance
print(classification_report(y_test, prediction))

# Save model
model._name = 'mnist_classification.h5'
model.save('\output\mnist_classification.h5')
