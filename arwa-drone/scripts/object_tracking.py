#!/usr/bin/env python

import rospy
from darknet_ros_msgs.msg import BoundingBoxes, BoundingBox
from sensor_msgs.msg import NavSatFix
from visualization_msgs.msg import MarkerArray, Marker
from std_msgs.msg import String

VALID_CLASS = ["person", "cat", "bird", "dog", "horse", "sheep", "cow", \
                "elephant", "bear", "zebra", "giraffe"]

markersPublisher = None
lastGpsPos = None
detections = []
index = 0

class ObjectDetected:
    gps = None
    bounding_box = None

    def __init__(self, gps, bounding_box):
        self.gps = gps
        self.bounding_box = bounding_box

def publishMarker(boundingBox):
    global index
    if lastGpsPos is None:
        return

    index += 1
    m = Marker()
    m.header.frame_id = "wgs84";
    m.header.frame_id = "map";
    m.header.stamp = rospy.Time();
    m.ns = "objects"
    m.id = index
    m.type = Marker.CUBE
    m.action = Marker.ADD
    m.pose.position.x = lastGpsPos.longitude
    m.pose.position.y = lastGpsPos.latitude
    m.pose.position.z = lastGpsPos.altitude
    m.pose.orientation.x = 0.0
    m.pose.orientation.y = 0.0
    m.pose.orientation.z = 0.0
    m.pose.orientation.w = 1.0
    m.scale.x = 10
    m.scale.y = 10
    m.scale.z = 10
    m.color.a = 1.0
    m.color.r = 0.0;
    m.color.g = 1.0;
    m.color.b = 0.0;
    markersPublisher.publish(m)

def callbackGps(data):
    global lastGpsPos
    rospy.loginfo("Callback GPS!")
    lastGpsPos = data

def callbackYolo(data):
    global markersPublisher
    rospy.loginfo("Callback Yolo!")
    filtered_data = filter(lambda e: e.Class in VALID_CLASS, data.bounding_boxes)
    rospy.loginfo(filtered_data)
    rospy.loginfo(data.bounding_boxes)
    for bb in filtered_data:
        # publishMarker(bb)
        detections.append(ObjectDetected(lastGpsPos, bb))
    publishMarkers()

def tracker():
    global markersPublisher
    rospy.init_node('arwa_tracker')
    sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callbackYolo)
    markersPublisher = rospy.Publisher('life', Marker, latch=True)
    rospy.loginfo("Initialized")
    rospy.loginfo("Filtering following classes: " + str(VALID_CLASS))
    publishMarker(None)
    # publishMarker(None)
    # publishMarker(None)
    # publishMarker(None)
    # publishMarker(None)
    # pub.publish("Hola")
    # pub.publish("Hola")
    # pub.publish("Hola")
    # pub.publish("Hola")
    # pub.publish("Hola")
    # pub.publish("Hola")
    rospy.spin()
    # rate = rospy.Rate(10) # 10hz
    # while not rospy.is_shutdown():
    #     hello_str = "hello world %s" % rospy.get_time()
    #     rospy.loginfo(hello_str)
    #     pub.publish(hello_str)
    #     rate.sleep()

if __name__ == '__main__':
    try:
        tracker()
    except rospy.ROSInterruptException:
        pass
