#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from marvelmind_nav.msg import hedge_pos

global pub
pub = rospy.Publisher("mavros/mocap/pose", PoseStamped, queue_size = 1)
global pose
pose = PoseStamped()
pose.header.frame_id = "local_origin"

def callback(data):
    pose.header.stamp = rospy.get_rostime()
    pose.pose.position.x = data.x_m
    pose.pose.position.y = data.y_m
    pose.pose.position.z = data.z_m
    pose.pose.orientation.w = 1
    print pose
    pub.publish(pose)

def listener():
    rospy.init_node("hdg_in", anonymous=True)
    rospy.Subscriber("hedge_pos", hedge_pos, callback)
    rospy.spin()

if __name__ == "__main__":
    listener()
