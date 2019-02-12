import sim

# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS)
newSim.run_sim()
