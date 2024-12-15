
import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
   return LaunchDescription([
    Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        output='screen',
        parameters=[{
            'image_size': [640, 480],
            'camera_frame_id': 'camera_link_optical'
        }]

    )
   ])