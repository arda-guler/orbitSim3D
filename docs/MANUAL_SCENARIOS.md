# MANUAL: OS3D Scenarios

## File Format
The OSF file extension stands for "OS3D Scenario Format". They are actually plain text files, but the extension simply differentiates them from files for human reading, such as TXT files. Scenario files can be opened by any text editor of your choice.

## What is a scenario anyway?
A scenario is a 'simulation state' at a given time. It contains the state vectors about planets, spacecraft and all such data using which any future (or past!) state of the system can be calculated.

## Loading Scenarios
Although you could load scenario files to OS3D from any path, the 'scenarios' directory is where scenario files are usually kept. If you wish to load a scenario from that directory, you don't need to specify the full path, it is enough to write the filename.

(Typing in `two_mirrors` is equal to typing in `scenarios/two_mirrors.osf` while loading a scenario.)

Any scenarios you export using OS3D will also appear there, in the 'scenarios' directory.

## Scenarios & Batch Files
Although scenarios can keep all the data for the accurate replay of a space mission, batch files can be used to set up a nice user output screen and set Rapid Compute intervals. Demo space mission scenarios usually come with batch files with the same name as the scenario file, such as `lunar_flight.osf` and `lunar_flight.obf`. In such cases, by default, OS3D also loads in the commands from the batch file. This auto-load behaviour can be changed by editing the configuration file at startup via 'Configure OrbitSim3D' option.

## Syntax Guide & Creating Scenarios
The best way to create scenarios is to design them in OS3D using the command panel and export them via the 'export' command, leaving the hassle of using the somewhat harsh syntax to the software, since OSF files are formatted in a very specific way for OS3D to parse and understand. An example is shown below;

```
;Celestial bodies
B|Earth|data\models\miniearth.obj|5972000000000000000000000|6371000|[0.0,0.25,1.0]|[0,0,0]|[0,0,0]|[[1,0,0],[0,1,0],[0,0,1]]|86400|0|0
B|Luna|data\models\miniluna.obj|73420000000000000000000|1737000|[0.8,0.8,0.8]|[346410000,10,-200000000]|[-483,0,-836.5]|[[1,0,0],[0,1,0],[0,0,1]]|2360592|0|0

;Vessels
V|lunar-orbiter|data\models\miniprobe.obj|[0.0,0.8,0.7]|[-590131,-10,6745234]|[7622,0,667]

;Maneuvers
M|mnv_tli|const_accel|lunar-orbiter|Earth|prograde|10|50|315
M|mnv_loi1|const_accel|lunar-orbiter|Luna|retrograde_dynamic|10|399300|50

;Surface points
S|science-target|Luna|[1,0,0]|[10,50,0]

;Barycenters
C|earth-luna-bc|Earth,Luna

```

Every line contains the various properties of simulation items -such as vessels, celestial bodies and orbital maneuvers- in a very specific order. To make the file more readable, a scenario author may choose to write comments. It is not necessary to use the semicolon (;) to denote comment lines, but if a line starts with one of the specific characters that the scenario loader function is looking for, it may try to parse a comment and fail, so using a character like semicolon to denote comments is a nice practice.

The list of special characters is given below;
- Lines starting in B are for bodies,
- Lines starting in V are for vessels,
- Lines starting in M are for maneuvers,
- Lines starting in S are for surface points,
- Lines starting in C are for barycenters,
- Lines starting in R are for radiation pressure effects,
- Lines starting in A are for atmospheric drag effects,
- Lines starting in P are for proximity zones,
- Lines starting in U are for resources.

Although exporting scenarios through OS3D is usually convenient, sometimes, you might want to make quick little changes to a scenario or engineer all the little details of your digital universe; for which you might want to modify scenario files by hand. For this, the necessary information is given below.

### Celestial Bodies
The syntax for denoting celestial bodies is as follows;
```
B|body_name|body_model|body_mass(kg)|body_radius(m)|body_color([r,g,b])|body_position([m,m,m])|body_velocity([m/s,m/s,m/s])|body_orientation(matrix3x3)|body_day_length(s)|body_rotation_axis(vector3)|body_J2|body_luminosity
```

