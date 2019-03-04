import numpy as np
import matplotlib.pyplot as plt
# Data:
# As rpm/thrust pair (grams)
healthy = np.array(
    [[7520, 90, 0],
    [11470, 204, 0],
    [13650, 306, 0],
    [15310, 388, 0],
    [16680, 457, 0],
    [17830, 523, 0],
    [18950, 591, 0],
    [20110, 664, 0],
    [20830, 722, 0],
    [21720, 774, 0],
    [23380, 836, 0],
    [24060, 887, 0],
    [24550, 942, 0],
    [25120, 995, 0],
    [25350, 1045, 0],
    [25630, 1098, 0],
    [25810, 1150, 0],
    [26050, 1208, 0],
    [26170, 1236, 0]])

motorFailure1 = np.array(
    [[7520, 54, 0],
     [11470, 122, 0],
     [13650, 183, 0],
     [15310, 232, 0],
     [16680, 274, 0],
     [17830, 313, 0],
     [18950, 354, 0],
     [20110, 398, 0],
     [20830, 433, 0],
     [21720, 464, 0],
     [23380, 501, 0],
     [24060, 532, 0],
     [24550, 565, 0],
     [25120, 597, 0],
     [25350, 627, 0],
     [25630, 658, 0],
     [25810, 690, 0],
     [26050, 724, 0],
     [26170, 741, 0]])

rsf1c = np.array(
    [[7646, 35.5, 32],
     [9698, 105, 45.9],
     [11312, 157.8, 80.1],
     [12144, 170.1, 110]])  # 1.5 tip. Clipped early as motor couldn't run past this speed.

rsf2 = np.array(
    [[7965, 32.2, 4],
     [10069, 113.5, 4.5],
     [11800, 186, 5.5],
     [12661, 173, 8],
     [13603, 219, 16.1],
     [14264, 233, 20.5],
     [14751, 254, 24.6],
     [15417, 268, 24.8],
     [27000, 500, 26]])  # Double small tip

rsf4 = np.array(
    [[9246, 33.5, 4],
     [11646, 61, 5.8],
     [13167, 93, 26.4],
     [14172, 139, 33.3],
     [14982, 160, 58.7],
     [15452, 174.6, 69.9],
     [16826, 211.5, 47],
     [16840, 221, 54.3],
     [24000, 526, 56],
     [27000, 738, 56]])  # Double 2.8

alldata = {'healthy': healthy, 'mf1': motorFailure1, 'rsf1c': rsf1c, 'rsf2': rsf2, 'rsf4': rsf4}


def plotprofile(mode):
    """
    Given mode key for all data, plot a graph showing rpm profile. Useful for debug or quick inspection
    :param mode: Mode key from alldata above
    :return: Graph
    """
    plt.figure()
    plt.plot(alldata[mode][:, 0], alldata[mode][:, 1])
    plt.xlabel('RPM')
    plt.ylabel('gram-force')
    plt.show()


def noise(mean, std):
    noise_y = np.random.normal(mean, std, 2000)
    noise_x = np.linspace(1, 2000, num=2000)
    plt.figure()
    plt.plot(noise_x, noise_y)
    plt.show()

#plotprofile('rsf4')

# noise(170,0)
