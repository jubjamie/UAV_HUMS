import modelStore.Quadcopter_simulator.uav_lookup as uav_lookup
import modelStore.Quadcopter_simulator.quad_sim as quad_sim


class Sim:
    def __init__(self):
        self.GOALS = [(0, 0, 3), (2, -2, 4), (-1.5, 1.5, 1)]
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
                                      'Linear_PID': {'P': [300, 300, 7000], 'I': [0.04, 0.04, 4.5],
                                                     'D': [450, 450, 5000]},
                                      'Linear_To_Angular_Scaler': [1, 1, 0],
                                      'Yaw_Rate_Scaler': 0.18,
                                      'Angular_PID': {'P': [22000, 22000, 1500], 'I': [0, 0, 1.2],
                                                      'D': [12000, 12000, 0]},
                                      }
        self.motor_modes = [0, 0, 0, 0]

    def set_params(self, goals=None, yaws=None, quadcopter=None, ctlprms=None):
        if goals is not None:
            self.GOALS = goals
        if yaws is not None:
            self.YAWS = yaws
        if quadcopter is not None:
            self.QUADCOPTER = quadcopter
        if ctlprms is not None:
            self.CONTROLLER_PARAMETERS = ctlprms
        print('Basic Parameters Set')

    def set_failure_mode(self, setting, mode='healthy'):
        if setting == 'random':
            pass # Do random setting here
        elif setting == 'defined':
            if len(mode) == 1:
                if mode in uav_lookup.modelist:
                    self.motor_modes = [mode, mode, mode, mode]
                else:
                    raise ValueError('set_failure_mode: Mode not recognised')
            else:
                self.motor_modes = mode
        else:
            raise ValueError('set_failure_mode: Setting not recognised')
        print('Set motor modes to: ' + str(self.motor_modes))

    def run_sim(self):
        quad_sim.Single_Point2Point(self.GOALS, self.YAWS, self.QUADCOPTER, self.CONTROLLER_PARAMETERS)
