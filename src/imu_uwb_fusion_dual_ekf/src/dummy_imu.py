#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose

pub1= rospy.Publisher('imu/dummy_data',Imu,queue_size=1)
pub2= rospy.Publisher('odometry/uwb',Odometry,queue_size=1)
uwb=Odometry()
imu=Imu()
def callback1(data):
    global imu
    imu=data
    imu.header.frame_id="base_link"
    imu.header.stamp=rospy.Time.now()
    pub1.publish(imu)

def callback2(data):
    global uwb
    uwb.pose.pose=data
    uwb.header.stamp=rospy.Time.now()
    uwb.header.frame_id="map"
    pub2.publish(uwb)

if __name__ == '__main__':
    try:
        rospy.init_node('dummy_topic', anonymous=True)
    	rospy.Subscriber('imu/data', Imu, callback1)
        rospy.Subscriber('tag_11', Pose, callback2)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
        #     # imu.header.frame_id="base_link"
        #     # imu.header.stamp=rospy.Time.now()
        #     # uwb.header.stamp=rospy.Time.now()
        #     # uwb.header.frame_id="map"
        #     pub1.publish(imu)
        #     pub2.publish(uwb)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
