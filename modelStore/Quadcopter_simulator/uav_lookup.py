import numpy as np
import motordata

modelist=['healthy', 'mf1']

# Lookup system for failed components


def lookup_rpm(rpm, mid, mode='healthy'):
    """
    Chooses a motor rotor profile depending on the motor id and/or base mode. Interps the values from emp data
    :param rpm: motor speed request from controller in rpm
    :param mode: The base motor mode
    :param mid: The motor id for choosing correct profile at later stage
    :return: return thrust in N
    """
    mode = parsemode(mode)
    newthrust_g = np.interp(rpm, motordata.alldata[mode][:, 0], motordata.alldata[mode][:, 1])
    newthrust_n = newthrust_g * 9.81 / 1000
    return newthrust_n


def parsemode(mode):
    """
    Parse a motor rotor mode identifier for call back from data
    :param mode: string or int that complies with modelist
    :return: Return the mode needed by motordata
    """
    if isinstance(mode, int) and mode <= len(modelist):
        return modelist[mode]
    elif mode in modelist:
        return mode
    else:
        raise ValueError('Mode not recognised')
