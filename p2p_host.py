import sim
import simutilities

# Set goals/yaws to go to
GOALS = simutilities.randomgoals(3)

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=10)
newSim.set_failure_mode(setting='random')
newSim.see_gui = True
newSim.time_scale = 0
newSim.ask_save_destination()
newSim.run_sim()
