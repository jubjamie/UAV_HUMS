import numpy as np
import math
import random
import time
import threading
import pandas as pd


class Controller_PID_Point2Point:
    def __init__(self, get_state, get_time, actuate_motors, params, quad_identifier, motor_modes, save_path):
        # Initialise
        self.quad_identifier = quad_identifier
        self.actuate_motors = actuate_motors
        self.motor_modes = motor_modes
        self.get_state = get_state
        self.get_time = get_time
        self.MOTOR_LIMITS = params['Motor_limits']
        self.TILT_LIMITS = [(params['Tilt_limits'][0] / 180.0) * 3.14, (params['Tilt_limits'][1] / 180.0) * 3.14]
        self.YAW_CONTROL_LIMITS = params['Yaw_Control_Limits']
        self.Z_LIMITS = [self.MOTOR_LIMITS[0] + params['Z_XY_offset'], self.MOTOR_LIMITS[1] - params['Z_XY_offset']]
        self.LINEAR_P = params['Linear_PID']['P']
        self.LINEAR_I = params['Linear_PID']['I']
        self.LINEAR_D = params['Linear_PID']['D']
        self.LINEAR_TO_ANGULAR_SCALER = params['Linear_To_Angular_Scaler']
        self.YAW_RATE_SCALER = params['Yaw_Rate_Scaler']
        self.ANGULAR_P = params['Angular_PID']['P']
        self.ANGULAR_I = params['Angular_PID']['I']
        self.ANGULAR_D = params['Angular_PID']['D']
        self.xi_term = 0
        self.yi_term = 0
        self.zi_term = 0
        self.thetai_term = 0
        self.phii_term = 0
        self.gammai_term = 0
        self.angle_error_dots = np.zeros(3)
        self.last_angle_errors = np.zeros(3)
        self.dt_step = 0.005
        self.thread_object = None
        self.target = [0, 0, 0]
        self.yaw_target = 0.0
        self.run = True
        self.time = 0

        #  Data Logging bits
        self.save_buffer = []
        self.buffer_counter = 0
        self.step_ignore_limit = 10
        self.step_ignore = self.step_ignore_limit
        self.buffer_size = 511
        self.header_tracker = False
        self.flush_override = False

        self.ts = time.gmtime()
        self.ts_mt = time.mktime(self.ts)
        self.init_timestamp = time.strftime("%Y_%m_%d--%H-%M-%S", self.ts)
        self.save_path = save_path + '/' + self.init_timestamp + '__' + str(threading.get_ident()) + '.csv'

        # ML buffer
        self.monitorbufferlength = 10
        self.monitorbuffer = np.zeros((self.monitorbufferlength, 6))

        # Sim time
        self.sim_clock = 0
        self.ready_for_goal = False

        print('Controller init')

    def wrap_angle(self, val):
        return (val + np.pi) % (2 * np.pi) - np.pi

    def update(self):
        [dest_x, dest_y, dest_z] = self.target
        [x, y, z, x_dot, y_dot, z_dot, theta, phi, gamma, theta_dot, phi_dot, gamma_dot] = self.get_state(
            self.quad_identifier)
        x_error = dest_x - x
        y_error = dest_y - y
        z_error = dest_z - z
        self.xi_term += self.LINEAR_I[0] * x_error
        self.yi_term += self.LINEAR_I[1] * y_error
        self.zi_term += self.LINEAR_I[2] * z_error
        dest_x_dot = self.LINEAR_P[0] * x_error + self.LINEAR_D[0] * (-x_dot) + self.xi_term
        dest_y_dot = self.LINEAR_P[1] * y_error + self.LINEAR_D[1] * (-y_dot) + self.yi_term
        dest_z_dot = self.LINEAR_P[2] * z_error + self.LINEAR_D[2] * (-z_dot) + self.zi_term
        throttle = np.clip(dest_z_dot, self.Z_LIMITS[0], self.Z_LIMITS[1])
        dest_theta = self.LINEAR_TO_ANGULAR_SCALER[0] * (dest_x_dot * math.sin(gamma) - dest_y_dot * math.cos(gamma))
        dest_phi = self.LINEAR_TO_ANGULAR_SCALER[1] * (dest_x_dot * math.cos(gamma) + dest_y_dot * math.sin(gamma))
        dest_gamma = self.yaw_target
        dest_theta, dest_phi = np.clip(dest_theta, self.TILT_LIMITS[0], self.TILT_LIMITS[1]), np.clip(dest_phi,
                                                                                                      self.TILT_LIMITS[
                                                                                                          0],
                                                                                                      self.TILT_LIMITS[
                                                                                                          1])
        theta_error = dest_theta - theta
        phi_error = dest_phi - phi
        gamma_dot_error = (self.YAW_RATE_SCALER * self.wrap_angle(dest_gamma - gamma)) - gamma_dot
        self.angle_error_dots[:] = [theta_error - self.last_angle_errors[0], phi_error - self.last_angle_errors[1],
                                    gamma_dot_error - self.last_angle_errors[2]]
        self.angle_error_dots = self.angle_error_dots/self.dt_step
        self.last_angle_errors[:] = [theta_error, phi_error, gamma_dot_error]
        self.thetai_term += self.ANGULAR_I[0] * theta_error
        self.phii_term += self.ANGULAR_I[1] * phi_error
        self.gammai_term += self.ANGULAR_I[2] * gamma_dot_error
        x_val = self.ANGULAR_P[0] * theta_error + self.ANGULAR_D[0] * (-theta_dot) + self.thetai_term
        y_val = self.ANGULAR_P[1] * phi_error + self.ANGULAR_D[1] * (-phi_dot) + self.phii_term
        z_val = self.ANGULAR_P[2] * gamma_dot_error + self.gammai_term
        z_val = np.clip(z_val, self.YAW_CONTROL_LIMITS[0], self.YAW_CONTROL_LIMITS[1])
        m1 = throttle + x_val + z_val
        m2 = throttle + y_val - z_val
        m3 = throttle - x_val + z_val
        m4 = throttle - y_val - z_val
        M = np.clip([m1, m2, m3, m4], self.MOTOR_LIMITS[0], self.MOTOR_LIMITS[1])

        # Collate Data for logging
        errors = np.array([x_error, y_error, z_error, theta_error, phi_error, gamma_dot_error])
        in_state = np.array([x, y, z, x_dot, y_dot, z_dot, theta, phi, gamma, theta_dot, phi_dot, gamma_dot])
        location_dests = np.array([dest_x, dest_y, dest_z])
        angle_dests = np.array([dest_theta, dest_phi, dest_gamma])
        requests = np.array([m1, m2, m3, m4])
        local_ts = time.mktime(time.gmtime())
        wall_clock = (local_ts - self.ts_mt)
        motor_status = np.asarray(self.motor_modes, dtype=object)
        save_data_cat = np.concatenate(
            (np.array([wall_clock, self.sim_clock]), location_dests, in_state, errors, self.angle_error_dots,
             angle_dests, requests, motor_status))
        names = ['wall_clock', 'sim_clock', 'dest_x', 'dest_y', 'dest_z', 'x', 'y', 'z', 'x_dot', 'y_dot', 'z_dot',
                 'theta', 'phi', 'gamma', 'theta_dot', 'phi_dot', 'gamma_dot',
                 'x_error', 'y_error', 'z_error', 'theta_error', 'phi_error', 'gamma_dot_error', 'theta_error_dot',
                 'phi_error_dot', 'gamma_dot_error_dot', 'dest_theta', 'dest_phi', 'dest_gamma', 'm1_r', 'm2_r', 'm3_r',
                 'm4_r', 'm1_mode', 'm2_mode', 'm3_mode', 'm4_mode']
        self.save_data(save_data_cat, names)
        self.update_monitorbuffer(np.array([theta_error, phi_error, self.angle_error_dots[0], self.angle_error_dots[1],
                                           theta_dot, phi_dot]))
        # Actuate the motors
        self.actuate_motors(self.quad_identifier, M)

    def update_monitorbuffer(self, data):
        """
        Updates the buffer for the healthmonitor to read from
        """
        data = np.reshape(data, (1, 6))
        self.monitorbuffer = np.vstack((self.monitorbuffer, data))
        self.monitorbuffer = np.delete(self.monitorbuffer, 0, 0)
        # print(self.monitorbuffer)

    def get_monitorbuffer(self):
        """
        Cross-thread hook for the monitor buffer
        :return: Monitor buffer and sim clock data
        """
        return self.monitorbuffer, self.sim_clock

    def save_data(self, data, col_names):
        """
        Saves flight data to a buffer and routinely flush to buffer
        :param data: Data to save
        :param col_names: Headers
        :return: None
        """
        if not self.flush_override:
            if self.step_ignore < self.step_ignore_limit:
                # Skip
                self.step_ignore += 1
            else:
                # Save to buffer
                self.step_ignore = 1
                if self.buffer_counter == 0:
                    # New buffer
                    self.save_buffer = pd.DataFrame([data], columns=col_names)
                    self.buffer_counter += 1
                    print('New buffer')
                elif self.buffer_counter < self.buffer_size:
                    #  Append to buffer
                    local_data_df = pd.DataFrame([data], columns=col_names)
                    self.save_buffer = self.save_buffer.append(local_data_df, ignore_index=True)
                    self.buffer_counter += 1
                    # print('Writing to buffer. Length: ' + str(len(self.save_buffer.index)))
                    #  print(self.save_buffer)
                elif self.buffer_counter >= self.buffer_size:
                    #  Append buffer to file
                    if self.header_tracker is False:
                        self.save_buffer.to_csv(self.save_path, index=False, header=True, mode='a')
                        self.header_tracker = True
                    else:
                        self.save_buffer.to_csv(self.save_path, index=False, header=False, mode='a')
                    self.buffer_counter = 0
                    self.save_buffer = pd.DataFrame([data], columns=col_names)
                    print('Writing to file @ sim-clock: ' + str(self.sim_clock))
                else:
                    print('Buffer counter error, skipping. Count @ ' + str(self.buffer_counter))
                    pass
        else:
            # print('Flush in progress. Saving override activated.')
            pass

    def flush_buffer(self):
        """
        Flushes the buffer at the end of a simulation
        :return: None
        """
        self.flush_override = True
        print('Flushing buffer to file')
        if self.header_tracker is False:
            self.save_buffer.to_csv(self.save_path, index=False, header=True, mode='a')
            self.header_tracker = True
        else:
            self.save_buffer.to_csv(self.save_path, index=False, header=False, mode='a')

    def update_target(self, target):
        self.target = target

    def update_yaw_target(self, target):
        self.yaw_target = self.wrap_angle(target)

    def thread_run(self, dt, time_scaling, goal_length):
        print('ctrl thread init')
        self.time = 0
        self.dt_step = dt
        update_rate = dt * time_scaling
        last_update = self.get_time()
        while self.run is True:
            time.sleep(0)
            self.time = self.get_time()
            # print('self time: ' + str(self.time) + ' Last update: ' + str(last_update))
            # print('Target rate:' + str(update_rate))
            if (self.time - last_update).total_seconds() > update_rate:
                # print('will update')
                self.update()
                last_update = self.time
                self.sim_clock += dt
                self.sim_clock = round(self.sim_clock, 5)
                # print(self.sim_clock)
                if self.sim_clock % goal_length == 0:
                    #  Flag new target
                    self.ready_for_goal = True
                    # print('Target flagging')
        print('ctrl thread finished')

    def start_thread(self, update_rate=0.005, time_scaling=1, goal_length=5):
        self.thread_object = threading.Thread(target=self.thread_run, args=(update_rate, time_scaling, goal_length))
        self.thread_object.start()

    def stop_thread(self):
        self.run = False
