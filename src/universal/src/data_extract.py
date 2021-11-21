#!/usr/bin/env python
import socket, traceback
# import tf
import rospy
import time
from datetime import datetime

from std_msgs.msg import Header
from sensor_msgs.msg import Imu, MagneticField, NavSatFix


def data_imu_to_msg(LIST_DATA):
    global accelerometer_x, accelerometer_y, accelerometer_z,gyroscope_x, gyroscope_y, gyroscope_z,magnetic_x, magnetic_y, magnetic_z, gps_lat, gps_lon, gps_alt


    accelerometer_data = LIST_DATA[2:5]
    for idx, acc in enumerate(accelerometer_data):
        accelerometer_data[idx] = float(acc.strip()[:-1])
    accelerometer_x, accelerometer_y, accelerometer_z = accelerometer_data

    gyroscope_data = LIST_DATA[6:9]
    for idx, gyro in enumerate(gyroscope_data):
        gyroscope_data[idx] = float(gyro.strip()[:-1])
    gyroscope_x, gyroscope_y, gyroscope_z = gyroscope_data

    magnetic_data = LIST_DATA[10:13]
    for idx, magneto in enumerate(magnetic_data):
        magnetic_data[idx] = float(magneto.strip()[:-1])
    magnetic_x, magnetic_y, magnetic_z = magnetic_data
    # print(magnetic_x)

    gps_data = LIST_DATA[14:17]
    for idx, gpso in enumerate(gps_data):
        gps_data[idx] = float(gpso.strip()[:-1])
    gps_lat, gps_lon, gps_alt = gps_data




def convert_to_msg():
    
    # print("hi im here")
    # rospy.init_node('mobile_read', anonymous=True)
    pub = rospy.Publisher('imu/data_raw', Imu, queue_size=10)
    pub2=rospy.Publisher('imu/mag',MagneticField, queue_size=10 )
    pub3=rospy.Publisher('gps/fix',NavSatFix, queue_size=10 )
    rate = rospy.Rate(10) # 10hz
    # while not rospy.is_shutdown():
    
    imu = Imu()
    # imu.header=Header()
    mag=MagneticField()
    gps=NavSatFix()
    imu.header.stamp=rospy.Time.now()
    mag.header.stamp=rospy.Time.now()
    gps.header.stamp=rospy.Time.now()
    imu.header.frame_id="odom"
    mag.header.frame_id="odom"
    gps.header.frame_id="earth"

    # header = Header()
    # header.stamp = rospy.Time.now()
    # # header.frame_id = self._frame_id
    #imu.header = header
    # imu.header.stamp=rospy.Time.from_sec(float(time.strftime("%s.%f")))
    # print("\n\n\n\n\n")
    # print(type(rospy.Time.now()))
    # print("\n\n\n\n\n")
    imu.linear_acceleration.y = accelerometer_x
    imu.linear_acceleration.x = accelerometer_y
    imu.linear_acceleration.z = accelerometer_z
    imu.angular_velocity.x = gyroscope_x
    imu.angular_velocity.y = gyroscope_y
    imu.angular_velocity.z = gyroscope_z    
    mag.magnetic_field.x=magnetic_x
    mag.magnetic_field.y=magnetic_y
    mag.magnetic_field.z=magnetic_z
    gps.latitude=gps_lat
    gps.longitude=gps_lon
    gps.altitude=gps_alt

    # gps.latitude=27.2046
    # gps.longitude=77.4977
    # gps.altitude=gps_alt
    # rospy.loginfo(imu)
    rospy.loginfo(gps)
    # rospy.loginfo(mag)
    pub.publish(imu)
    pub2.publish(mag)
    pub3.publish(gps)
    rate.sleep()
    # imu = Imu()
    # imu.linear_acceleration.y = accelerometer_x
    # imu.linear_acceleration.x = accelerometer_y
    # imu.linear_acceleration.z = accelerometer_z
    # imu.angular_velocity.x = gyroscope_x
    # imu.angular_velocity.y = gyroscope_y
    # imu.angular_velocity.z = gyroscope_z


host = '172.17.18.202'
port = 5555
rospy.init_node('mobile_read', anonymous=False)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
while 1:
    try:
        message, address = s.recvfrom(8192)
        print (message)
        LIST_DATA = str(message).split(",")
        rcvd_length = len(LIST_DATA)
        # print(rcvd_length)
        if(rcvd_length>13):
            # print(LIST_DATA)
            data_imu_to_msg(LIST_DATA)
            convert_to_msg()
            # print(LIST_DATA[10:13])
            # print(magnetic_x)
            # print("\n\n\n\n")
        # except (KeyboardInterrupt, SystemExit):
        # raise
        # except:
        # traceback.print_exc()
    except:
        pass
