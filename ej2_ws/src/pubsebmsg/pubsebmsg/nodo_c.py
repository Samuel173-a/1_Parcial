import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import random

class NodeC(Node):
    def __init__(self):
        super().__init__('nodo_c')
        self.publisher_ = self.create_publisher(Float64, 'sensor_3', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.valor = 3.0

    def timer_callback(self):
        msg = Float64()
        msg.data = random.uniform(1, 10)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Node C publicó: {msg.data}')
        self.valor += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = NodeC()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()