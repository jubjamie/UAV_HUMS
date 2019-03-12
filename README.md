# UAV_HUMS
Final Year Project Repo starting the process for machine learnt based HUMS for UAVs. This repo aims to have a curdly implemented neural network monitoring controller error correction to detirmine the health of the motor/rotor sets onboard.

## Required Packages/Dependancies
-  Python 3.6
-  Tensorflow >= 1.13 (Machine Learning)
-  Scipy >= 1.2.0 (Various Mmthematical operations)
-  Numpy >= 1.16.1 (Various mathematical operations)
-  Pandas >= 0.24.1 (Flight data processing)
-  Matplotlib >= 3.0.2 (Graph plotting)
-  h5py >= 2.9.0 (ML model save/restore)

### Original Material Notice
The underlying quadcopter model is an adapted version of [Abhijit Majumdar's Quadcopter Simulator](https://github.com/abhijitmajumdar/Quadcopter_simulator) used under the project's MIT Open Source Licence.

## Getting Started
The simulation environment is accessed by importing the sim file and creating a new simulation object. Note that scipy restrictions may mean only one simulation object may be created per session.

```python
import sim

newSim = sim.Sim() # Create new sim object
newSim.set_params(goals=[(5, -5, 3), (-4, 4, 6)], goal_time=8)  # Set goals as x,y,z coords and how long between switch goals.
newSim.set_failure_mode(setting='random')  # Set failure mode settings (See below)
newSim.see_gui = False  # Choose whether to display the 3D plot (slows performance) (Optional)
newSim.see_motor_gui = False  # Choose whether to accompany the 3D plot with motor performance graphs
newSim.time_scale = 0  # Set approximate timescale request (0=as fast as possibl,e 1=attempt real time. And value 0<=t<=1 accepted)
newSim.ask_save_destination()  # Open the pop up to set flight data to custom folder and not default. 
newSim.run_sim()  # Start the simulation.
```
The above example will run the simulation in full-speed-headless mode, i.e. as fast as it can without any gui elements. It will save the flight data to a destination of your choosing.

## Data Analysis
This project comes with a flight data analysis tool, a bit like reading an aircraft black box, that has graphs of the controller and quadcopter positional data. It can plot the flight path in 3D, show physical data compared to controller requested values etc.


<p align="center">
<img src="docs/data_analysis_1.jpg?raw=true" width="50%"/>
</p>

