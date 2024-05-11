# run every kernel restart before anything else
from ultralytics import YOLO
from roboflow import Roboflow
import cv2
import numpy as np
import roslibpy
model = YOLO("yolov8n")

# print(model.names)

cam = cv2.VideoCapture(0)


while True:
    result, image = cam.read()
    # cv2.imshow("image",image)
    results = model.predict(source=image, stream = True)  # generator of Results objects
    vip_Boxes = []
    temp = ""
    captured_coords = []
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        masks = r.masks  # Masks object for segment masks outputs
        probs = r.probs  # Class probabilities for classification outputs
        for box in boxes:
            if(box.cls == 0): # index 0 is human
                # print("Found a human")
                vip_Boxes.append(box)
        for box in vip_Boxes:
            str_box = str(box.xyxy)
            # print(str_box)
            # print(len(str_box))
            
            for index in range (9,len(str_box) - 3):
                temp  += str_box[index]
            captured_coords.append(temp)
            # print(temp)
            temp = ""

    print(captured_coords)