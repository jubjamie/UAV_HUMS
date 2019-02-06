import numpy as np
import motordata

modelist=['healthy', 'mf1']

# Lookup system for failed components


def lookup_rpm(rpm, mode='healthy'):
    mode=parsemode(mode);
    newthrust_g = np.interp(rpm, motordata.alldata[mode][:, 0], motordata.alldata[mode][:, 1])
    newthrust_n = newthrust_g * 9.81 / 1000
    return newthrust_n


def parsemode(mode):
    if isinstance(mode, int) and mode <= len(modelist):
        return modelist[mode]
    elif mode in modelist:
        return mode
    else:
        raise ValueError('Mode not recognised')
