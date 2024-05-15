import sys
import os
import cv2
import numpy as np
import rclpy
import numpy as np
import pyrealsense2 as rs2
from ultralytics import YOLO
from roboflow import Roboflow
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image as msg_Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError

model = YOLO("yolov8n")

class coordPub(Node): 
    def __init__(self):
        super().__init__('coord_pub')
        self.publisher_ = self.create_publisher(Int32MultiArray, 'targetCoords', 10)
        self.rgb_sub = self.create_subscription(msg_Image,'/camera/color/image_raw',self.rgb_callback,10)
        self.rgb_depth = self.create_subscription(msg_Image,'/camera/depth/image_rect_raw',self.depth_callback,10)
        self.rgb_info = self.create_subscription(CameraInfo,'/camera/depth/camera_info',self.info_callback,10)
        self.last_rgb = None
        self.last_depth = None
        self.last_info = None
        self.intrinsics = None
        self.timer_period = 1.0
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
    def rgb_callback(self, msg):
        self.last_rgb = msg
    def depth_callback(self, msg):
        self.last_depth = msg
    def info_callback(self, msg):
        self.last_info = msg
    def timer_callback(self):
        # Set camera info
        try:
            if self.intrinsics:
                return
            self.intrinsics = rs2.intrinsics()
            self.intrinsics.width = self.last_info.width
            self.intrinsics.height = self.last_info.height
            self.intrinsics.ppx = self.last_info.K[2]
            self.intrinsics.ppy = self.last_info.K[5]
            self.intrinsics.fx = self.last_info.K[0]
            self.intrinsics.fy = self.last_info.K[4]
            if self.last_info.distortion_model == 'plumb_bob':
                self.intrinsics.model = rs2.distortion.brown_conrady
            elif self.last_info.distortion_model == 'equidistant':
                self.intrinsics.model = rs2.distortion.kannala_brandt4
            self.intrinsics.coeffs = [i for i in self.last_info.D]
        except CvBridgeError as e:
            print(e)
            return

        # Run model to extract x and y values from RGB
        results = model.predict(source=self.last_rgb, classes=[0])
        data = results[0].boxes[0].xywh.numpy()
        xy = data[0,0:2]

        # Pull depth data at the specific x and y
        depth_image = self.bridge.imgmsg_to_cv2(self.last_depth, self.last_depth.encoding)
        depth = depth_image[xy[0],xy[1]]

        # Translate from x, y, depth to xyz in 3D space
        if self.intrinsics:
            result = rs2.rs2_deproject_pixel_to_point(self.intrinsics, [xy[0], xy[1]], depth)

        # Publish coordinates
        msg = Int32MultiArray
        msg.data = result
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