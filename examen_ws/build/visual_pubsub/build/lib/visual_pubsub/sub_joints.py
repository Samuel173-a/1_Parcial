import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class JointStateSubscriber(Node):

    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)
        
        
        self.d1 = 1.0
        self.a2 = 0.5
        self.a3 = 0.3
        
        
        self.last_print_time = self.get_clock().now()
        self.print_interval = 1.0  

    def listener_callback(self, msg):
        
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.last_print_time).nanoseconds / 1e9

        if elapsed_time < self.print_interval:
            return  

        
        joints = dict(zip(msg.name, msg.position))
        
        if 'q1' in joints and 'q2' in joints and 'q3' in joints:
            q1, q2, q3 = joints['q1'], joints['q2'], joints['q3']

           
            px = math.cos(q1) * (self.a2 * math.cos(q2) + self.a3 * math.cos(q2 + q3))
            py = math.sin(q1) * (self.a2 * math.cos(q2) + self.a3 * math.cos(q2 + q3))
            pz = self.d1 - self.a2 * math.sin(q2) - self.a3 * math.sin(q2 + q3)

            
            self.get_logger().info(
                f'\n--- LECTURA LENTA (1s) ---'
                f'\nÁngulos: q1:{q1:.2f}, q2:{q2:.2f}, q3:{q3:.2f}'
                f'\nEfector Final -> X: {px:.3f}, Y: {py:.3f}, Z: {pz:.3f}'
            )
            self.last_print_time = current_time

def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()