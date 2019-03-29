import datasource_lstm as datasource
import tensorflow as tf
from tensorflow import keras
import numpy as np
# get bulk data
X_train, X_test = datasource.lstm_transpose(datasource.get_data())
y_train = X_train[:, -1, [0, 2, 4]]
X_train = X_train[:, 0:-1, [0, 2, 4]]
y_test = X_test[:, -1, [0, 2, 4]]
X_test = X_test[:, 0:-1, [0, 2, 4]]
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)




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

model.fit(X_train, y_train, batch_size=512, epochs=8, shuffle=True)
model.summary()
test_loss = model.evaluate(X_test, y_test, batch_size=512)

print('Test Loss:', test_loss)
