#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from actionlib_msgs.msg import GoalID
from cv_bridge import CvBridge
from move_base_msgs.msg import MoveBaseActionGoal

import geometry_msgs.msg
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from random import randint
import cv2
import tf
import os
import numpy as np
import time
import threading

class Nodo(object):
    def __init__(self):
        # Params
       self.x = 0
       self.image = None
       self.br = CvBridge()
       self.loop_rate = rospy.Rate(1)
       #self.goal_publisher = rospy.Publisher("move_base/goal", PoseStamped, queue_size=10)
       self.aruco_detected = 0
       # Publishers
       self.cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=1)
       self.cancel_msg = GoalID()
       self.waypoints_counter = 0
       #  Subscribers, este subscriptor debe ser al chatter, mirar el mensaje que tienes que tener ahi
       rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)
       #self.publish_goals(pose_x=1, pose_y=2)
       x = randint(0,10)
       y = randint(0,10)
       angle = randint(0,1)
       moveResult = self.publishMoveBaseGoalWaitForReply( x, y, angle, "waypoint %d" % \
        (self.waypoints_counter))
	
    #def publish_goals(self, pose_x, pose_y):3, 5, 0.4
    def publishMoveBaseGoalWaitForReply(self, x, y, yaw, comment):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

       
        x , y, z, w = tf.transformations.quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation.x = x
        goal.target_pose.pose.orientation.y = y
        goal.target_pose.pose.orientation.z = z
        goal.target_pose.pose.orientation.w = w
        now = rospy.get_rostime()
        print ("[%i.%i] PubMove: %s x,y,z,w of %f %f %f %f yaw %f" % \
         (now.secs,now.nsecs,comment,x,y,z,w,yaw))

        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

  
        client.send_goal(goal)

        now = rospy.get_rostime()
    # Este callback tiene que ser suscrito a chatter
    def callback(self, msg):
        
        self.image = self.br.imgmsg_to_cv2(msg)

    def start(self):
     
        #rospy.spin()
        while not rospy.is_shutdown():
            print("hola")
            #br = CvBridge()
            if self.aruco_detected == 0:
                x = randint(0,10)
                y = randint(0,10)
                angle = randint(0,1)
                moveResult = self.publishMoveBaseGoalWaitForReply( x, y, angle, "waypoint %d"   % \
                 (self.waypoints_counter))
            #Si es mayor que 119000 aruco_detected esto es un atajo para el video		
            #Aqui está claro que tienes que poner la variable que te dice si ha detectado el Aruco
            if self.x > 2343412312:
            	rospy.loginfo("ARUCO detected, mission SAR completed")
            	self.cancel_pub.publish(self.cancel_msg)
            	self.aruco_detected = 1
            	break		
            print(self.x)
            self.x = 0
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node("imagetimer111", anonymous=True)
    my_node = Nodo()
    my_node.start()
