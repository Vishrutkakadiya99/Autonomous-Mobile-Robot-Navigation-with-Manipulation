from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 1. Start the Gazebo World with the TurtleBot3 + Arm
    tb3_manipulation_gazebo_dir = get_package_share_directory('turtlebot3_manipulation_gazebo')
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_manipulation_gazebo_dir, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Start Nav2 for Mobile Base Navigation
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
    )

    # 3. Start MoveIt2 for Arm Manipulation
    tb3_manipulation_moveit_config_dir = get_package_share_directory('turtlebot3_manipulation_moveit_config')
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_manipulation_moveit_config_dir, 'launch', 'move_group.launch.py')
        )
    )

    # 4. Start your custom Hybrid Controller Node
    hybrid_controller_node = Node(
        package='tb3_hybrid_control',
        executable='hybrid_controller',
        name='hybrid_controller',
        output='screen',
        parameters=[os.path.join(get_package_share_directory('tb3_hybrid_control'), 'config', 'arm_target.yaml')],
    )

    return LaunchDescription([
        gazebo_launch,
        nav2_launch,
        moveit_launch,
        hybrid_controller_node,
    ])
