#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - store the current orientation of Gretchen
# - look somewhere else, then return Gretchen's
#   head to the original position
#

# Import required modules
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
import time


def main():
    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Initalize & start robot
    robot = Robot()
    robot.start()

    # TODO
    # Obtain the current orientation of the robot using
    # getPosition(). getPosition() returns an array with
    # two elements: [0] refers to the pan, [1] to the tilt angle
    curr_pos  = robot.
    curr_pan  = curr_pos[
    curr_tilt =


    # TODO
    # Look somewhere else other than the current position
    # using any movement function you know, then wait a bit

    time.sleep(2)


    # TODO
    # Return back to the position stored in 'curr_pos'. 
    # Which function is most appropriate for that?

    time.sleep(2)


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
