from NN1 import datasource
import tensorflow as tf
from tensorflow import keras
import numpy as np
# get bulk data
X_train, X_test = datasource.lstm_transpose(datasource.get_data())
y_train = X_train[:, -1, [0, 2, 4]]
X_train = X_train[:, 0:-1, [0, 2, 4]]
print(X_train.shape)
print(y_train.shape)




model = keras.Sequential([
    keras.layers.LSTM(input_shape=(19, 3), units=19, return_sequences=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.LSTM(128, return_sequences=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.LSTM(128, return_sequences=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.LSTM(128),
    keras.layers.Dropout(rate=0.2),
    keras.layers.Dense(3, activation='linear')
])

model.compile(loss="mse", optimizer="adam")
model.summary()

model.fit(X_train, y_train, batch_size=512, epochs=16, shuffle=True)
