#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - have Gretchen look at two objects
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
    # Adjust the values in lookatpoint() such that Gretchen looks
    # at the red square.
    robot.lookatpoint(0,0,0)
    time.sleep(2)

    # TODO
    # Adjust the values in lookatpoint() such that Gretchen looks
    # at the green square.
    robot.lookatpoint(0,0,0)
    time.sleep(2)


#
# Program entry point when started directly
#
if __name__ == '__main__':
    print("Make sure to run 'rosrun look_at_point generate_marker' before "
          "executing this script!")
    main()
