#! /usr/bin/env python
import rospy                                      # the main module for ROS-python programs
from detector_goals.srv import Mision # we are creating a 'Trigger service'...
                                                  # ...Other types are available, and you can 
def hola(x):
    ''' 
    Callback function used by the service server to process
    requests from clients. It returns a TriggerResponse
    '''
    print(type(x))
    print(x.x)
    print("hola")
    
if __name__ == '__main__':
    rospy.init_node("add_two_ints_server")
    service = rospy.Service("/sar_service", Mision, hola)
    rospy.loginfo("Service server has been started")
    rospy.spin()
