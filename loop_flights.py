import sim
import time
import simutilities

# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=6)
newSim.ask_save_destination()
for k in range(0, 4):
    h_string = ['healthy', 'healthy', 'healthy', 'healthy']
    h_string[k] = 'healthy'
    for i in range(100):
        print("Starting Simulation " + str(i+1))
        GOALS = simutilities.randomgoals(3)
        newSim.reset_goals_to(GOALS)
        newSim.set_failure_mode(setting='defined', mode=h_string)
        newSim.see_gui = False
        newSim.time_scale = 0
        newSim.run_sim()
        time.sleep(0.3)
