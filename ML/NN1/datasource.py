import tensorflow as tf
import pandas as pd
import os
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from modelStore.Quadcopter_simulator import motordata

pollingcycles = 30
timepointwidth = 10


def get_motor_status(fdata, classtype='binary', labelas='int'):

    motor_modes = fdata[['m1_mode', 'm2_mode', 'm3_mode', 'm4_mode']].iloc[0]
    motor_extract = [motor_modes['m1_mode'], motor_modes['m2_mode'], motor_modes['m3_mode'],
                     motor_modes['m4_mode']]
    if all(i == 'healthy' for i in motor_extract):
            motor_status = 'healthy' if labelas == 'string' else 0
    else:
        if classtype == 'binary':
            if labelas == 'string':
                motor_status = 'failure'
            else:
                motor_status = 1
        elif classtype == 'multiclass':
            motor_status = 'healthy' if labelas == 'string' else 0  # Give healthy unless accepted damage mode found
            for modes in motor_extract:
                if modes in [*motordata.alldata][1:]:
                    #  If mode is a mode in the accepted list that is not healthy
                    motor_status = modes if labelas == 'string' else [*motordata.alldata].index(modes)
                    break
        else:
            raise ValueError('Class type not recognised for labelling motor status ( get_motor_status() )')

    return motor_status


def get_data(asdict=False, newdata=False, classtype='binary', labelas=None, return_class_ref=True):
    if labelas is None:
        if classtype == 'multiclass':
            labelas = 'string'
        else:
            labelas = 'int'

    mydir = ['../../databin/set2healthy/', '../../databin/set2mf2/', '../../databin/set2rsf1c/',
             '../../databin/set2rsf4/']
    if newdata:
        print('Fetching New Data...\nSearching Folders:')
        data = []
        labels = np.array([])

        for dirx in mydir:
            print(dirx)
            for file in os.listdir(dirx):
                if file.endswith(".csv"):
                    filepath = os.path.join(dirx, file)
                    flight_df = pd.read_csv(filepath, header=0, index_col=None)
                    poll_label = get_motor_status(flight_df, classtype, labelas)
                    flight_df = flight_df[['theta_error', 'phi_error', 'theta_error_dot', 'phi_error_dot', 'theta_dot', 'phi_dot']]
                    flight_df_n = flight_df.to_numpy()
                    timepoints = flight_df_n.shape[0]
                    for j in range(pollingcycles):
                        pollpoint = random.randint(0, timepoints-timepointwidth-1)
                        flight_df_n_poll = flight_df_n[pollpoint:pollpoint+timepointwidth, :].T
                        data.append(flight_df_n_poll)
                        labels = np.append(labels, poll_label)

        data = np.asarray(data)
        if labelas == 'int':
            labels = labels.astype(int)
        else:
            labels = labels.astype(str)
        # Save new data
        np.save(mydir[0] + '_' + classtype + '_data.npy', data)
        np.save(mydir[0] + '_' + classtype + '_labels.npy', labels)
    else:
        print('Loading data from file...')
        data = np.load(mydir[0] + '_' + classtype + '_data.npy')
        labels = np.load(mydir[0] + '_' + classtype + '_labels.npy')

    if classtype == 'multiclass':
        # Encode labels
        le = LabelEncoder()
        le.fit(labels)
        classref = list(le.classes_)
        labels = le.transform(labels)
    else:
        classref = ['healthy', 'failure']

    print(labels)
    print(type(labels))
    print(data.shape)
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

    if return_class_ref:
        return X_train, y_train, X_test, y_test, classref
    else:
        return X_train, y_train, X_test, y_test


def lstm_transpose(xt1, yt1, xt2, yt2):
    xt1 = np.transpose(xt1, (0, 2, 1))
    xt2 = np.transpose(xt2, (0, 2, 1))
    return xt1, yt1, xt2, yt2


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
