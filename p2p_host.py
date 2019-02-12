import sim

'''
# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 4), (-1.5, 1.5, 1)]
YAWS = [0, 3.14, -1.54, 1.54]
# Define the quadcopters
QUADCOPTER = {
    'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5], 'weight': 1.2}}
# Controller parameters
CONTROLLER_PARAMETERS = {'Motor_limits': [7000, 27000],
                         'Tilt_limits': [-10, 10],
                         'Yaw_Control_Limits': [-900, 900],
                         'Z_XY_offset': 500,
                         'Linear_PID': {'P': [300, 300, 7000], 'I': [0.04, 0.04, 4.5], 'D': [450, 450, 5000]},
                         'Linear_To_Angular_Scaler': [1, 1, 0],
                         'Yaw_Rate_Scaler': 0.18,
                         'Angular_PID': {'P': [22000, 22000, 1500], 'I': [0, 0, 1.2], 'D': [12000, 12000, 0]},
                         }

quad_sim.Single_Point2Point(GOALS, YAWS, QUADCOPTER, CONTROLLER_PARAMETERS)
'''

newSim = sim.Sim()
newSim.run_sim()