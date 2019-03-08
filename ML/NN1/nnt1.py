import tensorflow as tf
from tensorflow import keras
import datasource
import time

ts = time.gmtime()


# get bulk data
X_train, y_train, X_test, y_test = datasource.get_data()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(4, datasource.timepointwidth)),
    keras.layers.Dense(128, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    keras.layers.Dense(128, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    keras.layers.Dense(128, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#tb
tb_cb = tf.keras.callbacks.TensorBoard(log_dir='./logs', write_graph=True, update_freq='epoch')

model.fit(X_train, y_train, epochs=10, callbacks=[tb_cb])

print('Training Complete - Saving Model')
model.summary()
model.save('models/nnt1.h5')

test_loss, test_acc = model.evaluate(X_test, y_test)

print('Test Accuracy:', test_acc)

predictions = model.predict(X_test)

print('Predicts: ' + str(predictions[0]) + ' <-> Is actually: ' + str(y_test[0]))

