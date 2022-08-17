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
Although scenarios can keep all the data for the accurate replay of a space mission, batch files can be used to set up a nice user output screen and set Rapid Compute intervals. Demo space mission scenarios usually come with batch files with the same name as the scenario file, such as `lunar_journey.osf` and `lunar journey.obf`. In such cases, by default, OS3D also loads in the commands from the batch file. This auto-load behaviour can be changed by editing the configuration file at startup via 'Configure OrbitSim3D' option.

## Syntax Guide & Creating Scenarios
The best way to create scenarios is to design them in OS3D using the command panel and export them via the 'export' command, leaving the hassle of using the somewhat harsh syntax to the software, since OSF files are formatted in a very specific way for OS3D to parse and understand. An example is shown below, taken from `lunar_journey.osf`;

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
- Lines starting in A are for atmospheric drag effects.

Although exporting scenarios through OS3D is usually convenient, sometimes, you might want to make quick little changes to a scenario or engineer all the little details of your digital universe; for which you might want to modify scenario files by hand. For this, the necessary information is given below.

### Celestial Bodies
The syntax for denoting celestial bodies is as follows;
```
B|body_name|body_model|body_mass(kg)|body_radius(m)|body_color([r,g,b])|body_position([m,m,m])|body_velocity([m/s,m/s,m/s])|body_orientation(matrix3x3)|body_day_length(s)|body_J2|body_luminosity
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
