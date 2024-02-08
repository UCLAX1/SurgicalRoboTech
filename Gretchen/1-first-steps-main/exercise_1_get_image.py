#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - read image from Gretchen's camera
# - display image using OpenCV
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera


def main():
    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Initialize & start camera
    camera = Camera()
    camera.start()

    # Loop
    while True:
        # TODO
        # Get image from camera
        img = ...

        # TODO
        # Use OpenCV to show image in a window named "Frame"
        # Play around with the array slicing parameter and
        # observe how the colors change.
        cv2....

        # Exit loop if key was pressed
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
