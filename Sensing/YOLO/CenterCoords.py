# import necessary packages
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

# set yolo model to version 8
model = YOLO("yolov8n")

# read in image from .jpg file
image = 'Orange.jpg'

# run yolov8 object detection
results = model(image)
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image
    coords = r.boxes.xywh.numpy()  # saves the boxes class as an array of arrays

# isolate first object in results array
objectXYWH = coords[0]

# print out center values of object
print()
print("x value equals: " + str(objectXYWH[0]))
print("y value equals: " + str(objectXYWH[1]))