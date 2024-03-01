# Orbit Propagator Validation Case 1 (International Space Station)
This OrbitSim3D orbit propagator validation case is documented using the following version (commit number): [8a7037a4d0acc6ab07ca9958170bdfd7c0bd5a4a](https://github.com/arda-guler/orbitSim3D/tree/8a7037a4d0acc6ab07ca9958170bdfd7c0bd5a4a)

## Validation Case Setup
For validation of the numerical orbit propagation algorithms, a simple 2-body problem was used, replicating the orbit of International Space Station around Earth at year 2015.

The initial state was retreived from [JPL Horizons System](https://ssd.jpl.nasa.gov/horizons/app.html#/), belonging to date 2015-01-01, time 00:00:00. The final state was chosen to be after 2 days, at date 20015-01-03, time 00:00:00.

The 2-body problem was solved numerically using OS3D using different solver setups, and final state vectors were exported by plotting commands. The final state positions were then compared with those obtained from JPL Horizons system.
The scenario file can be found in [this folder](https://github.com/arda-guler/orbitSim3D/tree/master/docs/validation-2/validation_case_data/validation_scenario). As long as the same solver setups are used, the results should be reproducible.

Geocentric positional error of ISS was calculated, taking JPL Horizons data to be true results. The calculation method for the positional errors can be found in [this script](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation-2/validation_case_data/errors.py).
The exported raw data is found in [this folder](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation-2/validation_case_data), separated into folders, categorized by solver setups. The processed results are in [here](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation-2/results).

## Results
![Positional error plot for ISS](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation-2/results/ISS_propagation_errors.png?raw=true)

Here, "J2" refers to the oblate-body gravitational field model for Earth (as opposed to the point-mass model). The Euler (a 1st order solver) and Yoshida8 (an 8th order solver) were compared, with fixed time steps of dt=1 second and dt=100 seconds.

Same results in text form:

```
0.5 days (43200 seconds) integration (around 7 orbits):
dt=1s
Error: Euler w/out J2: 3.3934533417103374 %
Error: Euler w/ J2: 0.33069801201352883 %
Error: Yoshida8 w/out J2: 3.338156908582299 %
Error: Yoshida8 w/ J2: 0.4164456105805677 %

dt=100s
Error: Euler w/ J2: 10.793022970394238 %
Error: Yoshida8 w/ J2: 30.120918217199062 %


1 day (86400 seconds) integration (around 15 orbits):
dt=1s
Error: Euler w/out J2: 6.089755754093886 %
Error: Euler w/ J2: 0.5874206237855437 %
Error: Yoshida8 w/out J2: 6.497964326228753 %
Error: Yoshida8 w/ J2: 0.7892508053627536 %

dt=100s
Error: Euler w/ J2: 40.04950801764816 %
Error: Yoshida8 w/ J2: 21.496804718875566 %


2 days (172800 seconds) integration (around 31 orbits):
dt=1s
Error: Euler w/out J2: 13.97736605993215 %
Error: Euler w/ J2: 1.7015347078049137 %
Error: Yoshida8 w/out J2: 13.985818437525513 %
Error: Yoshida8 w/ J2: 1.6925799063338627 %

dt=100s
Error: Euler w/ J2: 133.14192162727758 %
Error: Yoshida8 w/ J2: 19.907185716488787 %

```

## Discussion
Using the J2 gravitational field model vastly increases accuracy over the point-mass model. This is because the simulation
better models the real-world system. Most often, this should be the first priority to increase the accuracy of any simulation.
However, more complicated models increase computation load and lengthen computation times. 

Another important point that should be noticed easily is that the errors stack up as the simulation time increases.
One exception seems to be the Yoshida8 solver with J2 model using dt=100 seconds, but that may be a coincidental
occurrence where the error "builds-up" in such a way to cancel itself out.

At low time steps, Euler and Yoshida8 solvers have comparable errors. But lower order propagators (Euler) are less stable
at higher time steps, as demonstrated with the dt=100 second cases.

In addition to the above factors, the inaccuracy of the ISS physical model contributes to errors as well. These include:
- Gravitational effects of Luna, Sol and other massive bodies
- Any outgassing or propulsive actions of the ISS
- Higher order spherical-harmonics variations in the gravitational field model
- Air drag acting on ISS
- Radiation pressure acting on ISS
- Geo-magnetic effects on ISS

# Orbit Propagator Validation Case 2 (Solar System)
This OrbitSim3D orbit propagation validation case is documented using the following version (commit number): [8694eb36573107ee0a833b327b93153b9e4832e1](https://github.com/arda-guler/orbitSim3D/commit/8694eb36573107ee0a833b327b93153b9e4832e1).

## Validation Case Setup
For validation of the orbit propagation algorithms, an n-body problem was used, replicating the Sol system with the central star and the 8 known major planets; Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.

The initial state was retreived from [JPL Horizons System](https://ssd.jpl.nasa.gov/horizons/app.html#/), belonging to date 2001-01-01, time 00:00:00. The final state was chosen to be after 1 year, at date 2002-01-01, time 00:00:00.

The n-body problem was solved by using OS3D using different solver setups, and the final state vectors were exported into scenario files. These were then compared to the final state vectors obtained from JPL Horizons system. 
These scenario files can be found in [this folder](https://github.com/arda-guler/orbitSim3D/tree/master/docs/validation/validation_scenarios). As long as the same solver setups are used, the results should be reproducible.

Positional errors of the planets were calculated, taking JPL Horizons data to be the true results. The calculation method for the positional errors can be found in [this script](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation/scripts/errors.py).

## Results
![Positional percent error plot](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation/position_errors.png?raw=true)

**Y4:** Yoshida4 solver

**SE:** Symplectic Euler solver

**dt:** time step size in seconds

Same results in text form:
```
Validation 1: Yoshida8, dt=1e3, t=31580001
Neptune position error:  0.005185221805610567 %
Uranus position error:  0.009382649744726412 %
Saturn position error:  0.032205378660685686 %
Jupiter position error:  0.07306456603222408 %
Mars position error:  0.5206266761043397 %
Earth position error:  0.8899959830495072 %
Venus position error:  1.3683105995155578 %
Mercury position error:  3.6271921157871105 %

Validation 2: Yoshida4, dt=5e2, t=31579501
Neptune position error:  0.00518522162380062 %
Uranus position error:  0.00938264941627399 %
Saturn position error:  0.03220537753503094 %
Jupiter position error:  0.07306456348264366 %
Mars position error:  0.5206266579470141 %
Earth position error:  0.889995952051969 %
Venus position error:  1.3683105518566654 %
Mercury position error:  3.627191989735945 %

Validation 3: Symplectic Euler, dt=1e3, t=31580001
Neptune position error:  0.005185329401051024 %
Uranus position error:  0.009383019038573142 %
Saturn position error:  0.03222659506273214 %
Jupiter position error:  0.07329852903605512 %
Mars position error:  0.5387484835653709 %
Earth position error:  0.8898279436085739 %
Venus position error:  1.418880683205945 %
Mercury position error:  3.3646809412859358 %
```

## Discussion
In addition to truncation errors and roundoff errors, other sources of errors may be the following:
- The timing inaccuracy in stopping the simulation at its final state
- Absence of moons and other minor bodies
- Uncertainties in masses of bodies
- Point mass assumption
- Planets not having been placed in the barycenters of their respective moon systems, but instead to their actual positions
- Planets not being given the initial velocities of the barycenters of their respective moon systems, but instead their actual velocities
- Absence of general relativity, drag, outgassing, radiation, mass flow, electromagnetic interactions and other minor effects

The reasons why errors of planets closer to the Sun are higher may be:
1) The increasing rate of change of gravitational acceleration in tighter orbits. The rate of change of the direction of the gravity vector per unit time is higher, as well
as the rate of change of gravitational acceleration per unit radial distance increment.
2) The increasing rate of travel in tighter orbits.
3) The magnitude of position used for error calculation of more distant planets being higher

The reason why the lower order Symplectic Euler might be doing better in case of Mercury *might be* (meaning this is just a theory) due to its tendency to "walk" the periapsis of the planet around the Sun. However, this should not mean
that Symplectic Euler is a more accurate solver. See below.

The following comparison shows the relative accuracies of the different solvers in a two-body problem.

![Comparison of orbit propagators](https://github.com/arda-guler/orbitSim3D/blob/master/docs/validation/propagator_comparison.png)

As evident, higher order propagators are more accurate and "stable", given the same time step size.

## Reducing Errors
To reduce the errors, generally, the systems should be modeled more faithfully to their real counterparts (e.g. adding the moons of Jupiter to the validation scenario), higher order integrators should be used, lower time step sizes should be preferred.
However, all of these steps increase the computation time, hence, a balance between resource expenditure and accuracy should be found.
