import tensorflow as tf
import numpy as np
import threading
import time
import matplotlib.pyplot as plt


class HealthMonitor:
    def __init__(self, controller, datafeed, displaybool=True):
        self.thread_object = None
        self.run = True
        self.ctrl_obj = controller
        self.datafeed = datafeed
        self.model = None
        self.displaybool = True
        self.sim_clock_data = np.array([0])
        self.health_data = np.array([0])
        if self.displaybool is True:
            self.health_fig, self.health_axs = plt.subplots()
            self.health_axs.plot(self.sim_clock_data, self.health_data)
            #plt.show()
        self.labelmodes = ['healthy', 'damaged']
        # tf.keras.backend.clear_session()
        # self.load_model()

    def checkhealth(self):
        x_data, sim_time = self.datafeed()
        x_input = x_data.T
        x_input = np.expand_dims(x_input, axis=0)
        # print(x_input.shape)
        try:
            assert(x_input.shape == (1, 6, 10))
        except AssertionError:
            return
        #tf.keras.backend.clear_session()
        predictions = self.model.predict([x_input])
        print(str(np.argmax(predictions[0])))
        if self.displaybool is True:
            self.sim_clock_data = np.append(self.sim_clock_data, sim_time)
            self.health_data = np.append(self.health_data, np.argmax(predictions[0]))
            self.health_axs.clear()
            self.health_axs.plot(self.sim_clock_data, self.health_data)


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
        print('Flight status mode:')
        print(np.around(np.mean(self.health_data)))
