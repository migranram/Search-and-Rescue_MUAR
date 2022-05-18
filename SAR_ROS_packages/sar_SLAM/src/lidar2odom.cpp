#include <ros/ros.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/PoseStamped.h>

std::string turtle_name;
ros::Publisher pub;
int i;

void slam_cb(const geometry_msgs::PoseStamped::ConstPtr& msg){
    nav_msgs::Odometry odom;

    odom.header.frame_id = "odom";
    odom.header.seq = i;
    ++i;
    odom.child_frame_id = "base_footprint";
    odom.header.stamp = ros::Time::now();
    odom.pose.pose = msg->pose;
    pub.publish(odom);
}
void chatterCallback(const nav_msgs::Odometry::ConstPtr& msg)
{
    ROS_INFO("Seq: [%d]", msg->header.seq);
    ROS_INFO("Position-> x: [%f], y: [%f], z: [%f]", msg->pose.pose.position.x,msg->pose.pose.position.y, msg->pose.pose.position.z);
    ROS_INFO("Orientation-> x: [%f], y: [%f], z: [%f], w: [%f]", msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
    ROS_INFO("Vel-> Linear: [%f], Angular: [%f]", msg->twist.twist.linear.x,msg->twist.twist.angular.z);
}
int main(int argc, char** argv){
  ros::init(argc, argv, "lidar2odom");
  i = 0;
  
  ros::NodeHandle node;
  ros::Subscriber sub = node.subscribe("/slam_out_pose", 1000, &slam_cb);
  pub = node.advertise<nav_msgs::Odometry>("/odom_lidar", 1000);
  
   ros::spin();
   return 0;
};