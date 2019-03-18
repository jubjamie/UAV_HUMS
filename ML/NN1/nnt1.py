import tensorflow as tf
from tensorflow import keras
import datasource
import time
import numpy as np

ts = time.gmtime()

# get bulk data
X_train, y_train, X_test, y_test = datasource.get_data()
#expand for CNN
X_train = np.expand_dims(X_train, axis=3)
X_test = np.expand_dims(X_test, axis=3)

model = keras.Sequential([
    keras.layers.Conv2D(128, (6, 5), 1, input_shape=(6, datasource.timepointwidth, 1), data_format='channels_last',
                        padding='same', activation='relu'),
    keras.layers.Conv2D(128, (6, 4), 1, data_format='channels_last', padding='same', activation='relu'),
    keras.layers.Conv2D(128, (6, 1), 1, data_format='channels_last', padding='same', activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    keras.layers.Dense(64, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    keras.layers.Dense(2, activation=tf.nn.softmax)

])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#tb
tb_cb = tf.keras.callbacks.TensorBoard(log_dir='./logs', write_graph=True, update_freq='epoch')

model.fit(X_train, y_train, batch_size=256, epochs=64, shuffle=True, callbacks=[tb_cb])

print('Training Complete - Saving Model')
model.summary()
model.save('models/cnnt3.h5')

test_loss, test_acc = model.evaluate(X_test, y_test)

print('Test Accuracy:', test_acc)

predictions = model.predict(X_test)

print('Predicts: ' + str(predictions[0]) + ' <-> Is actually: ' + str(y_test[0]))

