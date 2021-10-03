# Time Acceleration Dilemma
Should you use **delta_t** or **cycle_time** to accelerate the simulation?

TL;DR: For physical accuracy, use cycle_time whenever possible.

## What are 'delta_t' and 'cycle_time'?
The simulation runs in frames like many other simulation software. 
**delta_t** is the amount of simulated time (in seconds) the simulation calculates each frame.
**cycle_time** is the amount of real-world time the computer *should* take to calculate each frame.

You can time accelerate by either
- Increasing delta_t
- Decreasing cycle_time

## What is the trade-off?
Increasing delta_t reduces accuracy of the simulation. High delta_t values risk the simulation diverging from real-world physics.

Decreasing cycle_time usually increases the work load on your machine. If your machine can calculate each frame at, say, 0.02 seconds, your cycle_time should be just above 0.02 seconds ideally. This ensures the simulation is calculated at the fastest "safe" rate. You could lower cycle_time to 0.01 seconds -lower than what your machine can achieve- but you'll get a warning message stating

> Cycle time too low! Machine can't update physics at the given cycle time!
> Consider increasing cycle_time to get more consistent calculation rate.

Physics-wise, there is no downside for "overclocking" the simulation by setting cycle_time too low, the machine will simply update each frame at the fastest rate it can. The only downside would be the *possibly* inconsistent frame update rate, which would otherwise be controlled by a dynamic interrupter built into the simulation. (If a frame is calculated faster than the expected cycle_time, the simulation momentarily halts calculation to keep a consistent frame update rate.) If you are only using the simulation for fun, this usually will not create a major inconvenience. (...but don't quote me on that.)

### However!
You can only really lower cycle_time until you hit the limit of your machine's capabilities. (HINT: If you really want to squeeze an extra bit of cycle_time decrease, you can increase output_rate (which determines how many physics frames will be calculated per one screen drawing cycle (default is 1, so one physics frame is calculated every screen update)). You'll eventually have to increase delta_t for long space trips, such as a multiple day trip to Luna from Low Earth Orbit. (Or you'll have to keep the simulation running for a long time.)

To lower the inaccuracies and use delta_t responsibly, there are some rules you can follow.

## How to best use delta_t?


- **Decrease delta_t when flying-by gravity sources!**

High gravity itself is not the problem, this is mostly due to the increasing **change** in gravity with each frame. Let's take a look at a fancy graph to see why.

![riemann1](https://user-images.githubusercontent.com/80536083/134770036-054cbcd9-cb6e-4bc0-80ed-08a45b026af1.png)

This is a rough graph of the gravity experienced by a vessel that's rapidly moving away from a planet. The red line shows the real value of the experienced gravity at a given time, whereas the green rectangles show the Riemann sum representation of the simulated gravity. As you can see, while the vessel is moving away from the planet, there is some extra gravity applied that really shouldn't be there. Unfortunately, analytical solutions for n-body systems' behaviour isn't trivial so we are basically stuck with numerical solutions. (If you are a genious who thinks otherwise, you are welcome to open a Pull Request with your code.) For that reason, to reduce the difference between the simulated and real-world values, we lower delta_t.

In another case, if you go ahead and draw the graph for a vessel approaching a gravity source, you'll see that we are in fact not applying enough gravity!

![riemann2](https://user-images.githubusercontent.com/80536083/134770490-377ba216-74d2-4958-834a-18ac62e0b69e.png)

So, conclusion: Lower delta_t when passing close-by a gravity source.


------------

- **Decrease delta_t when performing high-precision maneuvers!**

It's basically the Riemann sum problem described above, especially with the vehicle orientation while using dynamic-orientation maneuvers. If you need to make a 3.88 second long mid-course correction burn, use a delta_t <= 0.02 to get a proper amount of precision.

The simulation, by default, decreases delta_t to 1 second prior to any maneuvers if the delta_t is larger than 1 before the maneuver starts.
