from modelStore.Quadcopter_simulator import quadcopter, gui, controller
import signal
import sys
import argparse
import time

# Constants
#  TIME_SCALING = 1.0 # Any positive number(Smaller is faster). 1.0->Real Time, 0.0->Run as fast as possible
QUAD_DYNAMICS_UPDATE = 0.002  # seconds
CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
run = True


def Single_Point2Point(GOALS, goal_length, YAWS, QUADCOPTER, CONTROLLER_PARAMETERS, motor_modes, gui_mode, time_scale, quad, save_path):
    # Catch Ctrl+C to stop threads
    gui_object = []
    signal.signal(signal.SIGINT, signal_handler)
    # Make objects for quadcopter, gui and controller
    # quad = quadcopter.Quadcopter(QUADCOPTER, motor_modes)
    if gui_mode is not 0:
        gui_object = gui.GUI(gui_mode=gui_mode, quads=QUADCOPTER, goals=GOALS, motor_modes=motor_modes)
    ctrl = controller.Controller_PID_Point2Point(quad.get_state, quad.get_time, quad.set_motor_speeds,
                                                 params=CONTROLLER_PARAMETERS, quad_identifier='q1', motor_modes=motor_modes, save_path=save_path)
    # Start the threads
    quad.start_thread(dt=QUAD_DYNAMICS_UPDATE, time_scaling=time_scale)
    ctrl.start_thread(update_rate=CONTROLLER_DYNAMICS_UPDATE, time_scaling=time_scale, goal_length=goal_length)
    # Update the GUI while switching between destination positions
    print('Starting goals')
    inittime = quad.get_time()
    for goal, y in zip(GOALS, YAWS):
        print(['Goal: ' + str(goal)])
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
    ctrl.flush_buffer()
    print('Goals complete.\nStopping threads')
    if gui_mode is not 0:
        gui_object.stop_gui()
    quad.stop_thread()
    ctrl.stop_thread()


def parse_args():
    parser = argparse.ArgumentParser(description="Quadcopter Simulator")
    parser.add_argument("--sim", help='single_p2p, multi_p2p or single_velocity', default='single_p2p')
    parser.add_argument("--time_scale", type=float, default=-1.0,
                        help='Time scaling factor. 0.0:fastest,1.0:realtime,>1:slow, ex: --time_scale 0.1')
    parser.add_argument("--quad_update_time", type=float, default=0.0,
                        help='delta time for quadcopter dynamics update(seconds), ex: --quad_update_time 0.002')
    parser.add_argument("--controller_update_time", type=float, default=0.0,
                        help='delta time for controller update(seconds), ex: --controller_update_time 0.005')
    return parser.parse_args()


def signal_handler(signal, frame):
    global run
    run = False
    print('Stopping')
    sys.exit(0)


if __name__ == "__main__":
    args = parse_args()
    """
    TIME_SCALING = args.time_scale if args.time_scale >= 0 else TIME_SCALING = 1.0
    QUAD_DYNAMICS_UPDATE = args.quad_update_time if args.quad_update_time > 0 else QUAD_DYNAMICS_UPDATE = 0.002
    CONTROLLER_DYNAMICS_UPDATE = args.controller_update_time if args.controller_update_time > 0 \
        else CONTROLLER_DYNAMICS_UPDATE = 0.005
    """
    if args.sim == 'single_p2p':
        #  Single_Point2Point()
        pass
