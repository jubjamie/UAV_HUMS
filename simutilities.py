import random

''' Pick x y and z values in ranges specified
    x and y use much wider rangs
    z uses smaller range with divisor of 10 to give altitude of 0.1m resolution
    '''


def randomgoals(count):
    goals = []
    for i in range(count):
        x = random.randrange(-10, 10)
        y = random.randrange(-10, 10)
        z = random.randrange(20, 60) / 10
        goals.append([x, y, z])
    return goals
