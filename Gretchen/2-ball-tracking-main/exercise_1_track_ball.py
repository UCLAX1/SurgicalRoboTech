#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Detect and track a ball
# Press a key to exit program (with camera window focused)
#
# Currently, this exercise is a copy of example 2. Modify it such that
# * it allows the user to click on the image and select the color of the filter
# * it moves Gretchen's head to follow the largest detected circle.
#

# Import required modules
import cv2
import sys
from example_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment


# Initalize globals
camera = Camera()
point = (0,0)

def rgb2hsv(r, g, b):
    r = float(r) / 255
    g = float(g) / 255
    b = float(b) / 255

    v = xmax = max(r, g, b)
    xmin = min(r, g, b)
    c = xmax - xmin

    # hue (0..360)
    if c == 0:
        h = 0
    elif v == r:
        h = int(60 * (0 + (g - b) / c))
    elif v == g:
        h = int(60 * (2 + (b - r) / c))
    else:
        h = int(60 * (4 + (r - g) / c))

    if (h < 0):
        h = 360 + h

    # saturation on an integer scale from 0..100
    if v > 0:
        s = int(255 * c / v)
    else:
        s = 0

    # value an integer scale from 0..100
    v = int(255 * v)
    return h, s, v


def clickColor(event, u, v, flags, param):
    # access global variable 'point'
    global point
    img = camera.getImage()

    # If left button is clicked...
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (u, v)
        (R, G, B) = img[v, u]

        # Convert RBG to HSV
        (H, S, V) = rgb2hsv(R, G, B)
        clow = ((H * .5) - 10, S * .5, v * .5)
        chigh = ((H * .5) + 10, 255, 255)

        ball_detector.setLower(clow)
        ball_detector.setUpper(chigh)


def main():
    global ball_detector
    global point


    # Initalize ROS environment and camera
    ROSEnvironment()
    camera = Camera()
    camera.start()

    # Initalize ball detector
    ball_detector = BallDetector()

    # Announce frame and set mouse handler
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", clickColor)


    # Loop
    while True:
        # access global variable 'point'
        global point

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
