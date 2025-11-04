TurtleBot3 Mobile Manipulation (ROS 2 Humble)
**Project Overview: Autonomous Mobile Robot Navigation with Manipulation**

This repository contains the necessary ROS 2 package (`tb3_hybrid_control`) to demonstrate a core concept in robotics: **coordinated mobile manipulation**. The project successfully integrates navigation and precision robotic arm control on a simulated **TurtleBot3 Waffle Pi** equipped with an **OpenMANIPULATOR**.

The primary goal is to execute a full object pick-up task autonomously:

1.  **Navigate:** The mobile base drives from a starting point to a target location (e.g., a table) using **Nav2**.
2.  **Manipulate:** The robotic arm precisely executes a pre-planned motion to pick up a virtual object using **MoveIt2**.
3.  **Coordinate:** A custom Python node sequences these two major tasks. 

### Key Technologies Used

| Technology | Role in Project |
| :--- | :--- |
| **ROS 2 Humble** | The foundational robot operating system. |
| **Gazebo** | The 3D physics simulator for the robot and environment. |
| **Nav2 (Navigation 2)** | Handles path planning, localization, and driving the mobile base. |
| **MoveIt2** | Handles collision-free motion planning and control for the robotic arm. |
| **Rviz2** | Visualization tool for monitoring maps, sensor data, and planned trajectories. |
| **Python** | Used for the custom `hybrid_controller` node that sequences the Nav2 and MoveIt2 actions. |

---

## ⚙️ Setup and Installation

### Prerequisites

This project is tested with the following environment. You must have the core `turtlebot3`, `turtlebot3_manipulation`, `nav2_bringup`, and **`moveit`** packages installed (refer to the official ROBOTIS documentation for the full TurtleBot3 Manipulator setup in ROS 2 Humble).

* **Operating System:** Ubuntu 22.04 LTS
* **ROS 2 Distribution:** Humble Hawksbill

### 1. Create and Configure ROS 2 Workspace

Ensure your workspace is set up correctly and the correct TurtleBot3 model is exported.

```bash
# Create the workspace directory
mkdir -p ~/tb3_ws/src
cd ~/tb3_ws

# Source your ROS 2 environment
source /opt/ros/humble/setup.bash

# Ensure the correct model is set for the manipulator (Waffle Pi)
echo 'export TURTLEBOT3_MODEL=waffle_pi' >> ~/.bashrc
source ~/.bashrc

File/Directory,Description,Customization Notes
launch/full_demo.launch.py,"Orchestrator for starting all necessary ROS 2 services (Gazebo, Nav2, MoveIt2, controller).",Ensure your Nav2 configuration and map paths are correct if you use a custom environment.
tb3_hybrid_control/hybrid_controller.py,The main Python node that implements the state machine using ROS 2 Action Clients to sequentially command the Nav2 and MoveIt2 Action Servers.,"This is the file to modify if you want to add more complex behaviors, like driving to a second location to drop the object."
config/arm_target.yaml,"Defines the specific numerical goal for the navigation pose (x, y, yaw) and the arm end-effector pose (position/orientation).",Crucial: Change these values to define the robot's navigation destination and the object's precise location.
