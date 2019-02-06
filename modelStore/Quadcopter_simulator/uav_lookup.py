import numpy as np
import motordata

# Lookup system for failed components


def lookup_rpm(rpm):
    newthrust_g = np.interp(rpm, motordata.healthy[:, 0], motordata.healthy[:, 1])
    newthrust_n = newthrust_g * 9.81 / 1000
    return newthrust_n
