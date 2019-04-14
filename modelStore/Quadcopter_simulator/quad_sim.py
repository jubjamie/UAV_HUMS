from modelStore.Quadcopter_simulator import quadcopter, gui, controller, healthmonitor
import signal
import sys
import argparse
import time

# Constants
#  TIME_SCALING = 1.0 # Any positive number(Smaller is faster). 1.0->Real Time, 0.0->Run as fast as possible
QUAD_DYNAMICS_UPDATE = 0.002  # seconds
CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
run = True


def Single_Point2Point(goals, goal_length, yaws, quadcopter, controller_params, motor_modes, gui_mode, time_scale,
                       quad, save_path, use_lstm, monitorscope):
    """
    Main simulation thread manageer
    :param goals: Goals to loop through
    :param goal_length: Approx how long to spend before changing to next goal
    :param yaws: Yaw targets
    :param quadcopter: Quadcopter parameters
    :param controller_params: Controller parameters to pass to controller thread
    :param motor_modes: Modes for each motor
    :param gui_mode: Whether to show certain GUI elements
    :param time_scale: Time scale to run the simulation error at (0-1)
    :param quad: Quadcopter physics model to run
    :param save_path: Where to save flight data to
    :param use_lstm: Whether the healthmonitor should use LSTMs
    :param monitorscope: Where to display health monitor classification scope (Broken)
    :return: Simulation run
    """
    # Catch Ctrl+C to stop threads
    gui_object = []
    signal.signal(signal.SIGINT, signal_handler)
    # Make objects for quadcopter, gui and controller
    # Load GUI worker if needed
    if gui_mode is not 0:
        gui_object = gui.GUI(gui_mode=gui_mode, quads=quadcopter, goals=goals, motor_modes=motor_modes)
    # Init controller object
    ctrl = controller.Controller_PID_Point2Point(quad.get_state, quad.get_time, quad.set_motor_speeds,
                                                 params=controller_params, quad_identifier='q1',
                                                 motor_modes=motor_modes, save_path=save_path)
    # Init healthmonitor object
    hmtr = healthmonitor.HealthMonitor(controller=ctrl, datafeed=ctrl.get_monitorbuffer, use_lstm=use_lstm, displaybool=monitorscope)
    # Start the healthmonitor thread to load model into memory
    hmtr.start_thread()
    # Wait for healthmonitor to report ready to continue simulation.
    while hmtr.ready is False:
        time.sleep(0.1)
    # Start the quadcopter physics model and the controleer threads
    quad.start_thread(dt=QUAD_DYNAMICS_UPDATE, time_scaling=time_scale)
    ctrl.start_thread(update_rate=CONTROLLER_DYNAMICS_UPDATE, time_scaling=time_scale, goal_length=goal_length)
    # Update the GUI while switching between destination positions
    print('Starting goals')
    inittime = quad.get_time()
    # Loop through goals and update GUI and other elements as required.
    for goal, y in zip(goals, yaws):
        print(['Goal: ' + str(goal)])
        if gui_mode is not 0:
            gui_object.goal_plot_activated(goal)
        ctrl.update_target(goal)
        ctrl.update_yaw_target(y)
        ctrl.ready_for_goal = False
        while ctrl.ready_for_goal is False:
            time.sleep(CONTROLLER_DYNAMICS_UPDATE * 0.95)
            # print(i)
            # print((quad.get_time() - inittime).total_seconds())
            if gui_mode is not 0:
                gui_object.quads['q1']['position'] = quad.get_position('q1')
                gui_object.quads['q1']['orientation'] = quad.get_orientation('q1')
                gui_object.update()
            if monitorscope is True:
                hmtr.scope_plotter()
    # Once complete flush flight data buffer to file.
    ctrl.flush_buffer()
    hmtr.stop_thread()
    print('Goals complete.\nStopping threads')
    if gui_mode is not 0:
        gui_object.stop_gui()
    quad.stop_thread()
    ctrl.stop_thread()


def signal_handler(signal, frame):
    global run
    run = False
    print('Stopping')
    sys.exit(0)
