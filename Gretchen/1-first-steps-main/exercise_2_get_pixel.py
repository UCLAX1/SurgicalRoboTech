#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Do it yourself:
# - print coordinates and color info of clicked
#   pixel in camera feed
# - change color of circle drawn around clicked point
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera


# Initalize global camera
camera = Camera()
# Initalize global point
point = (0,0)


# Method executed on click in camera image
def onMouse(event, u, v, flags, param):
    # Refer to global variable 'point'
    global point

    # Is event 'left button down'?
    if event == cv2.EVENT_LBUTTONDOWN:
        # Save mouse coordinates in global variable 'point'
        point = (u,v)

        # Retrieve image from camera
        img = camera.getImage()

        # TODO
        # Print coordinate and color info from image
        print(...)
        print(...)


def main():
    # Refer to global variable 'point'
    global point

    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Start camera (already initialized above)
    camera.start()

    # Create a window called "Frame" and install a mouse handler
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", onMouse)

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Use OpenCV to draw a circle around clicked point
        # TODO
        # Change the color of the circle
        cv2.circle(img, point, 10, (0, 0, 255), 3)

        # Use OpenCV to show image in a window named "Frame"
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
