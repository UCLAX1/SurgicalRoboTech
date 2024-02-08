#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Explore RGB and HSV color spaces.
# Prints coordinates, RGB and HSV values of clicked pixel.
# Press a key to exit program (with camera window focused)
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

# Initalize globals
camera = Camera()
point = (0,0)

# convert a value in RGB into HSV
# see https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
def rgb2hsv(r, g, b):
    r = float(r) / 255
    g = float(g) / 255
    b = float(b) / 255

    print(r, g, b)

    v = xmax = max(r, g, b)
    xmin = min(r, g, b)
    c = xmax - xmin

    print(v, xmin, c)

    # hue (0..360)
    if c == 0:
        h = 0
    elif v == r:
        h = int(60 * (0 + (g-b)/c))
    elif v == g:
        h = int(60 * (2 + (b-r)/c))
    else:
        h = int(60 * (4 + (r-g)/c))

    if (h < 0):
        h = 360 + h

    # saturation on an integer scale from 0..100
    if v > 0:
        s = int(255 * c / v)
    else:
        s = 0

    # value an integer scale from 0..100
    v = int(255 * v)

    print(h, s, v)

    return h, s, v


# Method executed on mouse event in camera image
def onMouse(event, u, v, flags, param):
    # access global variable 'point'
    global point

    # If left button is clicked...
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get image from camera
        img = camera.getImage()

        point = (u,v)
        (R, G, B) = img[v,u]

        # Convert RBG to HSV
        (H, S, V) = rgb2hsv(R, G, B)

        # print result
        print("Point clicked:   ({}/{})\n"
              "  RGB value:     ({:3d}, {:3d}, {:3d})\n"
              "  HSV value:     ({:3d}, {:3d}, {:3d})"
              .format(v, u,
                      R, G, B,
                      H, S, V))


        # double check using OpenCV
        # convert entire image to HSV
        # refer to https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#cvtcolor
        # Note that OpenCV uses a range of 0..179 for hue, so we scale it back to 0..359 when printing
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        (H, S, V) = hsv[v,u]

        print("  HSV (OpenCV):  ({:3d}, {:3d}, {:3d})\n"
              .format(H*2, S, V))


def main():
    # access global variable 'point'
    global point

    # Initalize ROS environment and camera
    ROSEnvironment()
    camera.start()

    # Announce frame and set mouse handler
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", onMouse)

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Draw circle 
        cv2.circle(img, point, 10, (0, 0, 255), 3)

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
