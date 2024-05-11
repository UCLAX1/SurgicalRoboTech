# run every kernel restart before anything else
from ultralytics import YOLO
from roboflow import Roboflow
import cv2
import numpy as np
import roslibpy
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
model = YOLO("yolov8n")


class coordPub(Node): 
    def __init__(self):
        super().__init__('coord_pub')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'humanCoords', 10)
        timer_period = 1 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cam = cv2.VideoCapture(0)
        self.vip_Boxes = []
        self.temp = ""
        self.captured_coords = []
        self.formatted_coords = []
        self.coord_floats = []
        self.float_temp = 0.0
    def timer_callback(self):
        result, image = self.cam.read()
        results = model.predict(source="image")
        boxes = results[0].boxes  # Boxes object for bbox outputs
        msg = Float32MultiArray()

        # Format box output into x,y center coordinates and input into data 
        for box in boxes:
            if(box.cls == 0): # index 0 is human
                # print("Found a human")
                self.vip_Boxes.append(box)
        for box in self.vip_Boxes:
            # each box results in a format that looks something like this: tensor([[   0.0000,  384.7042, 2876.7173, 3832.7683]])
            str_box = str(box.xyxy)
            for index in range (9,len(str_box) - 3): # sanitizes the box output to cut off the tesnor part and brackets
                temp += str_box[index]
            self.captured_coords.append(temp)
            temp = ""
            for coord in self.captured_coords: # removes spaces from coordinatees
                print("coord: " + str(coord) + " end")
                space_temp = ''
                for i in range(len(coord)):
                    if(coord[i] != " "):
                        space_temp += coord[i]
                self.formatted_coords.append(space_temp)

        # for coordinate in formatted_coords:
        #     # creates an array of floats with all the coordinates, so they can actually be
        #     # used for math
        #     for index in range(len(coordinate)):
        #         if index == len(coordinate) - 1:
        #             float_temp = float(temp)
        #             temp = ''
        #             coord_floats.append(float_temp)
        #         #     end point check & does same thing as comma check
        #         elif coordinate[index] != ",":
        #             temp += coordinate[index]
        #         #     building temp
        #         elif coordinate[index] == ",":
        #             float_temp = float(temp)
        #             temp = ''
        #             coord_floats.append(float_temp)
        #         #     comma means end of coordinate so built temp is converted to float and added to array of float
        # print("coord_floats: " + str(coord_floats))
        # # currently a bit of a mess when it does like a lot of people at the same time & no center point yet

        msg.data = []

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing coordinates')

def main(args=None):
	rclpy.init(args=args)
	coord_pub = coordPub()
	rclpy.spin(coord_pub)
	coord_pub.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
   		 main()









