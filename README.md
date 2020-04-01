# ARWA Project
## Install
```bash
# Clone repo in git folder inside home
cd ~/git
git clone --recursive https://github.com/turing-lab/arwa-drone.git

# create a symbolic link to catkin_ws
ln -s ~/git/arwa-drone ~/catkin_ws/src

# Change directory to catkin_ws, install dependencies and compile
cd ~/catkin_ws
rosdep install --from-paths src/ --ignore-src -y
catkin build
```

## Download weights
```bash
wget http://pjreddie.com/media/files/yolov3-tiny.weights -P darknet_ros/darknet_ros/yolo_network_config/weights/
```
