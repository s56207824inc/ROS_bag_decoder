import rosbag
import sensor_msgs.point_cloud2 as pc2
import numpy as np
import os
import glob
import cv2
from cv_bridge import CvBridge


def pt_decoder(bag, output_dir):
    
    pt_output = os.path.join(output_dir, 'velodyne')

    if not os.path.isdir(pt_output):
        os.makedirs(pt_output)
        
    # your targeted topic
    bag_data = bag.read_messages('/points_raw')
    frame = 0

    for topic, msg, t in bag_data:
        # save index
        index = '%006d' % frame + '.bin'
        #read ros format 
        lidar = pc2.read_points(msg)
        # convert into np format
        points = np.array(list(lidar), dtype=np.float32).reshape(-1, 9)
        points = points[:, 0:4]
        save_name = os.path.join(pt_output, index)
        print(save_name)
        points.tofile(save_name)
        frame+=1
        
    print("total frame:{}".format(frame))

def Img_decoder(bag, output_dir):
    
    img_output = os.path.join(output_dir, 'image_2')

    if not os.path.isdir(img_output):
        os.makedirs(img_output)

    bridge = CvBridge()
    # your targeted topic
    bag_data = bag.read_messages('/cameraF16/image_raw')
    frame = 0

    for topic, msg, t in bag_data:
        # save index
        index = '%006d' % frame + '.png'
        # convert into cv2 img format
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        save_name = os.path.join(img_output, index)
        cv2.imwrite(save_name, cv_image)
        print(frame)
        frame+=1

    print("total frame:{}".format(frame))