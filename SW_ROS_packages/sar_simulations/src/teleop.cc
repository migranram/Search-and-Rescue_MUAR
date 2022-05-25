#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <signal.h>
#include <termios.h>
#include <stdio.h>

#define KEYCODE_R 0x43 
#define KEYCODE_L 0x44
#define KEYCODE_U 0x41
#define KEYCODE_D 0x42
#define KEYCODE_Q 0x71
#define KEYCODE_E 0x65

struct termios cooked, raw;
int kfd = 0;

void quit(int sig)
{
  tcsetattr(kfd, TCSANOW, &cooked);
  ros::shutdown();
  exit(0);
}

int main(int argc, char** argv)
{
  char c;
  ros::init(argc, argv, "sar_teleop");
  ros::NodeHandle nh;

  signal(SIGINT,quit);

  ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 1);
  ros::Rate loop_rate(100);

  tcgetattr(kfd, &cooked);
   memcpy(&raw, &cooked, sizeof(struct termios));
   raw.c_lflag &=~ (ICANON | ECHO);
   // Setting a new line, then end of file                         
   raw.c_cc[VEOL] = 1;
   raw.c_cc[VEOF] = 2;
   tcsetattr(kfd, TCSANOW, &raw);
 
   puts("Reading from keyboard");
   puts("---------------------------");
   puts("Use arrow keys to move the turtle.");

  double multiplier;
   if (nh.getParam("vel_mult", multiplier))
    {
      ROS_INFO("Got vel multiplier: %f", multiplier);
    }
    else
    {
      ROS_INFO("Failed to get param 'vel_multiplier'. Set to default: 3.0");
      multiplier = 3.0;
    }

  while(ros::ok()){
    if(read(kfd, &c, 1) < 0)
     {
       perror("read():");
       exit(-1);
     }
    geometry_msgs::Twist msg;
    bool dirty= false;
    double angular, side, forward;
    angular = side = forward = 0;
    ROS_DEBUG("value: 0x%02X\n", c);
    switch(c)
     {
       case KEYCODE_L:
         ROS_DEBUG("LEFT");
         side = 1.0;
         dirty = true;
         break;
       case KEYCODE_R:
         ROS_DEBUG("RIGHT");
         side = -1.0;
         dirty = true;
         break;
       case KEYCODE_U:
         ROS_DEBUG("UP");
         forward = 1.0;
         dirty = true;
         break;
       case KEYCODE_D:
         ROS_DEBUG("DOWN");
         forward = -1.0;
         dirty = true;
         break;
      case KEYCODE_Q:
         ROS_DEBUG("Q");
         angular = 1.0;
         dirty = true;
         break;
        case KEYCODE_E:
         ROS_DEBUG("E");
         angular = -1.0;
         dirty = true;
         break;
     }
    

    // Write message
    msg.angular.x = 0.0;
    msg.angular.y = 0.0;
    msg.angular.z = angular*multiplier;

    msg.linear.x = forward*multiplier;
    msg.linear.y = side*multiplier;
    msg.linear.z = 0.0;

    ros::spinOnce();
    loop_rate.sleep();

      if(dirty ==true)
     {
       pub.publish(msg);   
       dirty=false;
     }

  }
}
// %EndTag(MAIN)%
// %EndTag(FULL)%