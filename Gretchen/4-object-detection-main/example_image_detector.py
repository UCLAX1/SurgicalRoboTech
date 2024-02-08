#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Object detection with YOLOv3
# This example demonstrates how to perform object detection
# with YOLOv3 on a single image loaded from disk.
#

import sys
sys.path.append('..')

# Import required modules
import cv2
import argparse
import numpy as np
import hashlib

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
    ap.add_argument('-i', '--image', required=True, help = 'path to input image')
    ap.add_argument('-c', '--confidence', required=False, help = 'confidence threshold', type=float)
    ap.add_argument('-m', '--nms', required=False, help = 'NMS threshold', type=float)
    args = ap.parse_args()

    if args.confidence is not None:
        conf_threshold = args.confidence
    if args.nms is not None:
        nms_threshold = args.nms

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
    cv2.namedWindow("Preview")
    cv2.namedWindow("ObjectDetection")

    #
    # Load image from disk
    #
    input_image = cv2.imread(args.image)
    if input_image is None:
        print("Error: cannot load image '{}'.".format(args.image))
        quit()
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    width = input_image.shape[1]
    height = input_image.shape[0]

    #
    # Preprocess image
    #
    # create blob from input image after mean subtraction and normalization
    blob = cv2.dnn.blobFromImage(input_image, scale, outsize, meansub, swapRB=False, crop=False)

    #
    # Inference: run forward pass through network
    #
    # feed the image blob to the neural net
    net.setInput(blob)

    # run inference and return results from identified output layers (2 for YOLOv3-tiny, 3 for YOLOv3)
    preds = net.forward(output_layers)

    #
    # Iterate through all detected anchor boxes in each output layer
    #
    # the format of an anchor box is
    #   [0:1] center (x/y), range 0..1 (multiply by image width/height)
    #   [2:3] dim    (x/y), range 0..1 (multiply by image width/height)
    #   [4]   p_obj  probability that there is an object in this box
    #   [5:]  probabilities for each class (80 with YOLOv3 / COCO)
    #
    # an anchor's total confidence is obj * argmax(class probabilities)
    #
    # initialize empty result lists
    class_ids = []
    confidence_values = []
    bounding_boxes = []

    for pred in preds:
        for anchorbox in pred:
            class_id = np.argmax(anchorbox[5:])
            confidence = anchorbox[4] * anchorbox[class_id + 5]

            # for analysis/debugging, we allow a separate (manual) threshold
            # replace 0 with 1 if you are not interested in predictions below the confidence threshold
            if confidence >= conf_threshold or confidence >= 0:
                cx = int(anchorbox[0] * width)      # center of anchorbox in image
                cy = int(anchorbox[1] * height)     #   in x & y direction
                dx = int(anchorbox[2] * width)      # dimensions of ancherbox in image
                dy = int(anchorbox[3] * height)     #   in x & y direction

                x  = int(cx - dx/2)                 # x/y coordinate of
                y  = int(cy - dy/2)                 #   anchorbox

                # print result
                print("[ ({:3d}/{:3d}) - ({:3d}/{:3d}): Pobj: {:.3f}, Pclass: {:.3f} -> Ptotal: {:.3f}, class: {:s} ]"
                        .format(x, y, x+dx, y+dy, anchorbox[4], anchorbox[class_id + 5], confidence, classes[class_id]))

                # only consider prediction if total confidence is above threshold
                if confidence >= conf_threshold:
                    class_ids.append(class_id)
                    confidence_values.append(float(confidence)) # find out what happens in NMSBoxes if you remove the typecast...
                    bounding_boxes.append([x, y, dx, dy])

    #
    # Preview: show all anchorboxes with a total confidence > conf_threshold
    #
    preview = input_image.copy()
    for idx, classid in enumerate(class_ids):
        drawAnchorbox(preview, classid, confidence_values[idx], bounding_boxes[idx])

    #
    # Run the NMS (Non Maximum Suppression) algorithm to eliminate boxes with a low confidence 
    # and those that overlap too much
    #
    if nms_threshold >= 0:
        indices = cv2.dnn.NMSBoxes(bounding_boxes, confidence_values, conf_threshold, nms_threshold)
    else:
        # include all boxes
        indices = range(0, len(bounding_boxes))

    #
    # Overlay final results on image
    #
    indices = np.reshape(indices, -1)
    for idx in indices:
        drawAnchorbox(input_image, class_ids[idx], confidence_values[idx], bounding_boxes[idx])

    #
    # Display results
    #
    cv2.imshow("Preview", preview[...,::-1])                    # swap RGB -> BGR
    cv2.imshow("ObjectDetection", input_image[...,::-1])        # idem
    key = cv2.waitKey()

    cv2.destroyAllWindows()


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
