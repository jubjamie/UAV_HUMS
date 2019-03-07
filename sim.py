import modelStore.Quadcopter_simulator.uav_lookup as uav_lookup
import modelStore.Quadcopter_simulator.quad_sim as quad_sim
from modelStore.Quadcopter_simulator import quadcopter
import random
from tkinter import filedialog
from tkinter import *


class Sim:
    def __init__(self):
        self.GOALS = [(0, 0, 3), (2, -2, 4), (-1.5, 1.5, 1)]
        self.goal_time = 5
        self.YAWS = [0, 3.14, -1.54, 1.54]
        # Define the quadcopters
        self.QUADCOPTER = {
            'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5],
                   'weight': 1.2}}
        # Controller parameters
        self.CONTROLLER_PARAMETERS = {'Motor_limits': [7000, 27000],
                                      'Tilt_limits': [-10, 10],
                                      'Yaw_Control_Limits': [-900, 900],
                                      'Z_XY_offset': 500,
                                      'Linear_PID': {'P': [300, 300, 14000], 'I': [0.04, 0.04, 10],
                                                     'D': [450, 450, 8000]},
                                      'Linear_To_Angular_Scaler': [1, 1, 0],
                                      'Yaw_Rate_Scaler': 0.18,
                                      'Angular_PID': {'P': [22000, 22000, 1500], 'I': [0, 0, 1.2],
                                                      'D': [12000, 12000, 0]},
                                      }
        self.motor_modes = ['healthy', 'healthy', 'healthy', 'healthy']
        self.gui_mode = 1
        self.see_motor_gui = False
        self.see_gui = True
        self.time_scale = 1.0
        self.quad = 0
        self.save_path = None

    def set_params(self, goals=None, yaws=None, quad_params=None, ctlprms=None, goal_time=None):
        if goals is not None:
            self.GOALS = goals
        if yaws is not None:
            self.YAWS = yaws
        if quad_params is not None:
            self.QUADCOPTER = quad_params
        if ctlprms is not None:
            self.CONTROLLER_PARAMETERS = ctlprms
        if goal_time is not None:
            self.goal_time = goal_time
        self.quad = quadcopter.Quadcopter(self.QUADCOPTER, self.motor_modes)
        print('Basic Parameters Set')

    def reset_goals_to(self, goals):
        self.GOALS = goals

    def set_failure_mode(self, setting='defined', mode='healthy'):
        if setting == 'random':
            self.motor_modes = [random.choices(uav_lookup.modelist, weights=[70, 7, 7, 7, 9])[0],
                                random.choices(uav_lookup.modelist, weights=[70, 7, 7, 7, 9])[0],
                                random.choices(uav_lookup.modelist, weights=[70, 7, 7, 7, 9])[0],
                                random.choices(uav_lookup.modelist, weights=[70, 7, 7, 7, 9])[0]]
        elif setting == 'defined':
            if type(mode) is not list:
                if mode in uav_lookup.modelist:
                    self.motor_modes = [mode, mode, mode, mode]
                else:
                    raise ValueError('set_failure_mode: Mode not recognised')
            else:
                self.motor_modes = mode
        else:
            raise ValueError('set_failure_mode: Setting not recognised')
        self.quad.motor_modes = self.motor_modes
        print('Set motor modes to: ' + str(self.motor_modes))

    def get_failure_mode(self):
        return self.motor_modes

    def ask_save_destination(self):
        destination = str(filedialog.askdirectory())
        if not destination:
            sys.exit(0)
        else:
            print('Save path: ' + destination)
            self.set_save_destination(destination)
        return destination

    def set_save_destination(self, path='databin/test1/'):
        if path is None:
            path = self.ask_save_destination()
        self.save_path = path

    def run_sim(self):
        # Parse gui visibility logic
        if self.see_gui is True and self.see_motor_gui is True:
            self.gui_mode = 2
        elif self.see_gui is True and self.see_motor_gui is False:
            self.gui_mode = 1
        else:
            self.gui_mode = 0

        quad_sim.Single_Point2Point(self.GOALS, self.goal_time, self.YAWS, self.QUADCOPTER, self.CONTROLLER_PARAMETERS, self.motor_modes, self.gui_mode, self.time_scale, self.quad, self.save_path)
