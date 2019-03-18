import tensorflow as tf
from tensorflow import keras
import datasource
import time
from sklearn.metrics import confusion_matrix
import numpy as np

ts = time.gmtime()

# get bulk data
X_train, y_train, X_test, y_test = datasource.get_data()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(6, datasource.timepointwidth)),
    keras.layers.Dense(16, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    keras.layers.Dense(16, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.3),
    #keras.layers.Dense(10, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#tb
tb_cb = tf.keras.callbacks.TensorBoard(log_dir='./logs', write_graph=True, update_freq='epoch')

model.fit(X_train, y_train, batch_size=64, epochs=128, shuffle=True, callbacks=[tb_cb])

print('Training Complete - Saving Model')
model.summary()
model.save('models/nnt2.h5')

test_loss, test_acc = model.evaluate(X_test, y_test)

print('Test Accuracy:', test_acc)

predictions = model.predict(X_test)

print('Predicts: ' + str(predictions[0]) + ' <-> Is actually: ' + str(y_test[0]))

cm = confusion_matrix(y_test, np.argmax(predictions, axis=1))
print(cm)
