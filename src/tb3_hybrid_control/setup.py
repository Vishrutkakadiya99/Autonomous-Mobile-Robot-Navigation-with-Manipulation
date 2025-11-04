from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'tb3_hybrid_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Install launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.py'))),
        # Install config files (for arm goals)
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='ROS 2 package for combined Nav2 and MoveIt2 control of TurtleBot3 Manipulator',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Define your main executable node
            'hybrid_controller = tb3_hybrid_control.hybrid_controller:main',
        ],
    },
)
