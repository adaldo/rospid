# rospid
A collection of PID controllers for ROS

## Installation

Type this in a terminal.
This should work if you have ROS and `catkin_tools` installed on your computer.

```
cd <your_catkin_workspace>/src
git clone https://github.com/adaldo/rospid
cd <your_catkin_workspace>
catkin build
source devel/setup.bash
```

## Usage

Type this in a terminal.

```
rosrun rospid <controller>.py
```

Replace `<controller>` with the controller that you want to use.
For now, you can only choose `proportional` or `zero`.


## Adding your own controllers using `rospy`

1. Inherit from `abstract.Abstract`.
2. Redefine `control_law` and, if needed, `__init__`.
4. Initiate a ROS node with `rospy.init_node`.
5. Spawn an instance of your child class.
6. Call the `start` method of your object.
