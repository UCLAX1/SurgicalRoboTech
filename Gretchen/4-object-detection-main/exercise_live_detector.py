#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Object detection with YOLOv3
# In this exercise, you learn how to perform object detection
# with YOLOv3 on Gretchen's video stream
#

import sys
sys.path.append('..')

# Import required modules
import cv2
import argparse
import numpy as np
import hashlib

from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

#
# Default parameters for network
# (YOLOv3)
#
cfg_path = "./yolov3.cfg"
weight_path= "./yolov3.weights"
class_name_path = "./yolov3.txt"

classes = None
COLORS = None

def loadClasses(filename):
    """ Load classes into 'classes' list and assign a random but stable color to each class. """
    global classes, COLORS

    # Load classes into an array
    try:
        with open(filename, 'r') as file:
            classes = [line.strip() for line in file.readlines()]
    except EnvironmentError:
        print("Error: cannot load classes from '{}'.".format(filename))
        quit()

    # Assign a random (but constant) color to each class
    # Method: convert first 6 hex characters of md5 hash into RGB color values
    COLORS = []
    for idx,c in zip(range(0, len(classes)), classes):
        cstr = hashlib.md5(c.encode()).hexdigest()[0:6]
        c = tuple( int(cstr[i:i+2], 16) for i in (0, 2, 4))
        COLORS.append(c)


def drawAnchorbox(frame, class_id, confidence, box):
    """ Draw an anchorbox identified by `box' onto frame and label it with the class name and confidence. """
    global classes, COLORS

    conf_str = "{:.2f}".format(confidence).lstrip('0')
    label = "{:s} ({:s})".format(classes[class_id], conf_str)
    color = COLORS[class_id]

    # Make sure we do not print outside the top/left corner of the window
    lx = max(box[0] + 5, 0)
    ly = max(box[1] + 15, 0)

    # 3D "shadow" effect: print label with black color shifted one pixel right/down, 
    #                     then print the colored label at the indented position.
    cv2.rectangle(frame, box, color, 2)
    cv2.putText(frame, label, (lx+1, ly+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(frame, label, (lx, ly), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def main():
    global cfg_path, weight_path, class_name_path, classes, COLORS

    #
    # Set default parameters
    #
    # blobFromImage
    scale = 1.0/255         # scale factor: normalize pixel value to 0...1
    meansub = (0, 0, 0)     # we do not use mean subtraction
    outsize = (416, 416)    # output size (=expected input size for YOLOv3)
    # result detection
    conf_threshold = 0.50   # confidence threshold
    nms_threshold = 0.4     # threshold for non-maxima suppression (NMS)

    #
    # Parse command line arguments
    #
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=False, help = 'path to input image')
    ap.add_argument('-c', '--confidence', required=False, help = 'confidence threshold', type=float)
    ap.add_argument('-m', '--nms', required=False, help = 'NMS threshold', type=float)
    # TODO
    # (1) add more command line arguments that allow 
    # - the specification of the network, the weights, and the labels
    # - to enable/disable the preview window
    # (2) define a boolean flag, such as 'isCam' that is True when the feed should be taken from the
    #     camera and is False otherwise

    args = ap.parse_args()

    if args.confidence is not None:
        conf_threshold = args.confidence
    if args.nms is not None:
        nms_threshold = args.nms
    # TODO
    # evaluate newly added parameters
    # ...

    isCam = False           # TODO: fix
    hasPreview = False      # TODO: fix

    #
    # Print configuration
    #
    print("Configuration:\n"
          "  Network:\n"
          "    config:      {}\n"
          "    weights:     {}\n"
          "    classes:     {}\n"
          "  Preprocessing:\n"
          "    scale        {:.3f}\n"
          "    mean subtr.  {}\n"
          "    output size  {}\n"
          "  Detection:\n"
          "    conf. thld   {:.3f}\n"
          "    nms. thld    {:.3f}"
          "\n"
          .format(cfg_path, weight_path, class_name_path, scale, meansub, outsize, conf_threshold, nms_threshold))

    #
    # Initialize network
    #
    # load DNN
    net = cv2.dnn.readNet(weight_path, cfg_path)

    # load classes
    loadClasses(class_name_path)

    # identify all output layers (depend on network: YOLOv3 has 3, YOLOv3-tiny has 2)
    layer_names = net.getLayerNames()
    output_layers = [ layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers() ]

    # print the names of all layers and, separately, all output layers
    print("Network information:\n"
          "  layer names:\n    {}"
          "  output layers:\n    {}"
          "\n"
          .format(layer_names, output_layers))

    #
    # Setup windows
    #
    cv2.namedWindow("ObjectDetection")
    if hasPreview:
        cv2.namedWindow("Preview")

    #
    # We only need to initialize the camera if we are actually going to use it
    #
    if isCam == True:
        ROSEnvironment()
        camera = Camera()
        camera.start()

    #
    # Here we go...
    #
    while(True):
        #
        # TODO
        #
        # - if the feed comes from the camera, set 'input_image' to the camera image,
        #   otherwise load image from disk
        # - determine height, width of image to analyze
        # - perform preprocessing, inference, and result extraction the same way as
        #   in example_image_detector.py (i.e., copy-paste the code and adjust a bit)

        if isCam == True:
            key = cv2.waitKey(10)
        else:
            key = cv2.waitKey()

        if key > 0:
            break

    cv2.destroyAllWindows()


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
