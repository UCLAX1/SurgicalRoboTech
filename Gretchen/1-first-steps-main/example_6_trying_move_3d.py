#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# First tries moving Gretchen.
# We use the following Robot API calls (in addition to the 
# obvious start()):
# - lookatpoint():  move Gretchen's head to 'look at' the
#                   given coordinates.
#
# The arguments to lookatpoint() are
#   lookatpoint(x, y, z, velocity=10.8)
#
# where x,y,z are 3d coordinates in the robot frame (Gretchen's
# base).
#
# The optional 'velocity' parameter allows you to control the
# speed of the movement.
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

    # Look at point (1,1,1) in real-world (Gretchen's base frame)
    # coordinates
    robot.lookatpoint(1,1,1)
    time.sleep(1)

    # Add your own code and have Gretchen look at different
    # points using 'lookatpoint()'





#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
