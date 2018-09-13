#!/usr/bin/env python
import rospy
from math import atan2
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Imu
from marvelmind_nav.msg import hedge_pos
from tf.msg import tfMessage
from tf.transformations import quaternion_from_euler

global prev
prev = [0, 0, 0, 0, 0, 0, 0]

global pub
pub = rospy.Publisher("mavros/vision_pose/pose", PoseStamped, queue_size = 1)
global pose
pose = PoseStamped()
pose.header.frame_id = "local_origin"

global imu_data
imu_data = [0, 0, 0]

def callback1(data):
    imu_data[0] = data.linear_acceleration.x
    imu_data[1] = data.linear_acceleration.y
    imu_data[2] = data.linear_acceleration.z

def callback(data):
    pose.header.stamp = rospy.get_rostime()

    pX = prev[0]
    pY = prev[1]
    pZ = prev[2]
    pT = prev[6]
    pVX = prev[3]
    pVY = prev[4]
    pVZ = prev[5]

    cX = data.x_m
    cY = data.y_m
    cZ = 0
#    cZ = data.z_m
    cT = data.timestamp_ms
    dT = cT - pT
    if not dT == 0:
        vX = (cX - pX) / dT
        vY = (cY - pY) / dT
        vZ = (cZ - pZ) / dT
        aX = (vX - pVX) / dT
        aY = (vY - pVY) / dT
        aZ = (vZ - pVZ) / dT
    else:
        vX = 0
        vY = 0
        vZ = 0
        aX = 0
        aY = 0
        aZ = 0

    t1 = atan2(vY, vX)
    t2 = atan2(vZ, vY)
    t3 = atan2(vX, vZ)

    if vX == 0:
        t1 = 0
        t3 = 0
    if vY == 0:
        t1 = 0
        t2 = 0
    if vZ == 0:
        t2 = 0
        t3 = 0

    #print t1, t2, t3
    q = quaternion_from_euler(t2, t3, t1)
#    q1 = quaternion_from_euler(t5, t6, t4)
    pose.pose.position.x = cX
    pose.pose.position.y = cY
    pose.pose.position.z = cZ
    pose.pose.orientation.x = q[0]
    pose.pose.orientation.y = q[1]
    pose.pose.orientation.z = q[2]
    pose.pose.orientation.w = q[3]

    prev[0] = cX
    prev[1] = cY
    prev[2] = cZ
    prev[3] = vX
    prev[4] = vY
    prev[5] = vZ
    prev[6] = cT

    print aX, aY, aZ
    print imu_data
    
    pub.publish(pose)
    #pub1 = rospy.Publisher("mavros/mocap/pose", PoseStamped, queue_size = 1)
    #pub1.publish(pose)

def listener():
    rospy.init_node("hdg_in", anonymous=True)
    rospy.Subscriber("hedge_pos", hedge_pos, callback)
    rospy.Subscriber("mavros/imu/data_raw", Imu, callback1)
    rospy.spin()


if __name__ == "__main__":
    listener()
