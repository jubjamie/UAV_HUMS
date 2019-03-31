import tensorflow as tf
from tensorflow import keras
import datasource
import time
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

ts = time.gmtime()

# get bulk data
X_train, y_train, X_test, y_test, enc_classes = datasource.get_data(newdata=False)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(6, datasource.timepointwidth)),
    keras.layers.Dense(128, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.Dense(128, activation=tf.nn.relu, use_bias=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#tb
tb_cb = tf.keras.callbacks.TensorBoard(log_dir='./logs', write_graph=True, update_freq='epoch')

history = model.fit(X_train, y_train, batch_size=16, epochs=16, shuffle=True, validation_split=0.15)

print('Training Complete - Saving Model')
model.summary()
model.save('models/nnt2_2x64.h5')

# summarize history for accuracy
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='lower right')
plt.savefig('train_acc.png')

test_loss, test_acc = model.evaluate(X_test, y_test)

print('Test Accuracy:', test_acc)

predictions = model.predict(X_test)

print('Predicts: ' + str(predictions[0]) + ' <-> Is actually: ' + str(y_test[0]))

cm = confusion_matrix(y_test, np.argmax(predictions, axis=1))
cm_raw = cm
cm = np.true_divide(cm, cm.sum(axis=1, keepdims=True))
print(cm)
labels = ['Healthy', 'Failure']
fig = plt.figure()
ax = fig.add_subplot(111)
plt.set_cmap('winter')
cax = ax.matshow(cm)
plt.title('Confusion matrix of the classifier')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
for xx in range(cm.shape[0]):
    for yy in range(cm.shape[1]):
        text = ax.text(xx, yy, "{0:.2%}\n({1})".format(cm[xx, yy], cm_raw[xx, yy]), ha="center", va="center", color="w")
        text.set_bbox(dict(facecolor='black', alpha=0.4, edgecolor='black'))
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig('confidenceMatrix1.png')
plt.show()
