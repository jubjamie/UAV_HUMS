import tensorflow as tf
import numpy as np
import threading
import time
import matplotlib.pyplot as plt


class HealthMonitor:
    def __init__(self, controller, datafeed, use_lstm=False, displaybool=True):
        self.thread_object = None
        self.thread_object_scope = None
        self.run = True
        self.ctrl_obj = controller
        self.datafeed = datafeed
        self.model = None
        self.displaybool = displaybool
        self.sim_clock_data = np.array([0])
        self.health_data = np.array([0])
        self.predict_confidence = np.array([0])
        if self.displaybool is True:
            self.health_fig, self.health_axs = plt.subplots(ncols=1, nrows=1)
            self.health_axs.set_xlabel('Simulation Time')
            self.health_axs.set_ylabel('Classifier Output')
            self.health_axs.plot(self.sim_clock_data, self.health_data)
            plt.pause(0.000000000000001)
            #plt.show()

        self.use_lstm = use_lstm
        self.labelmodes = ['healthy', 'damaged']
        self.sim_time = []
        self.predictions = []
        self.newstatus = 0
        self.status_list = ['Healthy', 'Failure']
        self.laststatus = 1
        # tf.keras.backend.clear_session()
        # self.load_model()

    def checkhealth(self):
        x_data, self.sim_time = self.datafeed()
        x_input = x_data.T
        x_input = np.expand_dims(x_input, axis=0)
        # print(x_input.shape)
        if self.use_lstm:
            x_input = np.transpose(x_input, (0, 2, 1))
            try:
                assert(x_input.shape == (1, 20, 6))
            except AssertionError:
                return
        else:
            try:
                assert(x_input.shape == (1, 6, 20))
            except AssertionError:
                return
        #tf.keras.backend.clear_session()
        self.predictions = self.model.predict([x_input])
        #print(str(np.argmax(self.predictions[0])))
        #print(str(self.predictions[0]))

        self.sim_clock_data = np.append(self.sim_clock_data, self.sim_time)
        self.health_data = np.append(self.health_data, np.argmax(self.predictions[0]))
        self.predict_confidence = np.append(self.predict_confidence, self.predictions[0][0])
        self.newstatus = np.around(np.mean(self.health_data[-5:-1]))
        if self.newstatus == 1:
            warnstatus = ' - WARN' if np.mean(self.predict_confidence[-5:-1]) < 0.75 else ' - ALERT'
        else:
            warnstatus = ''
        if self.newstatus != self.laststatus:
            print('\r' + self.status_list[int(self.newstatus)] + warnstatus)
        self.laststatus = self.newstatus
        #self.health_axs.clear()
        #self.health_axs.plot(self.sim_clock_data, self.health_data)

    def hook_data(self):
        return self.sim_time, self.health_data

    def load_model(self):
        if self.use_lstm:
            self.model = tf.keras.models.load_model('ML/LSTM1/models/lstm_class1.h5')
        else:
            self.model = tf.keras.models.load_model('ML/NN1/models/nnt2.h5')
        self.model._make_predict_function()
        self.model.summary()

    def thread_run(self):
        print('Health Monitor Starting...')
        self.load_model()
        time.sleep(1)
        while self.run is True:
            # Loop through inference
            time.sleep(0.25)
            self.checkhealth()

    def scope_plotter(self):
        #print('Updating graph')
        self.health_axs.clear()
        self.health_axs.plot(self.sim_clock_data[:self.health_data.shape[0]], self.health_data)
        self.health_axs.plot(self.sim_clock_data, self.predict_confidence[:self.sim_clock_data.shape[0]], 'r')
        plt.pause(0.0000001)

    def start_thread(self):
        self.thread_object = threading.Thread(target=self.thread_run)
        self.thread_object.start()
        """
        if self.displaybool is True:
            self.thread_object_scope = threading.Thread(target=self.scope_plotter())
            self.thread_object_scope.start()"""

    def stop_thread(self):
        self.run = False
        print('Flight status mode:')
        print(np.around(np.mean(self.health_data)))
        print(np.count_nonzero(self.health_data == 0))
        print(np.count_nonzero(self.health_data == 1))
