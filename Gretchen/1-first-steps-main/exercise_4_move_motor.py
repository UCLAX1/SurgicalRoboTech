#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - make your robot nod in agreement or shake
#   its head in disagreement.
# - try using both left/right/up/down and the
#   move API
#

# Import required modules
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
import time


def startNod(robot):
    robot.center()
    time.sleep(1)

    # TODO
    # Insert commands that make the robot nod
    # - version 1: use up/down
    # - version 2: use move


def startShake(robot):
    robot.center()
    time.sleep(1)

    # TODO
    # Insert commands that make the robot shake its head
    # - version 1: use left/right
    # - version 2: use move


def main():
    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Initalize & start robot
    robot = Robot()
    robot.start()

    # Nod
    startNod(robot)
    sleep(2)

    # Shake
    startNod(robot)
    sleep(2)

    # Shake another time
    startNod(robot)
    sleep(2)

    # Nod again
    startNod(robot)
    sleep(2)


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
