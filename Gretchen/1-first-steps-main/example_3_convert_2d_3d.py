#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Shows a live image from Gretchen's camera. When the user
# clicks on the image, we print the 2d coordinates of the
# click point, the 3d coordinates in the camera frame, and
# the translated 3d coordinates in the robot (Gretchen's) frame.
#
# Press a key to exit program (with camera window focused)
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment


# Initalize camera
camera = Camera()


# Method executed on click in camera image
def onMouse(event, u, v, flags, param):
    # If left button is clicked...
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print 2d coordinates of clicked pixel (y/x on image)
        print("Image:         ({}, {})".format(u,v))

        # Convert the 2d coordinates to 3d coordinates in camera frame
        # and print the result
        (x,y,z) = camera.convert2d_3d(u,v)
        print ("Camera frame: ({}, {}, {})".format(x,y,z))

        # Convert the 3d coordinates from the camera frame into
        # Gretchen's frame using a transformatio matrix, then
        # print the result
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print ("Robot frame:  ({}, {}, {})".format(x,y,z))


def main():
    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Start camera
    camera.start()

    # Tell OpenCV we are going to create a window called "Frame"
    cv2.namedWindow("Frame")

    # Make OpenCV call our function 'onMouse' whenever the mouse
    # is clicked in the camera image
    cv2.setMouseCallback("Frame", onMouse)

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

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
