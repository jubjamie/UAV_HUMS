import sim
import simutilities

# Set goals/yaws to go to
GOALS = simutilities.randomgoals(3)
# GOALS = [(5, -5, 3), (-4, 4, 6)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=8)
newSim.set_failure_mode(setting='defined')
newSim.see_gui = False
newSim.see_motor_gui = False
newSim.time_scale = 0
newSim.ask_save_destination()
newSim.run_sim()
