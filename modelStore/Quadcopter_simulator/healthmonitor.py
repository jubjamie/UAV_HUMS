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

    def checkhealth(self):
        print(self.datafeed())
        pass

    def load_model(self):
        pass

    def thread_run(self):
        print('Health Monitor Booting...')
        self.load_model()
        while self.run is True:
            # Loop through inference
            self.checkhealth()
            time.sleep(0.25)

    def start_thread(self):
        self.thread_object = threading.Thread(target=self.thread_run)
        self.thread_object.start()

    def stop_thread(self):
        self.run = False