If J2, day length or luminosity are unknown, they should be set to 0. If orientation is not known or irrelevant to the simulation, the best option is to set it as a 3x3 identity matrix, i.e. [[1,0,0],[0,1,0],[0,0,1]]

### Vessels
The syntax for denoting vessels is as follows;
```
V|vessel_name|vessel_model|vessel_color|vessel_position([m,m,m])|vessel_velocity([m/s,m/s,m/s])
```

Vessel mass and vessel orientation are irrelevant for the simulation as orbital maneuver parameters take care of such data.

### Maneuvers
The syntax for denoting constant accel maneuvers is as follows;
```
M|maneuver_name|maneuver_type(const_accel)|vessel|ref_frame|direction(preset/vector3)|acceleration(m/s/s)|start_time(s)|duration(s)
```

The syntax for denoting constant thrust (increasing acceleration) maneuvers is as follows;
```
M|maneuver_name|maneuver_type(const_thrust)|vessel|ref_frame|direction(preset/vector3)|thrust(N)|initial_mass(kg)|mass_flow(kg/s)|start_time(s)|duration(s)
```

### Surface Points
The syntax for denoting surface points is as follows;
```
S|surface_point_name|body|color([r,g,b])|position([lat(deg),lon(deg),alt(m)])
```

Surface points can be placed above or below the 'sea-level' by setting altitude to anything other than 0.

### Barycenters
The syntax for denoting barycenters is as follows;
```
C|barycenter_name|body1,body2,body3,body4...
```

2+ bodies should be entered to the last parameter, separated by commas.

### Radiation Pressure
The syntax for denoting the effects of radiation pressure is as follows;
```
R|effect_name|vessel|body|illuminated_area(m2)|reaction_force_orientation|vessel_mass(kg)|mass_auto_update_option
```
The mass auto-update option automatically reduces vessel mass in case of a constant thrust maneuver, since propellant will be spent.

### Atmospheric Drag
The syntax for denoting the effects of atmospheric drag is as follows;
```
A|effect_name|vessel|body|drag_area(m2)|drag_coeff|vessel_mass(kg)|mass_auto_update_option
```
The mass auto-update option automatically reduces vessel mass in case of a constant thrust maneuver, since propellant will be spent.

### Proximity Zone
The syntax for denoting proximity zones is as follows;
```
P|zone_name|vessel|vessel_size(m, radius)|zone_size(m, radius)
```

### Resource
The syntax for denoting custom resources is as follows;
```
U|resource_name|initial_value|equation_type(polynomial/logarithmic/power, incremental/absolute)|variable|object1|object2|equation_coefficients|value_min_max_limits
```

## [Example Scenarios](https://github.com/arda-guler/orbitSim3D/tree/master/scenarios)
OS3D provides example scenarios in /scenarios folder, demonstrating nearly all OS3D features in simple ways and settings.

Each of the example scenarios are explained below. These example missions can be categorized into three main types:
- **Demonstration:** This scenario demonstrates a space mission or OS3D features.
- **Challenge:** This scenario challenges the user to plan and execute a space mission to acheive the given objectives.
- **Sandbox:** This scenario was made as a template to build other scenarios upon or to play around the universe with.

### [3body.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/3body.osf)
**Type:** Demonstration / Sandbox

**Desc:** A model of the Alpha Centauri triple star system with the fictional planet "Trisolaris" from Cixin Liu's famous sci-fi novel Three Body Theorem (the first book in Remembrance of Earth's Past).

### [apophis_2029.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/apophis_2029.osf)
**Type:** Demonstration

**Desc:** The expected Earth fly-by of 99942 Apophis in 2029.

### [artemis-1.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/artemis-1.osf)
**Type:** Demonstation

**Desc:** Orion deep space capsule flies outbound to Luna, having been injected into a Luanr transfer orbit.

### [ascent.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/ascent.osf)
**Type:** Demonstration

