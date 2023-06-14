# Orbit Propagator Validation
OrbitSim3D orbit propagation validation is documented using the following version (commit number): [8694eb36573107ee0a833b327b93153b9e4832e1](https://github.com/arda-guler/orbitSim3D/commit/8694eb36573107ee0a833b327b93153b9e4832e1).

## Validation Case
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
