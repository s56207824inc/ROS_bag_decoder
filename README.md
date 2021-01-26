# ROS_bag_decoder
---
## impelement
this repo impelement a extractor can extract data
(ex. images, point cloud) from .bag file
# 

## environment requirement

* ROS

## rosbag decode procedures

### First.
to see which is your targeted signal
```bash=
rosbag info YOUR-ROS-FIlE
```
#### ex. ![Ouster-128 Beams](https://i.imgur.com/c4lZHcP.png)
#  
take this ouster-128 beam for ex. if your targeted signal is point cloud, you should choice "/points_raw" this topic

### Second.

customize your code base on script rosbag_decoder.py

#### 1. setting up your output path
#### 2. replace "/points_raw" on the 9th line with your own topic name 

```python=
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

```
## NOTE
---
There is an example for images and point cloud decode function in that python script and don't forget to import the necessary lib in the first