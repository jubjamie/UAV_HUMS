import tensorflow as tf
import numpy as np
import threading
import time


class HealthMonitor:
    def __init__(self, controller, datafeed):
        self.thread_object = None
        self.run = True
        self.ctrl_obj = controller
        self.datafeed = datafeed
        self.model = None
        # tf.keras.backend.clear_session()
        # self.load_model()

    def checkhealth(self):
        x_input = self.datafeed().T
        x_input = np.expand_dims(x_input, axis=0)
        # print(x_input.shape)
        assert(x_input.shape == (1, 4, 10))
        #tf.keras.backend.clear_session()
        predictions = self.model.predict([x_input])
        print(np.argmax(predictions[0]))

    def load_model(self):
        self.model = tf.keras.models.load_model('ML/NN1/models/nnt1.h5')
        self.model._make_predict_function()
        self.model.summary()

    def thread_run(self):
        print('Health Monitor Starting...')
        self.load_model()
        time.sleep(1)
        while self.run is True:
            # Loop through inference
            time.sleep(0.05)
            self.checkhealth()

    def start_thread(self):
        self.thread_object = threading.Thread(target=self.thread_run)
        self.thread_object.start()

    def stop_thread(self):
        self.run = False
