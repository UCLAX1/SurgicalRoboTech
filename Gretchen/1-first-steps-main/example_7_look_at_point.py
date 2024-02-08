#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# First tries moving Gretchen.
# Combine the camera with the robot to have Gretchen
# look at the point clicked in the image.
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment


# Create camera & robot
camera = Camera()
robot = Robot()

# Image point
p = (320, 240)

# Method executed on click in camera image
def onMouse(event, u, v, flags, param):
    global p

    # If left button is clicked...
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print 2d coordinates of clicked pixel (y/x on image)
        p = (u, v)
        print("Image:         ({}, {})".format(u,v))

        # Convert the 2d coordinates to 3d coordinates in camera frame
        # and print the result
        (x,y,z) = camera.convert2d_3d(u,v)
        print("Camera frame: ({}, {}, {})".format(x,y,z))

        # Convert the 3d coordinates from the camera frame into
        # Gretchen's frame using a transformatio matrix, then
        # print the result and have Gretchen look at that point
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print("Robot frame:  ({}, {}, {})".format(x,y,z))
        robot.lookatpoint(x,y,z)


def main():
    global p

    # Initalize ROS environment, start robot and camera
    ROSEnvironment()
    robot.start()
    camera.start()

    # Create a window called "Frame" and install a mouse handler
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", onMouse)

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Use OpenCV to draw a circle around clicked point
        # Change the color of the circle
        cv2.circle(img, p, 10, (0, 0, 255), 3)

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
