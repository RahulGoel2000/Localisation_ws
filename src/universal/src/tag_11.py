#! /usr/bin/env python
import paho.mqtt.client as mqtt
import ssl
import json
import rospy
from geometry_msgs.msg import Pose

host = "mqtt.cloud.pozyxlabs.com"
port = 443
topic = "5f07680e66f23b6fe65dbac9"  # your mqtt topic
username = "5f07680e66f23b6fe65dbac9"  # your mqtt username
password = "7dd561bf-5d4e-49df-83f7-578bd9c2b994"  # your generated api key

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    num_of_tags = len(json.loads(msg.payload.decode()))
    data = json.loads(msg.payload.decode())
    rospy.init_node("tags", anonymous=True)
    print("Total Tags found :", num_of_tags)
    print("Total Tags data found :", data)
    for x in range(num_of_tags):
        if "coordinates" in data[x]["data"]:
            id_n = data[x]['tagId']
            print(id_n)
            id_name = rospy.Publisher(id_n, Pose, queue_size=10 )
            p = Pose()
            p.position.x = data[x]["data"]["coordinates"]["x"]
            p.position.y = data[x]["data"]["coordinates"]["y"]
            p.position.z = data[x]["data"]["coordinates"]["z"]
            if "quaternion" in data[x]["data"]:
                p.orientation.x = data[x]["data"]["tagData"]["quaternion"]["x"]
                p.orientation.y = data[x]["data"]["tagData"]["quaternion"]["y"]
                p.orientation.z = data[x]["data"]["tagData"]["quaternion"]["z"]
                p.orientation.w = data[x]["data"]["tagData"]["quaternion"]["w"]
            id_name.publish(p)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

client = mqtt.Client(transport="websockets")
client.username_pw_set(username, password=password)
client.tls_set_context(context=ssl.create_default_context())
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)
client.loop_forever()