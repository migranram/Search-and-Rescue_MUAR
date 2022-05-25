#include <ros/ros.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <nav_msgs/Odometry.h>

std::string turtle_name;
int i;
void poseCallback(const nav_msgs::Odometry::ConstPtr& msg){
    static tf2_ros::TransformBroadcaster br;
    geometry_msgs::TransformStamped transformStamped;

    transformStamped.header.stamp = ros::Time::now();
    //transformStamped.header.stamp = msg->header.stamp;
    transformStamped.header.frame_id = "odom";
    transformStamped.child_frame_id = "base_footprint";
    transformStamped.header.seq = i;
    ++i;
    transformStamped.transform.translation.x = msg->pose.pose.position.x;
    transformStamped.transform.translation.y = msg->pose.pose.position.y;
    transformStamped.transform.translation.z = 0.0;
    //tf2::Quaternion q;
    //q.setRPY(0, 0, msg->theta);
    transformStamped.transform.rotation.x = msg->pose.pose.orientation.x;
    transformStamped.transform.rotation.y = msg->pose.pose.orientation.y;
    transformStamped.transform.rotation.z = msg->pose.pose.orientation.z;
    transformStamped.transform.rotation.w = msg->pose.pose.orientation.w;

    br.sendTransform(transformStamped);
}
void chatterCallback(const nav_msgs::Odometry::ConstPtr& msg)
{
    ROS_INFO("Seq: [%d]", msg->header.seq);
    ROS_INFO("Position-> x: [%f], y: [%f], z: [%f]", msg->pose.pose.position.x,msg->pose.pose.position.y, msg->pose.pose.position.z);
    ROS_INFO("Orientation-> x: [%f], y: [%f], z: [%f], w: [%f]", msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
    ROS_INFO("Vel-> Linear: [%f], Angular: [%f]", msg->twist.twist.linear.x,msg->twist.twist.angular.z);
}
int main(int argc, char** argv){
  ros::init(argc, argv, "tf2_odom_broadcaster");
  i = 0;
  ros::NodeHandle node;
  ros::Subscriber sub = node.subscribe("/odom", 1000, &poseCallback);
  
   ros::spin();
   return 0;
};