#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
pub= rospy.Publisher('imu/dummy_data',Imu,queue_size=1)
imu=Imu()
def callback(data):
    global imu
    imu=data
if __name__ == '__main__':
    try:
        rospy.init_node('imu_dummy_topic', anonymous=True)
    	rospy.Subscriber('imu/data', Imu, callback)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
	    imu.header.frame_id="base_link"
	    # imu.header.stamp=rospy.Time.now()
	    pub.publish(imu)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
