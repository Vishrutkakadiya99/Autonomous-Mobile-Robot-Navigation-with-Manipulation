import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle

# (In a real project, you would also import and set up the MoveIt2 Action Client)
# from moveit_msgs.action import MoveGroup

class HybridController(Node):
    def __init__(self):
        super().__init__('hybrid_controller')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('navigation_goal.x', 0.0),
                ('navigation_goal.y', 0.0),
                ('navigation_goal.yaw', 0.0),
                # ... declare all manipulation_goal parameters ...
            ]
        )
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        # self.moveit_action_client = ActionClient(self, MoveGroup, 'move_group') # Conceptual

        self.get_logger().info('Hybrid Controller Node Initialized. Waiting for Nav2 server...')
        self.nav_action_client.wait_for_server()
        self.get_logger().info('Nav2 server is available. Starting demo.')
        self.start_navigation_phase()


    def start_navigation_phase(self):
        """Sends the navigation goal to the Nav2 stack."""
        goal_msg = NavigateToPose.Goal()

        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = self.get_parameter('navigation_goal.x').get_parameter_value().double_value
        goal_msg.pose.pose.position.y = self.get_parameter('navigation_goal.y').get_parameter_value().double_value
        # Convert yaw to quaternion (simplified, requires full TF2 conversion in reality)
        goal_msg.pose.pose.orientation.w = 1.0 # Placeholder
        
        self.get_logger().info(f'Sending Nav2 goal: x={goal_msg.pose.pose.position.x}, y={goal_msg.pose.pose.position.y}')
        
        # Send goal and set up a callback for the result
        self._send_goal_future = self.nav_action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)


    def goal_response_callback(self, future):
        """Called when the Nav2 server accepts the goal."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Nav2 Goal rejected!')
            return
        
        self.get_logger().info('Nav2 Goal accepted. Waiting for result...')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.navigation_result_callback)


    def navigation_result_callback(self, future):
        """Called when Nav2 finishes navigating."""
        result = future.result().result
        status = future.result().status
        
        if status == ClientGoalHandle.STATUS_SUCCEEDED:
            self.get_logger().info('✅ Navigation SUCCESS! Starting manipulation phase...')
            self.start_manipulation_phase()
        else:
            self.get_logger().error('❌ Navigation FAILED! Status: %d' % status)


    def start_manipulation_phase(self):
        """Placeholder for sending the MoveIt2 goal."""
        self.get_logger().info('** MANIPULATION PHASE STARTED **')
        # In a real setup, this would construct a MoveGroup action goal
        # using the 'manipulation_goal' parameters from the YAML file
        # and send it to the 'move_group' action server.
        # It would then wait for the arm to complete the pick task.
        self.get_logger().info('Simulating arm movement... Completed pick task!')
        rclpy.shutdown() # End the node after the task


def main(args=None):
    rclpy.init(args=args)
    hybrid_controller = HybridController()
    rclpy.spin(hybrid_controller)
    # rclpy.shutdown() # Only shutdown if not already done in the controller

if __name__ == '__main__':
    main()
