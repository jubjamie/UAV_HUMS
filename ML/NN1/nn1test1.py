import tensorflow as tf
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split


def get_motor_status(fdata):
    motor_modes = fdata[['m1_mode', 'm2_mode', 'm3_mode', 'm4_mode']].iloc[0]
    motor_extract = [motor_modes['m1_mode'], motor_modes['m2_mode'], motor_modes['m3_mode'],
                     motor_modes['m4_mode']]
    if all(i == 'healthy' for i in motor_extract):
        motor_status = 0
    else:
        motor_status = 1
    return motor_status


data = []
labels = np.array([])

mydir = "../../databin/test2/"

for file in os.listdir(mydir):
    if file.endswith(".csv"):
        filepath = os.path.join(mydir, file)
        flight_df = pd.read_csv(filepath, header=0, index_col=None)
        labels = np.append(labels, get_motor_status(flight_df))
        flight_df = flight_df[['theta_error', 'phi_error', 'theta_error_dot', 'phi_error_dot']]
        flight_df_n = flight_df.to_numpy()
        data.append([flight_df_n])

data = np.asarray(data)
print(labels)

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25)

