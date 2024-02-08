#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Shows a live image from Gretchen's camera and draws
# a circle around the last point clicked with the mouse.
# We also show the mouse coordinates and the pixel's
# RGB color information in the terminal.
# Press a key to exit program (with camera window focused)
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

        # Print coordinate and color info from image
        print('Point', u,v)
        print('RGB', img[v,u])


def main():
    # Refer to global variable 'point'
    global point

    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Start camera (already initialized above)
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

        # Use OpenCV to draw a circle around clicked point
        cv2.circle(img, point, 10, (0, 0, 255), 3)

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
