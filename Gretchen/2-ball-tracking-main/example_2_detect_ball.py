#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Detect a ball
# Press a key to exit program (with camera window focused)
#

# Import required modules
import cv2
import sys
from example_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

def main():
    # Initalize ROS environment and camera
    ROSEnvironment()
    camera = Camera()
    camera.start()

    # Initalize ball detector
    ball_detector = BallDetector()

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Run ball detector on image
        (img, center) = ball_detector.detect(img)

        # Display image
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
