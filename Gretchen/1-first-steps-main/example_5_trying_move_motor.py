#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# First tries moving Gretchen.
# We use the following Robot API calls (in addition to the 
# obvious start()):
# - center():       centers the head of Gretchen by
#                   setting the angles on both motors
#                   to 0. 
# - move():         move Gretchen's head to an absolute position
#
# The arguments to move() are
#   move(pan_rad, tilt_rad, resend=False)
#
# where pan_rad and tilt_rad are the absolute values for pan/tilt
# in radians. Note that unlike for left/right/up/down, no safety 
# checks are made in move - Gretchen will try to move to any 
# given position!
#
# If 'resend' is True, the Gretchen library reads back the 
# position of the motors and resends the command if necessary.
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

    # Move robot to 0/0 (identical to robot.center())
    robot.move(0, 0)
    time.sleep(0.5)     # sleep half a second

    # Move robot 0.1 radian to the right and down
    robot.move(-0.1, -0.1)
    time.sleep(0.5)

    # Move robot 0.1 radian to the left and up
    robot.move(0.1, 0.1)
    time.sleep(0.5)

    # Add your own code and move Gretchen's head to different
    # positions using 'move()'





#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
