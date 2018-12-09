cmake_minimum_required(VERSION 2.8.3)
project(birl_trajectory_planner)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  trajectory_msgs
  std_msgs
)

catkin_python_setup()
catkin_python_setup()

catkin_package(
 CATKIN_DEPENDS trajectory_msgs  std_msgs )

 include_directories(
  ${catkin_INCLUDE_DIRS}
)