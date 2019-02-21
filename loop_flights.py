import sim
import time
import simutilities

# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=10)
newSim.ask_save_destination()
for i in range(300):
    GOALS = simutilities.randomgoals(1)
    newSim.reset_goals_to(GOALS)
    newSim.set_failure_mode(setting='random')
    newSim.see_gui = False
    newSim.time_scale = 0
    newSim.run_sim()
    time.sleep(1)
