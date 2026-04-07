import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import numpy as np
import time

class InverseKinematics(Node):

    def __init__(self):
        super().__init__('inverse_kinematics_pulgar_suave')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.target_sub = self.create_subscription(Point, 'target_position',
                                                     self.target_callback, 10)
        
        # PARÁMETROS DEL ROBOT
        self.l1 = 10
        self.l2 = 6
        self.l3 = 4
        self.l4 = 3
        
        # Límites Articulares
        self.q_min = np.array([-3.14, -3.14, -3.14, -3.14]) 
        self.q_max = np.array([3.14, 3.14, 3.14, 3.14])

        # PUNTO OBJETIVO FIJO 
        self.target_pos = np.array([23.0, 0.0, 0.0])  
        
        self.q = np.array([0.0, -0.5, -0.5, -0.5])  
        
        self.global_gain_factor = 2.5       
        self.tolerance = 0.015        
        self.timer_period = 0.02 # Frecuencia de actualización alta (50 Hz)
        
        self.damping_factor = 0.05    
        self.max_step_magnitude = 0.5
        self.timer = self.create_timer(self.timer_period, self.update_joints) 

        self.get_logger().info(f"Objetivo: {self.target_pos}")
    
    def forward_kinematics(self, q):
        q1, q2, q3, q4 = q
        
        x = self.l1 * np.cos(q1) \
            + self.l2 * np.cos(q1 + q2) \
            + self.l3 * np.cos(q1 + q2 + q3) \
            + self.l4 * np.cos(q1 + q2 + q3 + q4)

        y = self.l1 * np.sin(q1) \
            + self.l2 * np.sin(q1 + q2) \
            + self.l3 * np.sin(q1 + q2 + q3) \
            + self.l4 * np.sin(q1 + q2 + q3 + q4)

        z = 0
        return np.array([x, y, z])

    def jacobian(self, q):
        q1, q2, q3, q4 = q
        # -----------------------------
# JACOBIANO
# -----------------------------

# Fila X
        j11 = -self.l1*np.sin(q1) - self.l2*np.sin(q1+q2) - self.l3*np.sin(q1+q2+q3) - self.l4*np.sin(q1+q2+q3+q4)
        j12 = -self.l2*np.sin(q1+q2) - self.l3*np.sin(q1+q2+q3) - self.l4*np.sin(q1+q2+q3+q4)
        j13 = -self.l3*np.sin(q1+q2+q3) - self.l4*np.sin(q1+q2+q3+q4)
        j14 = -self.l4*np.sin(q1+q2+q3+q4)

# Fila Y
        j21 = self.l1*np.cos(q1) + self.l2*np.cos(q1+q2) + self.l3*np.cos(q1+q2+q3) + self.l4*np.cos(q1+q2+q3+q4)
        j22 = self.l2*np.cos(q1+q2) + self.l3*np.cos(q1+q2+q3) + self.l4*np.cos(q1+q2+q3+q4)
        j23 = self.l3*np.cos(q1+q2+q3) + self.l4*np.cos(q1+q2+q3+q4)
        j24 = self.l4*np.cos(q1+q2+q3+q4)

# Fila Z (robot planar)
        j31 = 0
        j32 = 0
        j33 = 0
        j34 = 0

        return np.array([[j11, j12, j13, j14], 
                         [j21, j22, j23, j24], 
                         [j31, j32, j33, j34]])

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

        if error_norm > self.tolerance:
            
            scaling_factor = self.global_gain_factor * error_norm
            
            if scaling_factor > self.max_step_magnitude:
                scaling_factor = self.max_step_magnitude
                
            J = self.jacobian(self.q)
            JtJ = J.T @ J 
            damping_sq = (self.damping_factor ** 2) * np.eye(JtJ.shape[0])
            
            dq_dir = np.linalg.solve(JtJ + damping_sq, J.T) @ error
            
            dq_norm = np.linalg.norm(dq_dir)
            dq_unit_vector = dq_dir / dq_norm if dq_norm > 1e-6 else dq_dir

            self.q += dq_unit_vector * scaling_factor * self.timer_period
            
            self.q = self.apply_joint_limits(self.q)
            
        else:
            self.get_logger().info("Objetivo alcanzado")

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['q1', 'q2', 'q3', 'q4'] 
        msg.position = self.q.tolist()
        self.joint_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
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