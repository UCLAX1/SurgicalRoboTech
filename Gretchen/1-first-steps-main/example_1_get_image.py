#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Shows a live image from Gretchen's camera.
# Press a key to exit program (with camera window focused)
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

        # Use OpenCV to show image in a window named "Frame"
        # Note: imshow() expects the image to be in BRG format, 
        #       whereas camera.getImage() returns images in RBG 
        #       format. The [...,::-1] uses Python's array slicing
        #       capabilities to reverse the innermost dimension
        #       of the array from (r,g,b) to (b,g,r)
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
