import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import random

class NodeB(Node):
    def __init__(self):
        super().__init__('nodo_b')
        self.publisher_ = self.create_publisher(Float64, 'sensor_2', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.valor = 2.0

    def timer_callback(self):
        msg = Float64()
        msg.data = random.uniform(1, 10)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Node B publicó: {msg.data}')
        self.valor += 0.2

def main(args=None):
    rclpy.init(args=args)
    node = NodeB()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()