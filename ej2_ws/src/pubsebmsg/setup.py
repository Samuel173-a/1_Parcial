from setuptools import find_packages, setup

package_name = 'pubsebmsg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='sadabarriosrocha@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'nodo_a = pubsebmsg.nodo_a:main',
            'nodo_b = pubsebmsg.nodo_b:main',
            'nodo_c = pubsebmsg.nodo_c:main',
            'nodo_sumador = pubsebmsg.nodo_sum:main',
            'nodo_resultado = pubsebmsg.nodo_resul:main',
        ],
    },
)
