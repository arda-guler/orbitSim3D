# orbitSim3D Manual

**OS3D** is an n-body gravitational systems and space mission simulator.

## Requirements

- Any OS that can run Python 3

- Python 3 with following 3rd party packages;
  - pyOpenGL
  - glfw
  - pywavefront
  - keyboard
  - matplotlib
  - numpy

## Quickstart

Run main.py through the command line/terminal to start.

See the [introductory tutorial](http://github.com/arda-guler/orbitSim3D/blob/master/docs/tutorial.md "introductory tutorial") for a quick introduction to using OS3D.

#### Default Keyboard Controls

**C**: Use command line.

**P**: Open command panel.

**W, A, S, D, Q, E**: Camera rotation.

**U, I, O, J, K, L**: Camera translation.

**T, G**: Increase/decrease camera translation speed.

**CTRL+L, CTRL+K**: Lock/unlock keyboard inputs.

Controls can be edited via 'Configure OrbitSim3D' option at startup.

## Working Principles

Instead of using Kepler's Laws, which are quite useful and accurate for most two-body systems, this simulation calculates the motion of celestial bodies and spacecraft in small time steps and integrates gravitational acceleration from all celestial bodies currently in the simulation. (Spacecraft maneuvers work the same way too.) All geometrical and mathematical relations are based on numerical/infinitesimal-like calculations.

This way, no movement happens "on rails", and perturbations from distant bodies are always accounted for.

(However, if you wish, you can still make Kepler style orbit projections, determine apoapsis and periapsis and ascending nodes and all that; but if the perturbations are too high, the spacecraft wouldn't necessarily follow the calculated 2-body orbit path.)

Given a J2 value on scenario setup, the simulation can also account for the oblateness of celestial bodies and apply J2 perturbations.

Given the required parameters, the simulation can account for atmospheric drag. The orbital decay due to atmospheric drag can be estimated for the planning of station-keeping boost burns or to decide on the best altitude for an acceptable decay rate while staying in close enough proximity of a planet.

Given the required parameters, the simulation can also account for radiation pressure. This can be used to calculate the drift in interplanetary trajectories that accumulate over time, or can be used as a main propulsion method in the case of solar sails. To learn more, see the [manual on radiation pressure effects.](https://github.com/arda-guler/orbitSim3D/blob/master/docs/MANUAL_RADIATION_PRESSURE.md)

OS3D is quite configurable and extendable, so much so that it will let the user make mistakes. The real-world accuracy of the simulation therefore depends on the user. For a simple introduction about possible risks, please read about the [Time Acceleration Problem](https://github.com/arda-guler/orbitSim3D/blob/master/docs/time_accel_problem.md "Time Acceleration Problem"), which is actually the OS3D version of a common trouble in scientific simulation software, engineering analysis software, video games and the like.

Relativistic effects are not taken into account whatsoever.

## Scenarios (.osf)

There are some scenario files provided in the /scenarios directory. These scenarios act as an initial state for a simulation. To learn more, read the [detailed manual on OS3D scenarios](https://github.com/arda-guler/orbitSim3D/blob/master/docs/MANUAL_SCENARIOS.md "detailed manual on OS3D scenarios") and check out any of the provided .osf files and read the scenario comments for more information about individual scenarios.

## Batch Files (.obf)

Instead of repeatedly entering some commands every time you start a scenario, or every time you want to perform a repeated task, you can create batch files to read the commands from. These are simple text files, and can be edited using any text editor you like. Syntax is the same as the run-time commands that are accepted by the interpreter, so in that sense, they work pretty much the same way batch files are used by operating systems.

## Config Files (.cfg)

These are text files which hold the options such as window size and keyboard control settings, as well as initial values for the simulation such as time step length (delta_t) or physics-to-output-frame ratio (output_rate).

There are only two configuration files;

 - data/config/current.cfg --> the settings currently in use
 - data/config/default.cfg --> the fallback option

## Code Organization

- main.py: initializer, command interpreter, main loop and high-level essential functionality routines.

- graphics.py: OpenGL functions for 3D rendering.

- vessel_class.py: the 'vessel' class used for representing spacecraft or small objects such as debris chunks which do not generate notable gravitational fields.

- body_class.py: the 'body' class used for representing celestial bodies such as planets or asteroids, which DO generate notable gravitational fields.

- camera_class.py: the 'camera' class used for  representing camera objects to move and rotate the user's point of view, as well as track objects in the 3D scene.

- surface_point_class.py: the 'surface_point' class used for representing points on the surfaces of celestial bodies, such as tracking stations, geographical features or landing zones.

- barycenter_class.py: the 'barycenter' class used for marking barycenters of two or more celestial bodies and making calculations relative to them.

- maneuver.py: the 'maneuver' classes used for various types of maneuvers that can be performed by spacecraft.

- radiation_pressure.py: the 'radiation_pressure' class used to simulate the effects of radiation pressure on spacecraft.

- atmospheric_drag.py: the 'atmospheric_drag' class used to simulate the effects of atmospheric drag on spacecraft.

- math_utils.py: general mathematical functions  that are not provided by the math library.

- orbit.py: 2-body Keplerian orbit class that is used for making quick trajectory projections into the future.

- plot.py: plot class that handles plotting of variables in certain time intervals on user's demand.

- command_panel.py: command panel window which provides a basic GUI interface for entering commands easily.

- config_utils.py: handles reading and editing of config files at data/config which hold values that the simulations are initialized with more of a convenience utility rather than a necessity.

- ui.py: includes functions to print alphanumeric characters on 3D viewport to help out graphics.py.

- vector3.py: 3D vector class to handle vector math/operations

- matrix3x3.py: 3x3 matrix class to handle matrix operations
