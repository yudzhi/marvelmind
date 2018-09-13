#!/usr/bin/env python
import rospy
import random
import time
from marvelmind_nav.msg import hedge_pos
from math import sin, cos, pi
def talker():
    pub = rospy.Publisher("hedge_pos", hedge_pos, queue_size = 1)
    rospy.init_node("talker", anonymous = True)
    rate = rospy.Rate(10)
    x = 0
    y = 1
    z = 0
    alpha = 0
    beta = 0
    pose = hedge_pos()
    while not rospy.is_shutdown():
        x = cos(alpha)*2
        y = sin(alpha)*2
        z = sin(beta)
        alpha += 0.01
        beta += 0.05
        if alpha >= 2*pi:
            alpha = 0
        if beta >= 2*pi:
            beta = 0

        pose.x_m = x
        pose.y_m = y
        pose.z_m = z
        pose.timestamp_ms = rospy.get_time()*1000

#        print pose
        pub.publish(pose)

        rate.sleep()


if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
