import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ubuntu/Robotica_class/1_Parcial/examen_ws/install/visual_pubsub'
