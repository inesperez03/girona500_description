# girona500_description

ROS 2 description of the Girona500 vehicle. The main Xacro is `urdf/girona500.urdf.xacro`; it lists the vehicle, sensor, thruster and camera frames explicitly, following the structure of `bluerov.urdf.xacro`.

## Usage

```bash
colcon build --packages-select girona500_description
source install/setup.bash
ros2 launch sura_bringup sura_bringup.launch.py robot_namespace:=girona500
```

In another terminal, source the workspace and start teleop:

```bash
source install/setup.bash
ros2 launch sura_teleop teleop.launch.py robot_namespace:=girona500
```

To publish only the description, run `ros2 launch girona500_description robot_description.launch.py` instead of bringup. The teleop profile is installed with `sura_teleop` as `teleop_params_girona500_sim.yaml`.

The description launcher publishes the vehicle's fixed transforms. The bringup launcher reads `config/bringup_description.yaml` and starts the controller manager. The Xacro declares `ros2_control` interfaces for five thrusters and the IMU, pressure, DVL and GPS sensors. The default `environment:=sim` uses the workspace's `sura_hardware_interface` plugins and Stonefish topic names. The T200 lookup table is a provisional simulation choice; verify it against the Girona500 thrusters before using the controller. Real hardware also needs the correct thruster channels, inversion flags and sensor connection settings.

The vehicle geometry comes from [srv/girona500_description](https://github.com/srv/girona500_description) at revision `6ec4cdc1bf30b692fb47785d105e7f50b741a8ee`. The unused Bravo 7 assets come from [slopezba/blueprintlab_reachbravo7_manipulator_description](https://github.com/slopezba/blueprintlab_reachbravo7_manipulator_description) at revision `84b1b0852192ba777ff81e0cc63c700ad7f72b60`. The upstream projects do not state clear redistribution terms; check them before publishing this package.

The Girona500 simulation teleop uses the BlueROV joystick layout and initial controller gains. Tune those gains and confirm thruster directions on the Girona500 model before relying on closed-loop modes.
