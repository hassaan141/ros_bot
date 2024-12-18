# import os
# import subprocess
# from ament_index_python.packages import get_package_share_directory


# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

# from launch_ros.actions import Node



# def generate_launch_description():


#     # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
#     # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

#     package_name='ros_bot' #<--- CHANGE ME

#     rsp = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource([os.path.join(
#                     get_package_share_directory(package_name),'launch','rsp.launch.py'
#                 )]), launch_arguments={'use_sim_time': 'true'}.items()
#     )

#     # Gazebo server 
#     gazebo_server = subprocess.Popen([
#         "gzserver",
#         "--verbose",
#         "-s", "libgazebo_ros_init.so",
#         "-s", "libgazebo_ros_factory.so"
#     ])

#     # Gazebo client
#     gzclient_process = subprocess.Popen(["gzclient"])

#     # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
#     spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
#                         arguments=['-topic', 'robot_description',
#                                    '-entity', 'my_bot'],
#                         output='screen')



#     # Launch them all!
#     return LaunchDescription([
#         rsp,
#         gazebo_server,
#         gzclient_process,
#         spawn_entity,
#     ])


import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    # Package name
    package_name = 'ros_bot'  # <--- CHANGE THIS IF YOUR PACKAGE NAME IS DIFFERENT

    # Include the robot_state_publisher launch file
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')
    # Include the Gazebo server launch file
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gzserver.launch.py'
        )]),
        launch_arguments={'verbose': 'true', 'extra_gazebo_args': '--ros-args --params-file' + gazebo_params_file }.items(),
    )

    # Include the Gazebo client launch file
    gzclient_process = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )
    # Run the spawner node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description', '-entity', 'my_bot'],
        output='screen'
    )

    diff_cont = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_cont'],
    )

    joint_broad = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_broad'],
    )

    # Launch them all
    return LaunchDescription([
        rsp,
        gazebo_server,
        gzclient_process,
        spawn_entity,
        diff_cont,
        joint_broad,
    ])
