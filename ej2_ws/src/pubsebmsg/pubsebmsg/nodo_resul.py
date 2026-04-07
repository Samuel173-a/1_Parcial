import rclpy
from rclpy.node import Node
from interfaz.msg import FilteredSensor  

class NodeResultado(Node):
    def __init__(self):
        super().__init__('nodo_resultado')
        self.sub = self.create_subscription(
            FilteredSensor,           
            '/filtered_sensor',      
            self.callback,
            10
        )

    def callback(self, msg):
        self.get_logger().info(
            f'Resultado recibido → Promedio: {msg.promedio:.2f}, '
            f'A={msg.sensor_1:.2f}, B={msg.sensor_2:.2f}, C={msg.sensor_3:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = NodeResultado()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()