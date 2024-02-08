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
# - left()/right(): move Gretchen's head to the left/right
# - up/down():      move Gretchen's head up/down
#
# For all functions, the arguments are
#   direction(delta=0.1, resend=False)
#
# All movements 'delta' are relative to the current position 
# of Gretchen's head. left/right/up/down limit the pan/tilt 
# angle to [-1...+1] radian in order not to pull out any
# of Gretchen's cables.
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

    # Center robot
    # Note: if you're Gretchen does not look straight ahead but 
    # 90 degrees up, down, left, or right, you have assembled 
    # Gretchen wrongly...time to get a screwdriver :-)
    robot.center()
    time.sleep(1)                   # sleep for 1 second

    # Move head a bit to the left
    robot.left(0.2)
    time.sleep(1)

    # Move head a bit to the right
    robot.right(0.2)
    time.sleep(1)

    # Add your own code and move Gretchen's head to different
    # positions, including up & down!





#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
