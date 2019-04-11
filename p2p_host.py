import sim
import simutilities

# Set goals/yaws to go to
# GOALS = simutilities.randomgoals(3)
GOALS = [(5, -5, 3), (-4, 4, 6)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS, goal_time=15)
newSim.set_failure_mode(setting='defined', mode=['mf2', 'healthy', 'healthy', 'healthy'])
newSim.see_gui = False
newSim.see_motor_gui = False
newSim.time_scale = 0.5
newSim.use_lstm = False
newSim.ask_save_destination()
newSim.run_sim()
