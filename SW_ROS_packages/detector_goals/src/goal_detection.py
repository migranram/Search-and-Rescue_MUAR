#!/usr/bin/env python

import rospy

from sensor_msgs.msg import Image
from actionlib_msgs.msg import GoalID
from cv_bridge import CvBridge
from move_base_msgs.msg import MoveBaseActionGoal
from detector_goals.srv import Mision
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from random import randint
from std_msgs.msg import Int16MultiArray
import geometry_msgs.msg
import actionlib
import cv2
import tf
import os
import numpy as np
import time



class Nodo(object):
    def __init__(self, x, y, angle, identifier_aruco):
       self.x = 0
       self.image = None
       self.br = CvBridge()
       self.id_aruco = identifier_aruco
       self.loop_rate = rospy.Rate(1)
       self.aruco_detected = 0
       
       
       # Publishers
       self.cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=1)
       self.cancel_msg = GoalID()
       self.waypoints_counter = 0
       
       #  Subscribers, este subscriptor debe ser al chatter, mirar el mensaje que tienes que 	tener ahi
       #Lo que debería de estar
       #rospy.Subscriber("/chatter", Int16MultiArray ,self.check_aruco_detected)
       rospy.Subscriber("/camera/rgb/image_raw",Image,self.check_aruco_detected)
       moveResult = self.publishMoveBaseGoalWaitForReply( x, y, angle, "waypoint %d" % \
        (self.waypoints_counter))
       self.start()
	
    def publishMoveBaseGoalWaitForReply(self, x, y, yaw, comment): 
    
    	# Creamos el mensaje move_base
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

  	# Esto no es necesario porque estamos en 2D pero bueno
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
    
    def check_aruco_detected(self, msg):
    #Incluir codigo que detecte en función de lo que me pasa el servicio ver si se ha encontrado el Aruco
        #TODO
        # msg_listed = list(msg)
        # if self.id_aruco ==  msg_listed.index(1)
        	#self.aruco_detected = 1
        self.image = self.br.imgmsg_to_cv2(msg)
    		
    def start(self): 
        #rospy.spin()
        while not rospy.is_shutdown():
            if self.aruco_detected == 0:
                x = randint(0,10)
                y = randint(0,10)
                angle = randint(0,1)
                moveResult = self.publishMoveBaseGoalWaitForReply( x, y, angle, "waypoint %d"   % \
                 (self.waypoints_counter))
                 
            #Si es mayor que 119000 aruco_detected esto es un atajo para el video		
            #Aqui está claro que tienes que poner la variable que te dice si ha detectado el Aruco	    elif self.aruco_detected == 1:
                #rospy.loginfo("ARUCO detected, mission SAR completed")
            	#self.cancel_pub.publish(self.cancel_msg)
            	break
            if self.x > 2343412312:
            	rospy.loginfo("ARUCO detected, mission SAR completed")
            	self.cancel_pub.publish(self.cancel_msg)
            	self.aruco_detected = 1
            	break		
            print(self.x)
            self.x = 0
            self.loop_rate.sleep()
            

		
	
def start_mision(mision):
	my_node = Nodo(mision.x,mision.y,mision.angle, mision.id_aruco)
	rospy.loginfo("Beginning the mission")
	

if __name__ == '__main__':
    rospy.init_node("goal_searcher", anonymous=True)
    service = rospy.Service("/sar_service", Mision, start_mision)
    rospy.loginfo("Service server has been started")
    rospy.spin()
    
