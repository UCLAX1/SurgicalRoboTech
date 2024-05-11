# run every kernel restart before anything else
from ultralytics import YOLO
from roboflow import Roboflow
import cv2
import numpy as np
import roslibpy
model = YOLO("yolov8n")

# print(model.names)

cam = cv2.VideoCapture(0)


# while True:
result, image = cam.read()
# cv2.imshow("image",image)
results = model.predict(source="people.jpg")  # generator of Results objects
# print(results)
vip_Boxes = []
temp = ""
captured_coords = []
formatted_coords = []
coord_floats = []
float_temp = 0.0

boxes = results[0].boxes  # Boxes object for bbox outputs
masks = results[0].masks  # Masks object for segment masks outputs
probs = results[0].probs  # Class probabilities for classification outputs
for box in boxes:
    if(box.cls == 0): # index 0 is human
        # print("Found a human")
        vip_Boxes.append(box)
for box in vip_Boxes:
    # each box results in a format that looks something like this: tensor([[   0.0000,  384.7042, 2876.7173, 3832.7683]])
    str_box = str(box.xyxy)
    for index in range (9,len(str_box) - 3): # sanitizes the box output to cut off the tesnor part and brackets
        temp += str_box[index]
    captured_coords.append(temp)
    # print(temp)
    temp = ""
    for coord in captured_coords: # removes spaces from coordinatees
        print("coord: " + str(coord) + " end")
        space_temp = ''
        for i in range(len(coord)):
            if(coord[i] != " "):
                space_temp += coord[i]

        formatted_coords.append(space_temp)

print("formatted: " + str(formatted_coords))

for coordinate in formatted_coords:
    # creates an array of floats with all the coordinates, so they can actually be
    # used for math
    for index in range(len(coordinate)):
        if index == len(coordinate) - 1:
            float_temp = float(temp)
            temp = ''
            coord_floats.append(float_temp)
        #     end point check & does same thing as comma check
        elif coordinate[index] != ",":
            temp += coordinate[index]
        #     building temp
        elif coordinate[index] == ",":
            float_temp = float(temp)
            temp = ''
            coord_floats.append(float_temp)
        #     comma means end of coordinate so built temp is converted to float and added to array of float
print("coord_floats: " + str(coord_floats))
# currently a bit of a mess when it does like a lot of people at the same time & no center point yet