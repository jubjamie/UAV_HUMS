from analyse import getdatafile as gdf
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
    path_data = flight_df[['x', 'y', 'z']]
    path_data_n = path_data.to_numpy()
    print(path_data_n)
    return path_data_n


def plotfp():
    path_data_n = getfp()
    fig = plt.figure()
    ax = Axes3D.Axes3D(fig)
    ax.plot(path_data_n[:, 0], path_data_n[:, 1], path_data_n[:, 2], label='Flight Path')
    ax.legend()
    plt.show()


def getangles():
    angle_data = flight_df[['theta', 'phi', 'gamma']]
    angle_data_n = angle_data.to_numpy()
    print(angle_data_n)
    return angle_data_n


def plotangles():
    angle_data_n = getangles()

    angleplot_fig, angleplot_axs = plt.subplots(3, sharex='all', sharey='all')
    angleplot_fig.suptitle('Angle Scope')

    #  Calculate time axes
    time_data = np.arange(0, step=0.005*10, stop=0.005*10*(angle_data_n[:, 0].shape[0]))
    angleplot_axs[0].plot(time_data, angle_data_n[:, 0])
    angleplot_axs[0].set_title('Theta - Roll')
    angleplot_axs[1].plot(time_data, angle_data_n[:, 1])
    angleplot_axs[1].set_title('Phi - Pitch')
    angleplot_axs[2].plot(time_data, angle_data_n[:, 2])
    angleplot_axs[2].set_title('Gamma - Yaw')

    plt.show()

def enda():
    print('Analysis Complete. Closing')
    sys.exit()


""" Main stuff """
b_exit = Button(root, text='Exit', command=enda)
b_fp = Button(root, text='Plot Flight Path', command=plotfp)
b_an = Button(root, text='Plot Angle Traces', command=plotangles)
b_fp.pack()
b_an.pack()
b_exit.pack()

mainloop()
