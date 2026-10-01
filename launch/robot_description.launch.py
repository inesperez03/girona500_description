from pathlib import Path
import shlex

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import xacro


def launch_setup(context, *args, **kwargs):
    robot_namespace = LaunchConfiguration('robot_namespace').perform(context).strip('/')
    environment = LaunchConfiguration('environment').perform(context)
    description_package = LaunchConfiguration('robot_description_package').perform(context)
    xacro_file = LaunchConfiguration('xacro_file').perform(context)
    xacro_arguments = LaunchConfiguration('xacro_arguments').perform(context)
    xacro_path = Path(get_package_share_directory(description_package)) / xacro_file
    mappings = {'robot_name': robot_namespace, 'environment': environment}
    for argument in shlex.split(xacro_arguments):
        name, separator, value = argument.partition(':=')
        if not separator:
            raise ValueError(f'Invalid Xacro argument: {argument}')
        mappings[name] = value
    description = xacro.process_file(
        str(xacro_path), mappings=mappings
    ).toxml()
    return [Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=f'/{robot_namespace}',
        output='screen',
        parameters=[{'robot_description': ParameterValue(description, value_type=str)}],
    )]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('robot_namespace', default_value='girona500'),
        DeclareLaunchArgument('environment', default_value='sim'),
        DeclareLaunchArgument('robot_description_package', default_value='girona500_description'),
        DeclareLaunchArgument('xacro_file', default_value='urdf/girona500.urdf.xacro'),
        DeclareLaunchArgument('xacro_arguments', default_value=''),
        OpaqueFunction(function=launch_setup),
    ])
