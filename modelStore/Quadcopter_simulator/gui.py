import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as Axes3D
import sys


class GUI:
    def __init__(self, gui_mode, quads, goals, motor_modes):
        self.gui_mode = gui_mode
        self.quads = quads
        self.fig = plt.figure()
        self.fig.set_size_inches(9, 7)
        self.ax = Axes3D.Axes3D(self.fig)
        self.goals = np.asarray(goals)
        self.ax.set_xlim3d([np.min(self.goals[:, 0]-2), np.max(self.goals[:, 0]+2)])
        self.ax.set_xlabel('X')
        self.ax.set_ylim3d([np.min(self.goals[:, 1]-2), np.max(self.goals[:, ]+2)])
        self.ax.set_ylabel('Y')
        self.ax.set_zlim3d([0, np.max(self.goals[:, 2]+2)])
        self.ax.set_zlabel('Z')
        self.ax.set_title('Quadcopter Simulation')
        self.init_plot()
        self.goal_plot(goals)
        self.fig.canvas.mpl_connect('key_press_event', self.keypress_routine)

        # Thrust monitoring
        self.motor_modes = motor_modes
        self.c_bank = ['blue', 'blue', 'blue', 'blue']
        for mid, m in enumerate(self.motor_modes):
            self.c_bank[mid] = 'blue' if m == 'healthy' else 'red'
        if self.gui_mode is 2:
            self.thrust_fig, self.thrust_axs = plt.subplots(ncols=1, nrows=2)
            self.thrust_ax = self.thrust_axs[0]
            self.thrust_mids = [1, 2, 3, 4]
            self.thrust_values = [0, 0, 0, 0]
            self.thrust_ax.set_ylim(0, 13)
            self.thrust_ypos = np.arange(len(self.thrust_mids))
            self.thrust_ax.set_xlabel('Thrust')
            self.thrust_ax.bar(self.thrust_mids, self.thrust_values)

            self.thrust_rpm_ax = self.thrust_axs[1]
            self.rpm_values = [0, 0, 0, 0]
            self.thrust_rpm_ax.set_ylim(0, 30000)
            self.thrust_rpm_ax.set_xlabel('Requested RPMs')
            self.thrust_ax.bar(self.thrust_mids, self.rpm_values)

    def rotation_matrix(self, angles):
        ct = math.cos(angles[0])
        cp = math.cos(angles[1])
        cg = math.cos(angles[2])
        st = math.sin(angles[0])
        sp = math.sin(angles[1])
        sg = math.sin(angles[2])
        R_x = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
        R_y = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
        R_z = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
        R = np.dot(R_z, np.dot(R_y, R_x))
        return R

    def init_plot(self):
        for key in self.quads:
            self.quads[key]['l1'], = self.ax.plot([], [], [], color='blue', linewidth=2, antialiased=False)
            self.quads[key]['l2'], = self.ax.plot([], [], [], color='red', linewidth=2, antialiased=False)
            self.quads[key]['hub'], = self.ax.plot([], [], [], marker='o', color='green', markersize=6,
                                                   antialiased=False)

    def thrust_plot(self, thrust_values_in, rpm_values_in):
        self.thrust_ax.clear()
        self.thrust_mids = [1, 2, 3, 4]
        self.thrust_ax.set_ylim(0, 13)
        self.thrust_ax.set_xlabel('Thrust')
        self.thrust_ax.bar(self.thrust_mids, thrust_values_in, color=self.c_bank)

        self.thrust_rpm_ax.clear()
        self.thrust_rpm_ax.set_ylim(0, 30000)
        self.thrust_rpm_ax.set_xlabel('Requested RPMs')
        self.thrust_rpm_ax.bar(self.thrust_mids, rpm_values_in, color=self.c_bank)

    def goal_plot(self, goals):
        for goal in goals:
            self.ax.plot([goal[0]], [goal[1]], [goal[2]], marker='o', color='black', markersize=3, antialiased=False)

    def goal_plot_activated(self, goal):
        self.ax.plot([goal[0]], [goal[1]], [goal[2]], marker='o', color='green', markersize=5, antialiased=False)

    def update(self):
        for key in self.quads:
            R = self.rotation_matrix(self.quads[key]['orientation'])
            L = self.quads[key]['L']
            points = np.array([[-L, 0, 0], [L, 0, 0], [0, -L, 0], [0, L, 0], [0, 0, 0], [0, 0, 0]]).T
            points = np.dot(R, points)
            points[0, :] += self.quads[key]['position'][0]
            points[1, :] += self.quads[key]['position'][1]
            points[2, :] += self.quads[key]['position'][2]
            self.quads[key]['l1'].set_data(points[0, 0:2], points[1, 0:2])
            self.quads[key]['l1'].set_3d_properties(points[2, 0:2])
            self.quads[key]['l2'].set_data(points[0, 2:4], points[1, 2:4])
            self.quads[key]['l2'].set_3d_properties(points[2, 2:4])
            self.quads[key]['hub'].set_data(points[0, 5], points[1, 5])
            self.quads[key]['hub'].set_3d_properties(points[2, 5])

            if self.gui_mode is 2:
                # Update thrust graph
                self.thrust_values[0] = self.quads[key]['m1'].thrust
                self.thrust_values[1] = self.quads[key]['m2'].thrust
                self.thrust_values[2] = self.quads[key]['m3'].thrust
                self.thrust_values[3] = self.quads[key]['m4'].thrust
                # rpm values
                self.rpm_values[0] = self.quads[key]['m1'].speed
                self.rpm_values[1] = self.quads[key]['m2'].speed
                self.rpm_values[2] = self.quads[key]['m3'].speed
                self.rpm_values[3] = self.quads[key]['m4'].speed
                self.thrust_plot(self.thrust_values, self.rpm_values)
        plt.pause(0.000000000000001)

    def stop_gui(self):
        plt.close('all')

    def keypress_routine(self, event):
        sys.stdout.flush()
        if event.key == 'x':
            y = list(self.ax.get_ylim3d())
            y[0] += 0.2
            y[1] += 0.2
            self.ax.set_ylim3d(y)
        elif event.key == 'w':
            y = list(self.ax.get_ylim3d())
            y[0] -= 0.2
            y[1] -= 0.2
            self.ax.set_ylim3d(y)
        elif event.key == 'd':
            x = list(self.ax.get_xlim3d())
            x[0] += 0.2
            x[1] += 0.2
            self.ax.set_xlim3d(x)
        elif event.key == 'a':
            x = list(self.ax.get_xlim3d())
            x[0] -= 0.2
            x[1] -= 0.2
            self.ax.set_xlim3d(x)
