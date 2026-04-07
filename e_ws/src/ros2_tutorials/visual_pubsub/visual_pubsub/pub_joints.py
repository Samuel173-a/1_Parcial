import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pynput import keyboard  

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        
       
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.step = 0.1 

       
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.timer = self.create_timer(0.1, self.publish_joint_states)
        self.get_logger().info('Control por flechas activo. Mueve el robot en RViz.')

    def on_press(self, key):
       
        try:
            if key == keyboard.Key.up:
                self.q2 += self.step
            elif key == keyboard.Key.down:
                self.q2 -= self.step
            elif key == keyboard.Key.left:
                self.q1 += self.step
            elif key == keyboard.Key.right:
                self.q1 -= self.step
        except AttributeError:
            pass

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        
        msg.name = ['q1', 'q2', 'q3'] 
        
        
        msg.position = [self.q1, self.q2, self.q3]

        self.publisher_.publish(msg)
       
        self.get_logger().info(f'Enviando a URDF: q1={self.q1:.2f}, q2={self.q2:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()