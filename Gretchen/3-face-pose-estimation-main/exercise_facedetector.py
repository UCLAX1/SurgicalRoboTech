#
# First Steps in Programming a Humanoid AI Robot
#
# FaceDetector class
# Detect faces using Dlib's 68-point face detector and perform pose estimation
#

import numpy as np
import cv2
import imutils
import dlib

class FaceDetector:
    # indices into Dlib's 68-point face detector output array (0-indexed)
    # see https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/ for a map of the 68 points on the face
    NOSE = TODO # nose tip
    CHIN = TODO # chin
    LEYE = TODO # left eye, left corner
    REYE = TODO # right eye, right corner
    MOUL = TODO # mouth, left corner
    MOUR = TODO # mouth, right corner

    def __init__(self, img_w=640, img_h=480):
        # Initalize detector & pretrained predictor for pose estimation
        # see https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/
        # also note that this dataset (and thus the trained predictor) comes with a non-commercial license
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')


        # Camera matrix containing
        # - focal length (f)
        # - optical center in image (c)
        # - radial distortion parameters
        #
        # If you are serious refer to "Camera calibration with OpenCV" at
        #   https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
        #
        # Lazy (usually good-enough) approximtion:
        # - focal length: w = width of image; then 0.7w <= f <= w.
        #   (see https://learnopencv.com/approximate-focal-length-for-webcams-and-cell-phone-cameras/)
        # - optical center: center of image
        # - no radial distortion
        f = TODO

        cx = TODO
        cy = TODO

        self.camera_matrix = np.array(
            [
              [ f,  0, cx],
              [ 0,  f, cy],
              [ 0,  0,  1]
            ], dtype = "double")

        self.distortion_coeffs = np.zeros((4,1))

        # For debugging purposes. Feel free to remove once you know that the camera matrix and
        # the distortion coefficients look good
        print ("Camera Matrix :\n {0}".format(self.camera_matrix))
        print ("Dist. Coeffs  :\n {0}".format(self.distortion_coeffs))


    # Detect face
    def detect(self, frame):
        """Detect faces using Dlib's internal frontal face detector"""

        # TODO
        # - call the face detector and return the identified faces (replace the next line)
        faces = TODO

        return faces


    def estimatePose(self,frame, rect):
        """Estimate face pose using Dlib's 68-point predictor"""

        # TODO
        # - call the shape predictor to predict the (2D) location of the 68 face landmarks
        # - convert the returned shape into a Numpy array
        shape = TODO
        shape = TODO

        # extract points we want to match to our 3D model face
        image_points = np.array([
                                    (shape[self.NOSE, :]),   # Nose tip
                                    (shape[self.CHIN, :]),   # Chin
                                    (shape[self.LEYE, :]),   # Left eye left corner
                                    (shape[self.REYE, :]),   # Right eye right corner
                                    (shape[self.MOUL, :]),   # Left Mouth corner
                                    (shape[self.MOUR, :])    # Right mouth corner
                                ], dtype="double")

        # 3D points of the face model. The number and order of these model points must
        # match the parameters we extracted into 'image_points' above.
        # You can experiment with these coordinates to maybe match your face more closely
        model_points = np.array([
                                        (   0.0,    0.0,    0.0),  # Nose tip
                                        (   0.0, -330.0,  -65.0),  # Chin
                                        (-225.0,  170.0, -135.0),  # Left eye left corner
                                        ( 225.0,  170.0, -135.0),  # Right eye right corner
                                        (-150.0, -150.0, -125.0),  # Left Mouth corner
                                        ( 150.0, -150.0, -125.0)   # Right mouth corner
                                    ])

        # TODO
        # - Find rotation and translation vectors through Perspective-n-Point (PnP) pose computation
        #   Refer to https://docs.opencv.org/3.4/d5/d1f/calib3d_solvePnP.html for details
        (success, v_rot, v_tran) = TODO

        return (success, v_rot, v_tran, shape)


    def drawFacePoints(self, frame, points, color=(0,0,255)):
        """Mark a wireframe of Dlib's 68 face feature points with dots on frame"""

        # draw a dot for each feature point
        # TODO
        # - use a for loop to iterate over all points p in 'points'
        # - use cv2's circle() function to draw a circle at point p
        #   refer to https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html 

        return frame


    def drawPolyline(self, frame, points, start, end, isClosed=False, color=(0,0,255)):
        """Draw a polyline from a range of points"""

        # create a list of points from points[start] to points[end] (including)
        pts = []
        # TODO
        # - iterate through 'points' from 'start' to 'end+1'
        # - add each point to the list 'pts'

        # convert list into Numpy integer array
        pts = np.array(pts, dtype=np.int32)

        # draw polygonal lines
        # TODO
        # - use cv2's polylines() function. Pass on arguments are required.
        #   refert to https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#gaa3c25f9fb764b6bef791bf034f6e26f5


    def drawFaceWireframe(self, frame, points, color=(0,0,255)):
        """Draw a wireframe of Dlib's 68 face feature points onto frame"""

        # draw polylines of different facial features
        # TODO
        # - refer to the map of the facial features at https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/
        # - call self.drawPolyline(frame, points, <start index>, <end index>) to draw an element.
        #    If the contour is closed, pass 'isClosed=True'
        # - draw the following elements
        #   face contour, right eye brow, left eye brow, node bridge, node line, right eye contour, left eye contour,
        #   outer lip contour, innner lip contour.

        # connect end of nose bridge with center of nose line
        # TODO
        # - extract the two relevant points (Nose tip (defined above as NOSE) and center of nose line)
        #   Note: you have to convert the elements of the points to integers by type casting them to
        #         and int. For example:: int(points[77][0])
        # - use cv2.line() to draw a line between the two points
        #   refer to https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga7078a9fae8c7e7d13d24dac2520ae4a2

        return frame


    # Draw pose
    def drawPose(self,frame, v_rot, v_tran, image_points):
        """Draw a wireframe of Dlib's 68 face feature points onto frame"""

        # impose identified points on frame
        self.drawFacePoints(frame, image_points)
        self.drawFaceWireframe(frame, image_points)

        # 3D point (0, 0, 500.0) is projected on to the image plane using the face's rotation/translation vectors
        # https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga1019495a2c8d1743ed5cc23fa0daff8c
        (pinocchio, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), v_rot, v_tran, 
                                                  self.camera_matrix, self.distortion_coeffs)

        # nose direction: center of nose line to projected 3d point
        p1 = ( int(image_points[33][0]), int(image_points[33][1]))
        p2 = ( int(pinocchio[0][0][0]), int(pinocchio[0][0][1]))
        cv2.line(frame, p1, p2, (255,0,0), 2)

        return frame