**Desc:** An ascent capsule launches from Luna's surface, entering a low Selenocentric orbit.

### [decay.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/decay.osf)
**Type:** Demonstration / Sandbox

**Desc:** The orbit of an abandoned space station in LEO decays due to atmospheric drag. Slowly.

### [DEFCON.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/DEFCON.osf)
**Type:** Demonstration

**Desc:** Mutually assured destruction, the destroyer of worlds. USA and USSR launch ICBMs at each other.

### [fourth_twilight.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/fourth_twilight.osf)
**Type:** Demonstration

**Desc:** A few spacecraft orbiting Earth at different inclinations, under the influence of oblate body gravitational perturbations.

### [geostationary.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/geostationary.osf)
**Type:** Demonstration / Sandbox

**Desc:** Two geostationary satellites in zero inclination orbits, their phases 180 degrees apart.

### [hell_probe.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/hell_probe.osf)
**Type:** Demonstration

**Desc:** In this mission, an exploration probe parked in LEO is brought to a Venus orbit.

### [hypervelocity.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/hypervelocity.osf)
**Type:** Demonstration

**Desc:** A space station collides with a satellite in LEO and contributes to Kessler syndrome.

### [JUICE.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/JUICE.osf)
**Type:** Demonstration

**Desc:** JUICE aligns itself for a slingshot around Earth using a Lunar gravity assist in August 2024.

### [jupiter_direct.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/jupiter_direct.osf)
**Type:** Demonstration

**Desc:** A futuristic spacecraft performs a constant 1G brachistochrone transfer flight from Earth to Jupiter.

### [lagrange.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/lagrange.osf)
**Type:** Sandbox

**Desc:** Objects in Earth-Sol L4 and L5 lagrange points.

### [launch_vehicle.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/launch_vehicle.osf)
**Type:** Demonstration

**Desc:** Launch of a small-sat two-stage launch vehicle.

### [mars_transfer.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/mars_transfer.osf)
**Type:** Demonstration

**Desc:** A simple Hohmann transfer from Earth to Mars. 

### [northern_terror.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/northern_terror.osf)
**Type:** Sandbox

**Desc:** A hypothetical Near-Earth Object strike on, well, Earth.

### [occultation.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/occultation.osf)
**Type:** Demonstration

**Desc:** Shows a satellite generating and consuming battery power in LEO, entering and exiting Earth's shadow.

### [OdysseyII.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/OdysseyII.osf)
**Type:** Challenge

**Desc:** Takes place in Arthur C. Clarke's 2001 universe, Leonov arrives at Jupiter and has to rendezvous with the derelict Discovery in the orbit of Io.

### [orbital_rendezvous_demo.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/orbital_rendezvous_demo.osf)
**Type:** Demonstration

**Desc:** A satellite performs an expensive orbital rendezvous mission in Earth orbit to meet up with another satellite. A solution for the two_mirrors challenge scenario.

### [sol.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/sol.osf)
**Type:** Sandbox

**Desc:** Our solar system.

### [solar_surf.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/solar_surf.osf)
**Type:** Demonstration

**Desc:** A demonstration of solar sails, with two satellites in a rather low Heliocentric orbit. One has a solar sail, the other has not.

### [sun_synchronous.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/sun_sychronous.osf)
**Type:** Demonstration

**Desc:** A sun synchronous Earth observation satellite, never going into Earth's dark side.

### [three_vessels.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/three_vessels.osf)
**Type:** Sandbox

**Desc:** The very first OS3D scenario ever created. Kept for nostalgia reasons. Self-explanatory. There are three vessels to play around with.

### [two_mirrors.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/two_mirrors.osf)
**Type:** Challenge

**Desc:** Can you rendezvous the two satellites in out-of-plane orbits?

### [voyager.osf](https://github.com/arda-guler/orbitSim3D/blob/master/scenarios/voyager.osf)
**Type:** Demonstration

**Desc:** Voyager 1's Grand Tour milestone - the Jupiter flyby!
