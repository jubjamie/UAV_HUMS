import sim

# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS)
newSim.set_failure_mode(setting='random')
newSim.see_gui = False
newSim.time_scale = 0
newSim.ask_save_destination()
newSim.run_sim()
