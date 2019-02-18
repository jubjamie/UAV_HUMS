import sim
import time

# Set goals/yaws to go to
GOALS = [(0, 0, 3), (2, -2, 3), (-1.5, 1.5, 3)]

newSim = sim.Sim()
newSim.set_params(goals=GOALS)
for i in range(3):
    newSim.set_failure_mode(setting='random')
    newSim.see_gui = True
    newSim.time_scale = 0
    newSim.run_sim()
    time.sleep(1)
