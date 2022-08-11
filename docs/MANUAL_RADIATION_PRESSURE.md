# MANUAL: Radiation Pressure
## What even is radiation pressure?
Radiation pressure is the pressure due to radiation. (Very explanatory, I know.)

When photons impact a surface and change direction, due to the conservation of momentum, the object that reflects the photons experiences a momentum change, to preserve the total momentum of the system (which is comprised of photons AND the reflector).

This phenomenon therefore results in a very small force on any illuminated object whose magnitude is insignificant in daily life applications.

For a better and longer explanation, see [the Wikipedia page on radiation pressure](https://en.wikipedia.org/wiki/Radiation_pressure "the Wikipedia page on radiation pressure").

## What is the importance of radiation pressure on space travel?
Spacecraft in orbit are basically in a state of constant free-fall, and the effect of radiation pressure is not countered by any other force. Even though this force is very tiny, it accumulates over time and causes orbits and trajectories to shift ever so slowly. This accumulated drift must be accounted for, so that orbital stationkeeping maneuvers or mid-course-corrections can be planned accordingly. Not taking radiation pressure into account on an interplanetary flight may cause you to miss the target by a considerable margin, ending the mission earlier than expected.

## How can radiation pressure be accounted for?
OS3D has a simulation item called 'radiation pressure' which calculates the acceleration on a vessel due to the radiation pressure from a luminous body such as the Sun. 

Granted, planets like Earth also emit *some amount of* light, but accounting for such miniscule effects would really turn out to be a waste of time. 
(That being said, OS3D **does** in fact allow you to account for that as well, if you really wanted to.)

The radiation pressure is calculated by the radiation flux density at a given distance from the radiation source, the total illuminated area on the spacecraft
that is facing a certain orientation, and the said orientation of the reflecting plane normal.

![rad_press_terms](https://user-images.githubusercontent.com/80536083/184159735-4ac871d5-9a7f-4d65-8369-1f15cc59048c.png)

The radiation flux density is calculated from the body's luminosity and the vessel's distance from the light-emitting body. 
Luminosity gives the total radiation output in Watts. We then draw an imaginary sphere with a radius equal to the distance
between the body and the light source and divide the luminosity to a unit area to figure out how many Watts of power is received per meters squared.

![sphere](https://user-images.githubusercontent.com/80536083/184159646-807f1b9f-9e1b-4f67-bab7-7b009840ac49.png)

It is possible for a vessel to change orientation during flight, which would change the cross-sectional illuminated area. 
OS3D calculates this cross-sectional area itself, so the user only has to enter the real (engineering design) face area of the vessel that is illuminated.

![radpress1](https://user-images.githubusercontent.com/80536083/184158666-df8f0c10-9edb-4061-a5e6-cd482c14f2e5.png)

It is a widely known fact that spacecraft are three dimensional objects and they may have multiple orthogonal faces that are illuminated, 
resulting in radiation pressure-induced forces in different (sometimes orthogonal) directions. For that, you simply have to define multiple 
radiation pressure effects on the same vessel.

![multiple_rays](https://user-images.githubusercontent.com/80536083/184159866-6072c3ce-05c9-468e-8f26-938584f56fb7.png)

It is also possible for a vessel to change mass during flight, which would change its acceleration (since F=ma). 
The mass value can be updated automatically during constant thrust maneuvers if the mass_auto_update parameter is set to 1 in a radiation pressure simulation item. 
If this parameter is set to 0 or a constant acceleration maneuver is performed, the mass value should be updated manually. 

(Propellant flow mass is not automatically accounted for during constant acceleration maneuvers because a constant acceleration maneuver 
either implies the propellant mass loss during the maneuver is very small or the maneuver requires throttling capabilities. Throttling of 
various propulsion systems can not always be assumed to be linear with the change in mass flow rate, and in fact, this can be a very complex 
engineering problem that is highly spacecraft-specific. It is therefore the user's responsibility to change the mass value according to the 
propulsion system design they have, either manually or with a script of their own that mimicks their own propulsion system's behavior.)
