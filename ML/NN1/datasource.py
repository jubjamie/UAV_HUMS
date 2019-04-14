import pandas as pd
import os
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from modelStore.Quadcopter_simulator import motordata

pollingcycles = 30  # How many times to sample from a flight data file
timepointwidth = 10  # How many rows are in each sample.


def get_motor_status(fdata, classtype='binary', labelas='int'):
    """
    Generates labelling data from a segment of flight data.
    :param fdata: Flight data segment
    :param classtype: Binary or multiclass.
    :param labelas: Whether to label as ints or as label string
    :return: Label
    """

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


def get_data(newdata=False, classtype='binary', labelas=None, return_class_ref=True):
    """
    Gets data from a list of directories mydir below and pre-processes.
    :param newdata: Whether to go through directories and re-sample flight data or load in existing sampled data.
    :param classtype: Whether this will be used for "binary" or "multiclass" classification.
    :param labelas: How to label the labels i.e. int or label string.
    :param return_class_ref: Whether to return a list of classes for the label encoder.
    :return: Data split into train and test with optional class reference from label encoder.
    """
    # Infer suitable lebl modes from classtype
    if labelas is None:
        if classtype == 'multiclass':
            labelas = 'string'
        else:
            labelas = 'int'
    # Directories with flight data. Changes as required.
    mydir = ['../../databin/set2healthy/', '../../databin/set2mf2/', '../../databin/set2rsf1c/',
             '../../databin/set2rsf4/']
    if newdata:
        print('Fetching New Data...\nSearching Folders:')
        data = []
        labels = np.array([])

        # Loop through all csv files and collect the feature columns required. Append to a master array.
        for dirx in mydir:
            print(dirx)
            for file in os.listdir(dirx):
                if file.endswith(".csv"):
                    filepath = os.path.join(dirx, file)
                    flight_df = pd.read_csv(filepath, header=0, index_col=None)
                    poll_label = get_motor_status(flight_df, classtype, labelas)
                    flight_df = flight_df[['theta_error', 'phi_error', 'theta_error_dot', 'phi_error_dot', 'theta_dot',
                                           'phi_dot']]
                    flight_df_n = flight_df.to_numpy()
                    timepoints = flight_df_n.shape[0]
                    for j in range(pollingcycles):
                        pollpoint = random.randint(0, timepoints-timepointwidth-1)
                        flight_df_n_poll = flight_df_n[pollpoint:pollpoint+timepointwidth, :].T
                        data.append(flight_df_n_poll)
                        labels = np.append(labels, poll_label)

        # Format conversions for next steps
        data = np.asarray(data)
        if labelas == 'int':
            labels = labels.astype(int)
        else:
            labels = labels.astype(str)
        # Save new data as numpy object
        np.save(mydir[0] + '_' + classtype + '_data.npy', data)
        np.save(mydir[0] + '_' + classtype + '_labels.npy', labels)
    else:
        # Load in numpy data from file
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
    # Split data into test and train
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25)

    if return_class_ref:
        return X_train, y_train, X_test, y_test, classref
    else:
        return X_train, y_train, X_test, y_test


def lstm_transpose(xt1, yt1, xt2, yt2):
    """
    Transposes the data into the format for LSTM training
    :param xt1: x train data - Auto feeds if wrapping get_data()
    :param yt1: y train data - Auto feeds if wrapping get_data()
    :param xt2: x test data - Auto feeds if wrapping get_data()
    :param yt2: y test data - Auto feeds if wrapping get_data()
    :return:
    """
    xt1 = np.transpose(xt1, (0, 2, 1))
    xt2 = np.transpose(xt2, (0, 2, 1))
    return xt1, yt1, xt2, yt2
