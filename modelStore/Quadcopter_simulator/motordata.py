import numpy as np
import matplotlib.pyplot as plt
# Data:
# As rpm/thrust pair (grams)
healthy = np.array(
    [[7520, 90], [11470, 204], [13650, 306], [15310, 388], [16680, 457], [17830, 523], [18950, 591], [20110, 664],
     [20830, 722],
     [21720, 774], [23380, 836], [24060, 887], [24550, 942], [25120, 995], [25350, 1045], [25630, 1098], [25810, 1150],
     [26050, 1208], [26170, 1236]])

motorFailure1 = np.array(
    [[7520, 54],
     [11470, 122],
     [13650, 183],
     [15310, 232],
     [16680, 274],
     [17830, 313],
     [18950, 354],
     [20110, 398],
     [20830, 433],
     [21720, 464],
     [23380, 501],
     [24060, 532],
     [24550, 565],
     [25120, 597],
     [25350, 627],
     [25630, 658],
     [25810, 690],
     [26050, 724],
     [26170, 741]])

alldata = {'healthy':healthy, 'mf1': motorFailure1}


def plotprofile(mode):
    plt.figure()
    plt.plot(alldata[mode][:, 0], alldata[mode][:, 1])
    plt.xlabel('RPM')
    plt.ylabel('gram-force')
    plt.show()
