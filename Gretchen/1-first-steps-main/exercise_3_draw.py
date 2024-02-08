#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - manually draw a rectangle onto camera frame
#
# Additional ideas:
# - draw rectangle around point clicked on image
#   (requires more significant changes; combine
#    code from exercise_2_* with this one)
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
        # Get image from camera
        img = camera.getImage()

        # TODO
        # Set bountaries for rectangle in image coordinates
        y_min =
        y_max =

        x_min =
        x_max =

        # TODO
        # Manually draw the rectangle on the image
        # - add an inner loop to cover the x range
        # - set pixel color to a color of your choice
        for y in range(y_min,y_max):
            ...
                ...

        # Show image
        cv2.imshow("Frame", img[...,::-1])

        # Exit loop if key was pressed
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
