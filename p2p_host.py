import sim
import simutilities

# Set goals/yaws to go to
GOALS = simutilities.randomgoals(1)
# GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=15)
newSim.set_failure_mode(setting='defined')
newSim.see_gui = False
newSim.see_motor_gui = False
newSim.time_scale = 0
newSim.ask_save_destination()
newSim.run_sim()
