PRIMER PARCIAL 

Este repositorio contiene la configuración y los nodos de ROS 2 para el control del Robot_A de 3 Grados de Libertad 
y el Robot Bioinspirado de 4 Grados de Libertad mediante Cinemática Inversa, igual encontraras el jercicio 2 donde se generan 5 nodos.

REQUISITOS Y COMPILACION ROBOT_A

Se tiene que ingresar a la carpeta examen_ws el cual es nuestro workspace, se compila el programa usando el comando:
colcon build
de ahi se usa:
source install/setup.bash 
para mostrar los programas, de ahi se usa el siguiente comando para lograr la visualizacion del robot_A
ros2 launch robot_description view_robot1.launch.py 
al aplicar el comando se llega a visualizar el robot, ahora para aplicar cinematica inversa usamos otra terminal
de igual manera entramos a la carpeta examen_ws, de ahi usamos:
source install/setup.bash 
y de ahi ejecutamos el programa de cinematica inversa usando el siguiente comando:
ros2 run visual_pubsub inverse_A 
en este caso llegamos a tener un problema debido a que a veces el programa no se sincroniza con la visualizacion 
por lo que se recomienda volver cancelar el programa y volver a ejecutar asi hasta que se vea un movimento en la
visualizacion, de ahien otra terminal igual entramos al examen_ws y ejecutamos el siguiente comando para corroborar 
que la cinematica inversa funciona de manera correcta:
ros2 topic pub /target_position geometry_msgs/msg/Point "{x: 3.0, y: 0.0, z: 3.0}" --once
lo que hace el comando es poner el robot en punto de reposo.

REQUISITOS Y COMPILACION ROBOT_BIOINSPIRADO

Se tiene que ingresar a la carpeta examen_ws el cual es nuestro workspace, se compila el programa usando el comando:
colcon build
de ahi se usa:
source install/setup.bash 
para mostrar los programas, de ahi se usa el siguiente comando para lograr la visualizacion del robot_A
ros2 launch robot_description view_robot.launch.py 
al aplicar el comando se llega a visualizar el robot, ahora para aplicar cinematica inversa usamos otra terminal
de igual manera entramos a la carpeta examen_ws, de ahi usamos:
source install/setup.bash 
y de ahi ejecutamos el programa de cinematica inversa usando el siguiente comando:
ros2 run visual_pubsub inverse 
en este caso llegamos a tener un problema debido a que a veces el programa no se sincroniza con la visualizacion 
por lo que se recomienda cancelar el programa y volver a ejecutar asi hasta que se vea un movimento en la
visualizacion, de ahi en otra terminal igual entramos al examen_ws y ejecutamos el siguiente comando para corroborar 
que la cinematica inversa funciona de manera correcta:
ros2 topic pub /target_position geometry_msgs/msg/Point "{x: 23.0, y: 0.0, z: 0.0}" --once
lo que hace el comando es poner el robot en punto de reposo.

EXTRA  

En las carpeta de robot_description/launch, en esa carpeta se encuentra dos archivos view_robot.launch.py (pertenece al robot_bioinspirado) y 
view_robot1.launch.py (pertenece al robot_A)
En la carpeta de robot_description/urdf, en esa carpeta se encuentra dos archivos robot_bioinspirado.urdf (pertenece al robot_bioinspirado) y 
robot_manipulador.urdf  (pertenece al robot_A)
En la carpeta visual_pubsub, en esa carpeta se encuentra dos archivos inverse_kinematics.py (pertenece al robot_bioinspirado) y 
inverse_kinematic_robot1.py (pertenece al robot_A)
Finalmente en el archivo setup se añadio este codigo:
            'inverse = visual_pubsub.inverse_kinematics:main',
            'inverse_A = visual_pubsub.inverse_kinematic_robot1:main'


EJERCICIO 2
Se puede ver lo que es la estructura de nodos en una imagen png, que se realiza cuando todos los nodos estaban siendo ejecutados, ademas esta imagen de ROS 2 muestra cómo se mueve la información dentro del ejercicio. Los nodos sensores nodo_a, nodo_b y nodo_c generan datos de manera independiente y los envían a través de los tópicos sensor_1, sensor_2 y sensor_3. Luego, estos datos son recibidos por el nodo nodo_sumador, que se encarga de procesarlos y calcular el promedio.

Una vez obtenido el resultado, el nodo sumador publica el valor en el tópico filtered_sensor, usando una interfaz personalizada que incluye tanto el valor numérico como un identificador. Finalmente, el nodo nodo_resultado se suscribe a este tópico y muestra en pantalla el promedio calculado en tiempo real.

REQUISITOS Y COMPILACION 
para ejecutar el codigo tenemos que ingresar al ej2_ws y ejecutar el siguiente comando:
colcon build
despues de ejecutar el comando tenemos que visualizar los archivos con el siguiente comando:
source install/setup.bash 
finalmente se debe de ejecutar cada nodo en una terminal diferente para poder visualizar use los siguientes comandos para ejecutar:
ros2 run pubsebmsg nodo_a
ros2 run pubsebmsg nodo_b
ros2 run pubsebmsg nodo_c
ros2 run pubsebmsg nodo_sumador
ros2 run pubsebmsg nodo_resultado
cada codigo en una terminal diferente y para obtener la grafica ejecutamos el siguiente comando:
ros2 run rqt_graph rqt_graph --force-discover




