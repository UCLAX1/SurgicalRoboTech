# run every kernel restart before anything else
from ultralytics import YOLO
from roboflow import Roboflow
import cv2
import numpy as np
import roslibpy

model = YOLO("yolov8n")


# print(model.names)

def center_points(source, mode):
    # cv2.imshow("image",image)

    results = model.predict(source=source)  # generator of Results objects
    # cv2.imshow("results", results)
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
        if (box.cls == 0):  # index 0 is human
            vip_Boxes.append(box)
    for box in vip_Boxes:
        # each box results in a format that looks something like this: tensor([[   0.0000,  384.7042, 2876.7173, 3832.7683]])
        str_box = str(box.xyxy)
        # print(str_box)
        for index in range(9, len(str_box) - 3):  # sanitizes the box output to cut off the tesnor part and brackets
            temp += str_box[index]
        captured_coords.append(temp)
        # print(temp)
        temp = ""
    space_temp = ""
    for coord in captured_coords:  # removes spaces from coordinatees
        # print("coord: " + str(coord) + " end")

        for i in range(len(coord)):
            if coord[i] != " ":
                space_temp += coord[i]
                # print(space_temp)
        formatted_coords.append(space_temp)
        space_temp = ""

    # print("captured coords: ", captured_coords)
    # print("formatted: " + str(formatted_coords))

    for coordinate in formatted_coords:
        # creates an array of floats with all the coordinates, so they can actually be used for math
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
    # print("coord_floats: " + str(coord_floats))
    # currently a bit of a mess when it does like a lot of people at the same time & no center point yet

    center_points = []

    temp_arr = []
    index_counter = 0

    for index in range(len(coord_floats)):  # calculates center points
        if index_counter != 4:
            temp_arr.append(coord_floats[index])
            index_counter += 1
        if index_counter == 4:
            # print(temp_arr)
            x_coord = (temp_arr[0] + temp_arr[1]) / 2
            y_coord = (temp_arr[2] + temp_arr[3]) / 2
            temp_arr = []
            coordinate = x_coord, y_coord
            center_points.append(coordinate)
            index_counter = 0
    # center_points is an array of center point floats formatted as (x,y)

    if mode == 0:  # debug mode
        print("number of vip boxes: " + str(len(vip_Boxes)))
        print("formatted length " + str(len(formatted_coords)))
        print("float length: " + str(len(coord_floats)) + "    debug: correct length - " + str(len(vip_Boxes) * 4))
        print("number of center points: " + str(len(center_points)) + "    debug: correct length - " + str(
            len(vip_Boxes)))
        print("center points: " + str(center_points))
    if mode == 1:  # center point mode
        print(center_points)


def yolo_center_points(camera_stream, camera_source, file_source, debug_mode):
    if camera_stream:
        cam = cv2.VideoCapture(camera_source)
        while True:
            result, image = cam.read()
            center_points(image, debug_mode)
    else:
        center_points(file_source, debug_mode)


yolo_center_points(True, 0, "people.jpg", 1)
# debug mode 0 prints debug statements, 1 is just center points
# if camera stream is True then file_source can be set to None but doesn't have to be
# file_source won't be read if camera_stream is set to true
