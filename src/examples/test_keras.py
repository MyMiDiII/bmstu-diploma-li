import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import time
import tensorflow as tf

# Generate some random data
from utils.osm import sparce_ids

keys = sparce_ids

sort_indexes = np.argsort(keys)
N = len(keys)
keys = np.array(keys)[sort_indexes]
positions = np.arange(0, N) / (N - 1)

keys = (keys - np.min(keys)) / (np.max(keys) - np.min(keys))



input_dim = 1
# Define the model architecture
model = Sequential()
model.add(Dense(32, input_dim=input_dim, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(loss=tf.keras.losses.MeanSquaredError(),
              optimizer=tf.keras.optimizers.SGD(1e-2))

# Start the timer
start_time = time.time()

# Train the model
model.fit(keys, positions, epochs=30, batch_size=1, verbose=0)

# Calculate the training time
training_time = time.time() - start_time
print("Keras training time:", training_time, "seconds")

start_time = time.time()

# Train the model
model.predict(keys, verbose=0)

# Calculate the training time
training_time = time.time() - start_time
print("Keras training time:", training_time, "seconds")
