import sim
import simutilities

# Set goals/yaws to go to
#GOALS = simutilities.randomgoals(1)
GOALS = [(0, 0, 3), (2, -2, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=15)
newSim.set_failure_mode(setting='defined')
newSim.see_gui = True
newSim.see_motor_gui = True
newSim.time_scale = 1
newSim.ask_save_destination()
newSim.run_sim()
