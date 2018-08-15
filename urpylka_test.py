#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.Subscriber("beacons_pos_a", TOPIC_MESSAGE_TYPE_POSE_PX4, callback2)
# http://wiki.ros.org/mavros#mavros.2BAC8-Plugins.Published_Topics-3
# https://clever.copterexpress.com/mavros.html

# local_position/pose

rospy.Subscriber("beacons_pos_a", TOPIC_MESSAGE_TYPE_BEACON, callback)
pub = rospy.Publisher('mocap_pose_estimate', TOPIC_MESSAGE_TYPE_MOCAP)

def callback(msg):
    rospy.loginfo("I heard %s", msg.data)
    TOPIC_MESSAGE_MOCAP = ваш алгоритм для обработки msg.data
    pub.publish(TOPIC_MESSAGE_MOCAP)

def talker():
    
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
 
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


