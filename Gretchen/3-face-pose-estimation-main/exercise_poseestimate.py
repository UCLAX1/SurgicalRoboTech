#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Face pose estimation
# Press a key to exit program (with camera window focused)
#

# Import required modules
import cv2
import sys
import numpy as np
import dlib
import time
from imutils import face_utils

# TODO replace the precompiled FaceDetector with your own once you have
#      worked your way through all TODOs in this file
from facedetector import FaceDetector
#from exercise_facedetector import FaceDetector
from history import History

import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
from lib.robot import Robot

def main():
    # Initalize ROS environment, robot and camera
    ROSEnvironment()
    robot = Robot()
    robot.start()
    camera = Camera()
    camera.start()

    # Initalize our face detector
    face_detector = FaceDetector()

    # Create two windows
    cv2.namedWindow("FaceDetector")
    cv2.namedWindow("Wireframe")

    # Initialize weighted history for rotation & translation vectors
    weights = [ 0.8, 0.6, 0.4, 0.2, 0.1 ]
    r_hist = History(3, weights)
    t_hist = History(3, weights)

    # Tell Numpy to print 3 decimal digits for float arrays
    np.set_printoptions(precision=3)

    # Loop
    while True:
        # Get image from camera an create a white copy of the image
        img = camera.getImage()
        white = img.copy()
        white.fill(255)

        # Find all faces using the face detector
        faces = face_detector.detect(img)

        # Draw bounding boxes around all faces and also remember the largest deteted face
        max_area = 0
        max_face = None
        for face in faces:
            # TODO
            # - use cv2's rectangle() function to draw the bounding box
            #   refer to https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga07d2f74cadcf8e305e810ce8eed13bc9
            #   use (face.left(), face.top()) for point 1 and (face.right(), face.bottom()) for point 2
            # - check if the area of the bounding box is bigger than the so-far biggest bounding box and, if so,
            #   remember the new largest area and the face
            pass

        # Estimate the face pose for the largest detected face (if any)
        if max_face is not None:
            (success, v_rot, v_trans, image_points) = face_detector.estimatePose(img, max_face)

            if success == True:
                # Print rotation and translation vectors
                # TODO disable once you have familiarized yourself with the returned values
                print("Face pose:\n"
                      "----------\n"
                      "Rotation:\n{}\n"
                      "Translation:\n{}\n\n"
                      .format(v_rot, v_trans))

                # TODO
                # Determine which elements in the rotation/translation vectors refer to which angle/coordinate
                # Also find out what each face pose means in numerical values (i.e., up = v_rot[0][2] 
                # Write your results directly into the code here
                #
                # v_rot[0][<index>]: pitch ---> up: <value> ... <value>: down
                # v_rot[0][<index>]: roll  ---> up: <value> ... <value>: down
                # v_rot[0][<index>]: yaw   ---> up: <value> ... <value>: down
                # 
                # v_trans[0][<index>]: x
                # v_trans[0][<index>]: y
                # v_trans[0][<index>]: z


                # Ignore outliers to not pollute our history
                # TODO find reasonable limits for valid values in v_rot, then filter out outliers
                # - the values for v_trans are given, but you feel free to modify
                # - enable the code block once you have entered the limits
                #if (v_rot[0][0] < -5 or v_rot[0][0] > 5 or
                #    v_rot[1][0] < -5 or v_rot[1][0] > 5 or
                #    v_rot[2][0] < -5 or v_rot[2][0] > 5 or 
                #    abs(v_trans[0][0]) > 480 or abs(v_trans[1][0]) > 640 or
                #    v_trans[2][0] < -1000 or v_trans[2][0] > 3000):
                #    continue

                # Overlay pose on frame
                img = face_detector.drawPose(img, v_rot, v_trans, image_points)

                # Also draw pose on wireframe model
                white = face_detector.drawPose(white, v_rot, v_trans, image_points)


                # Add values to history and get average
                r_hist.add(v_rot)
                t_hist.add(v_trans)

                weighted_r = r_hist.average()
                weighted_t = t_hist.average()

                # Print averaged values of rotation and translation
                # TODO first, enable once you have completed the TODOs above, then disable after finding
                #      the values that help you determine the face pose
                #print("Weighted Face pose:\n"
                #      "-------------------\n"
                #      "Rotation:\n{}\n"
                #      "Translation:\n{}\n\n"
                #      .format(weighted_r, weighted_t))


                # Verbose head position

                # Evaluation of weighted rotation matrix
                # TODO
                # - fill in the indices you determined above for pitch, roll, yawn, and the translation vector
                # - then determine what values constitute good limits for each movement
                TODO = 0.0  # TODO: remove once you have filled in the actual limits
                INDEX = 0   # TODO: remove once you have filled in the actual indices
                if weighted_r[INDEX] < TODO:
                    pitch = "up"
                elif weighted_r[INDEX] > TODO:
                    pitch = "down"
                else:
                    pitch = "level"

                if weighted_r[INDEX] < TODO:
                    roll = "left"
                elif weighted_r[INDEX] > TODO:
                    roll = "right"
                else:
                    roll = "level"

                if weighted_r[INDEX] < TODO:
                    yaw = "left"
                elif weighted_r[INDEX] > TODO:
                    yaw = "right"
                else:
                    yaw = "straight"
                if abs(weighted_r[INDEX]) > TODO:
                    yaw = "strong " + yaw

                # Evaluation of weighted translation matrix
                # (i.e., where is the face in the image?)
                pos = "of"
                if abs(weighted_t[0]) <= 100 and abs(weighted_t[1]) <= 100:
                    pos = "in"
                else:
                    if weighted_t[0] < -100:
                        pos = "left " + pos
                    elif weighted_t[0] > 100:
                        pos = "right " + pos

                    if weighted_t[1] < -100:
                        pos = "top " + pos
                    elif weighted_t[1] > 100:
                        pos = "bottom " + pos

                if weighted_t[2] > 1800:
                    dist = "away"
                elif weighted_t[2] < 1000:
                    dist = "close"
                else:
                    dist = "normal distance"


                # Print head position
                print("Head position:\n"
                      "  looking {} {}, tilted {}\n"
                      "  {} center, {}\n".format(pitch, yaw, roll, pos, dist))



        # show image (imshow expects BGR format, hence we reverse the last dimension from RGB to BGR)
        cv2.imshow("FaceDetector", img[...,::-1])
        cv2.imshow("Wireframe", white[...,::-1])

        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
