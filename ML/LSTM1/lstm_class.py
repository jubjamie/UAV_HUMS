import datasource
from tensorflow import keras
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# get bulk data
X_train, y_train_b, X_test, y_test_b, enc_classes = datasource.get_data(classtype='binary')
# Transpose for LSTMS
X_train, y_train_b, X_test, y_test_b = datasource.lstm_transpose(X_train, y_train_b, X_test, y_test_b)
classes = len(enc_classes)
# Convert to one-hot
y_train = keras.utils.to_categorical(y_train_b, classes)
y_test = keras.utils.to_categorical(y_test_b, classes)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

# Build model using Keras Layers
model = keras.Sequential([
    keras.layers.LSTM(input_shape=(X_train.shape[1], X_train.shape[2]), units=X_train.shape[1], return_sequences=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.LSTM(16, return_sequences=True),
    keras.layers.Dropout(rate=0.2),
    keras.layers.LSTM(16),
    keras.layers.Dense(classes, activation='softmax')
])

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

history = model.fit(X_train, y_train, batch_size=16, epochs=16, shuffle=True, validation_split=0.15)
model.summary()
model.save('models/lstm_' + str(classes) + '_classes_' + str(X_train.shape[1]) + '_3x16.h5')

# summarize history for accuracy
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='lower right')
plt.savefig('train_acc.png')

# Run tests
test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=16)

print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)

predictions = model.predict(X_test)

print('Predicts: ' + str(predictions[0]) + ' <-> Is actually: ' + str(y_test[0]))

# Create confusion matrix
cm = confusion_matrix(y_test_b, np.argmax(predictions, axis=1))
cm_raw = cm
cm = np.true_divide(cm, cm.sum(axis=1, keepdims=True))
print(cm)
labels = enc_classes
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
