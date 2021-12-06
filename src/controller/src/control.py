from std_msgs.msg import Float64
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import rospy
from std_msgs.msg import Int32MultiArray
import numpy as np
import math
from math import *
from datetime import datetime





class Server:
    def _init_(self):
        self.x_vehicle = 0
        self.x_follow1 = 0

        self.y_vehicle = 0
        self.y_follow1 = 0

        self.xx = 0
        self.yy = 0

        self.heading = 0
        self.key = 0
        self.counter=1

    def orientation_callback(self, msg):
        self.x_vehicle = msg.position.x
        self.y_vehicle = msg.position.y
        self.heading = msg.orientation.x

        if self.counter == 2.0:
            self.xx = self.x_follow1
            self.yy = self.y_follow1

        else:
            self.xx = self.x_vehicle
            self.yy = self.y_vehicle

        dist, angle = server.calculator()
        # if self.counter == 1:
        #     voice.publish(881)
        #     # speak("Finding Tag 1")
        # elif self.counter == 3:
        #     voice.publish(992)
        #     # speak("Found Tag 1")
        # else: 
        #     pass 
            
        t = Twist()
        if dist > 50:
            cal_dist.publish(dist)
            cal_angle.publish(angle)
            t.linear.x = 50
            t.angular.z = -angle
            pub.publish(t)
            print(50)
            print(angle)
        else:
            self.counter = self.counter + 1
            cal_dist.publish(0)
            cal_angle.publish(0)
            t.linear.x = 0
            t.angular.z = 0
            pub.publish(t)

        
        

    def tag1_callback(self, msg):
        # "Store" the message received.
        self.x_follow1 = msg.position.x
        self.y_follow1 = msg.position.y


    def key_callback(self,msg):
        self.key =  msg.data
        if self.key == 1.0:
            self.counter = 1.0
        else: 
            self.counter = 4.0



    def calculator(self):
        a = np.array([0, 0])
        a.reshape(2,1)

        x = (self.xx - self.x_vehicle)
        y = (self.yy - self.y_vehicle)

        dist = math.sqrt((y*2) + (x*2))
        dist = np.round(dist)

        # angle = atan2(y, x)
        # final_angle = round(math.degrees(angle))

        # # now = datetime.now()
        # # current_time = now.strftime("%H:%M:%S%f")[:-5] 

        # t_angle = -1*round(self.heading - final_angle)

        phidesired = math.atan2((self.yy-self.y_vehicle),(self.xx -self.x_vehicle))
        temp = phidesired - radians(self.heading)    
        error_heading = degrees(round((math.atan2(math.sin(temp), math.cos(temp))), 4))


        # alpha = (90 - t_angle)
        # alpha = math.radians(alpha)
        # x_cor = (dist * math.cos(alpha))
        # y_cor = dist * math.sin(alpha)

        # print("Time is", current_time)
        # print("angle with car     " , final_angle)
        # print("heading            ", round(self.heading)) 
        # print("difference         ", t_angle)
        # print("phidesired         ", phidesired)
        # print("error heading      ", error_heading)
        print("E Distance         ", dist)
        # print("x", x_cor)
        # print("y", y_cor)
        print("counter", self.counter)
        
        print("    ")
        # print("    ")
        return dist, error_heading


if __name__ == '_main_':

    server = Server()
    rospy.init_node('calculator')

    cal_dist = rospy.Publisher('/cal_dist', Float64, queue_size=10)
    cal_angle = rospy.Publisher('/cal_angle', Float64, queue_size=10)
    throttle = rospy.Publisher('/arduino_throttle', Int32,queue_size=10)
    # voice = rospy.Publisher('/voice', Float64, queue_size=10)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    rospy.Subscriber("/30283", Pose, server.orientation_callback)
    rospy.Subscriber("/1", Pose, server.tag1_callback)
    rospy.Subscriber("/key", Float64, server.key_callback)

    rate = rospy.Rate(10)
    rospy.spin()