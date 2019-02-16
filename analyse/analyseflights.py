import pandas as pd
import mpl_toolkits.mplot3d.axes3d as Axes3D
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *
import sys

root = Tk()


def pickFile():
    root.filename = filedialog.askopenfilename(initialdir="databin/", title="Select file",
                                               filetypes=(("csv Flight Data", "*.csv"), ("all files", "*.*")))
    return root.filename


flight_df = pd.read_csv(pickFile(), header=0, index_col=None)


def getfp():
    path_data = flight_df[['x', 'y', 'z', 'dest_x', 'dest_y', 'dest_z']]
    fp_goals = flight_df[['dest_x', 'dest_y', 'dest_z']]
    fp_goals = fp_goals.groupby(['dest_x', 'dest_y', 'dest_z']).size().reset_index().rename(columns={0: 'count'})
    print('Goals')
    print(fp_goals)
    path_data_n = path_data.to_numpy()
    fp_goals_n = fp_goals.to_numpy()
    #  print(path_data_n)
    return {'pathdata': path_data_n, 'goaldata': fp_goals_n}


def plotfp():
    fpdata = getfp()
    path_data_n = fpdata['pathdata']
    goal_data_n = fpdata['goaldata']
    fig = plt.figure()
    ax = Axes3D.Axes3D(fig)
    ax.plot(path_data_n[:, 0], path_data_n[:, 1], path_data_n[:, 2], label='Flight Path')
    for i in range(goal_data_n.shape[0]):
        print(goal_data_n[i, 0])
        ax.plot([goal_data_n[i, 0]], [goal_data_n[i, 1]], [goal_data_n[i, 2]], marker='o', color='black', markersize=3)
    ax.legend()
    plt.show()


def plotfptrace():
    fpdata = getfp()
    path_data_n = fpdata['pathdata']

    fpplot_fig, fpplot_axs = plt.subplots(3, sharex='all')
    fpplot_fig.suptitle('Location Scope')

    #  Calculate time axes
    time_data = flight_df[['sim_clock']].to_numpy()[:, 0]
    fpplot_axs[0].plot(time_data, path_data_n[:, 0])
    fpplot_axs[0].plot(time_data, path_data_n[:, 3], 'r--')
    fpplot_axs[0].set_title('x')
    fpplot_axs[1].plot(time_data, path_data_n[:, 1])
    fpplot_axs[1].plot(time_data, path_data_n[:, 4], 'r--')
    fpplot_axs[1].set_title('y')
    fpplot_axs[2].plot(time_data, path_data_n[:, 2])
    fpplot_axs[2].plot(time_data, path_data_n[:, 5], 'r--')
    fpplot_axs[2].set_title('z - Alt')

    plt.show()


def getangles():
    angle_data = flight_df[['theta', 'phi', 'gamma', 'dest_theta', 'dest_phi', 'dest_gamma']]
    angle_data_n = angle_data.to_numpy()
    return angle_data_n


def plotangles():
    angle_data_n = getangles()

    angleplot_fig, angleplot_axs = plt.subplots(3, sharex='all')
    angleplot_fig.suptitle('Angle Scope')

    #  Calculate time axes
    time_data = flight_df[['sim_clock']].to_numpy()[:, 0]
    angleplot_axs[0].plot(time_data, angle_data_n[:, 0])
    angleplot_axs[0].plot(time_data, angle_data_n[:, 3], 'r--')
    angleplot_axs[0].set_title('Theta - Roll')
    angleplot_axs[1].plot(time_data, angle_data_n[:, 1])
    angleplot_axs[1].plot(time_data, angle_data_n[:, 4], 'r--')
    angleplot_axs[1].set_title('Phi - Pitch')
    angleplot_axs[2].plot(time_data, angle_data_n[:, 2])
    angleplot_axs[2].plot(time_data, angle_data_n[:, 5], 'r--')
    angleplot_axs[2].set_title('Gamma - Yaw')

    plt.show()


def enda():
    print('Analysis Complete. Closing')
    sys.exit()


""" Main stuff """
b_exit = Button(root, text='Exit', command=enda)
b_fp = Button(root, text='Plot Flight Path', command=plotfp)
b_fpt = Button(root, text='Plot Flight Path Traces', command=plotfptrace)
b_an = Button(root, text='Plot Angle Traces', command=plotangles)
b_fp.pack()
b_fpt.pack()
b_an.pack()
b_exit.pack()

mainloop()
