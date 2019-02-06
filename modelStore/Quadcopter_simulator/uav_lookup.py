import numpy as np

# Lookup system for failed components
# Data:
# As rpm/thrust pair (grams)
healthy = np.array(
    [[7520, 90], [11470, 204], [13650, 306], [15310, 388], [16680, 457], [17830, 523], [18950, 591], [20110, 664],
     [20830, 722],
     [21720, 774], [23380, 836], [24060, 887], [24550, 942], [25120, 995], [25350, 1045], [25630, 1098], [25810, 1150],
     [26050, 1208], [26170, 1236]])


def lookup_rpm(rpm):
    newthrust_g = np.interp(rpm, healthy[:, 0], healthy[:, 1])
    newthrust_n = newthrust_g * 9.81 / 1000
    return newthrust_n
