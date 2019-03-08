import tensorflow as tf
import pandas as pd
import os
import numpy as np
import random
from sklearn.model_selection import train_test_split

pollingcycles = 5
timepointwidth = 100

def get_motor_status(fdata):
    motor_modes = fdata[['m1_mode', 'm2_mode', 'm3_mode', 'm4_mode']].iloc[0]
    motor_extract = [motor_modes['m1_mode'], motor_modes['m2_mode'], motor_modes['m3_mode'],
                     motor_modes['m4_mode']]
    if all(i == 'healthy' for i in motor_extract):
        motor_status = 0
    else:
        motor_status = 1
    return motor_status


def get_data(asdict=False):
    print('Fetching Data...')
    data = []
    labels = np.array([])

    mydir = "../../databin/set1ThursEve0307/"

    for file in os.listdir(mydir):
        if file.endswith(".csv"):
            filepath = os.path.join(mydir, file)
            flight_df = pd.read_csv(filepath, header=0, index_col=None)
            poll_label = get_motor_status(flight_df)
            flight_df = flight_df[['theta_error', 'phi_error', 'theta_error_dot', 'phi_error_dot']]
            flight_df_n = flight_df.to_numpy()
            timepoints = flight_df_n.shape[0]
            for j in range(pollingcycles):
                pollpoint = random.randint(0, timepoints-timepointwidth-1)
                flight_df_n_poll = flight_df_n[pollpoint:pollpoint+timepointwidth, :].T
                data.append(flight_df_n_poll)
                labels = np.append(labels, poll_label)

    data = np.asarray(data)
    labels = labels.astype(int)
    print(labels)
    print(type(labels))
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25)
    if asdict is True:
        X_train = {'theta_error': X_train[:, 0, :],
                   'phi_error': X_train[:, 1, :],
                   'theta_error_dot': X_train[:, 2, :],
                   'phi_error_dot': X_train[:, 3, :]}
        X_test = {'theta_error': X_test[:, 0, :],
                   'phi_error': X_test[:, 1, :],
                   'theta_error_dot': X_test[:, 2, :],
                   'phi_error_dot': X_test[:, 3, :]}
    return X_train, y_train, X_test, y_test


def train_input_fn(features, labels, batch_size=100):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))

    # Shuffle, repeat, and batch the examples.
    # dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""

    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset
