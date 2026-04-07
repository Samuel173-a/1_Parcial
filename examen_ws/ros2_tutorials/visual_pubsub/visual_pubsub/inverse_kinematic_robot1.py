import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import numpy as np
import time


class InverseKinematics(Node):

    def __init__(self):
        super().__init__('inverse_kinematics')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.target_sub = self.create_subscription(Point, 'target_position',
                                                   self.target_callback, 10)

        # Angulos iniciales ///
        self.q = np.array([-0.22, 0.7, 0.03])  

        # parametros y limites del robot ///
        self.l1 = 3
        self.l2 = 1.5
        self.l3 = 1.5

        #limites articulares
        self.q_min = np.array([-3.14, -1.57, -1.57])
        self.q_max = np.array([3.14, 1.57, 1.57])
        
        self.timer = self.create_timer(0.1, self.update_joints)

        #punto objetivo fijo///
        self.target_pos = np.array([1.2, 0.5, 0.0])  

        # Angulos iniciales ///
        self.q = np.array([-0.22, 0.7, 0.03]) 

        # Parameters for IK
        self.step_size = 0.1
        self.max_iterations = 100
        self.tolerance = 0.01
        self.damping_factor = 0.1  # For damped least squares method

    def forward_kinematics(self, q):
        q1, q2, q3 = q

# Ecuaciones de Cinemática Directa - Robot A 
        x = self.l2 * (np.cos(q2) + np.cos(q2 + q3)) * np.cos(q1)
        y = self.l2 * (np.cos(q2) + np.cos(q2 + q3)) * np.sin(q1)
        z = self.l2 * np.sin(q2) + self.l3 * np.sin(q2 + q3) + self.l1
        return np.array([x, y, z])

    def jacobian(self, q):
        q1, q2, q3 = q

        j11 = -self.l2 * (np.cos(q2) + np.cos(q2 + q3)) * np.sin(q1)
        j12 = self.l2 * (-np.sin(q2) - np.sin(q2 + q3)) * np.cos(q1)
        j13 = -self.l3 * np.sin(q2 + q3) * np.cos(q1)

# Fila Y
        j21 = self.l2 * (np.cos(q2) + np.cos(q2 + q3)) * np.cos(q1)
        j22 = self.l2 * (-np.sin(q2) - np.sin(q2 + q3)) * np.sin(q1)
        j23 = -self.l3 * np.sin(q1) * np.sin(q2 + q3)

# Fila Z
        j31 = 0
        j32 = self.l2 * np.cos(q2) + self.l3 * np.cos(q2 + q3)
        j33 = self.l3 * np.cos(q2 + q3)

        return np.array([[j11, j12, j13], [j21, j22, j23], [j31, j32, j33]])
    
    def apply_joint_limits(self, q):
        return np.clip(q, self.q_min, self.q_max)

    def target_callback(self, msg):
        self.target_pos = np.array([msg.x, msg.y, msg.z])
        self.get_logger().info(
            f"New target received: [{msg.x}, {msg.y}, {msg.z}]")

    def update_joints(self):
        current_pos = self.forward_kinematics(self.q)
        error = self.target_pos - current_pos
        error_norm = np.linalg.norm(error)

        self.get_logger().info(f"Current position: {current_pos}")
        self.get_logger().info(f"Target position: {self.target_pos}")
        self.get_logger().info(f"Error: {error_norm}")

        if error_norm > self.tolerance:
            # Compute Jacobian
            J = self.jacobian(self.q)

            determinant = np.linalg.det(J)
            self.get_logger().info(f"Jacobian determinant: {determinant}")

            JtJ = J.T @ J
            damping = self.damping_factor * np.eye(JtJ.shape[0])
            J_dls = np.linalg.solve(JtJ + damping, J.T) @ error

            # Apply update with step size
            self.q += J_dls * self.step_size
            self.q = self.apply_joint_limits(self.q)


        # Publish updated joint states
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['q1', 'q2', 'q3']
        msg.position = self.q.tolist()
        self.joint_pub.publish(msg)


def main():
    rclpy.init()
    node = InverseKinematics()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
