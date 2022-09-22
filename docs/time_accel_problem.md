# Time Acceleration Problem
There are many ways to accelerate simulated time in OS3D. The questions are; which one is the best, and in what situations should you use them, and how?

 - Increasing delta_t
 - Decreasing cycle_time
 - Increasing output_rate
 - Using 'Rapid Compute'

TL;DR: Use the **'Rapid Compute'** system whenever possible if you are only after the results and can sacrifice instantaneous user output. If you want to keep instantaneous user output and still care about physical accuracy, use **cycle_time** whenever possible, and **increase output_rate** for a bit more push. If all else fails and you can settle for sacrificing a bit of physical accuracy for a faster simulation, you may **increase delta_t**.

## The Advanced & Convenient Solution
The 'Rapid Compute' system is the ultimate time acceleration method in OS3D. It is essentially an automated implementation of every physical-accuracy-protecting method I have discussed further into this document. It is available in the form of a command at runtime in OS3D, which can be reached through the command panel or typed into the command line.

Once you set the time interval during which you want the simulation to be 'rapid computed', the simulation switches into a mode where it provides nearly no user output and instead allocates all computing power it can get to mathematical operations. The simulation switches back into the usual operation mode once rapid compute reaches its target time.

This makes the simulation behave more like analysis software.

## What are 'delta_t' and 'cycle_time' and 'output_rate'?
The simulation runs in frames like many other simulation software that resort to numerical calculations. In this case, the 'frames' are the 'time infinitesimal (dt)' equivalents of computer world.

**delta_t** is the amount of simulated time (in seconds) the simulation calculates each frame. For the duration of a single frame, all vectors and scalars (and all other sorts of variables including matrices and quaternions) are static values. The values are updated between each frame. A frame can be called a 'physics frame' to differentiate between output frames and physical calculation frames. (At least that's what I call them.)

**cycle_time** is the amount of real-world time the computer *should* take to calculate each frame. It is does not act as a hard limit for the computer, since you can't force a computer to calculate faster than its hardware lets it to. cycle_time, in that sense, is more of a suggestion, or perhaps more of an aspirational goal for the machine.

**output_rate** is a bit of a mis-named value. It is the ratio of user-output updates to physics updates. If yout output_rate is 10, this means 10 physics frames are calculated between each UI updates.

## What is the trade-off?
Increasing delta_t reduces accuracy of the simulation. High delta_t values risk the simulation diverging from real-world physics. That is because the supposedly infinitesimal dt value is no longer infinitesimal enough at high delta_t values. In that case, the calculations become less of an integral and more a discrete summation. We don't want that.

Decreasing cycle_time usually increases the work load on your machine. If your machine can calculate each frame at, say, 0.02 seconds, your cycle_time should be just above 0.02 seconds ideally. This ensures the simulation is calculated at the fastest consistent rate. You could lower cycle_time to 0.01 seconds -lower than what your machine can achieve- but (if warn_cycle_time is enabled) you'll probably get a warning message stating

> Cycle time too low! Machine can't update physics at the given cycle time!
> Consider increasing cycle_time to get more consistent calculation rate.

Physics-wise, there is no downside for "overclocking" the simulation by setting cycle_time too low, the machine will simply update each frame at the fastest rate it can. The only downside would be the *possibly* inconsistent frame update rate (or your computer catching on fire), which would otherwise be controlled by a dynamic interrupter built into the simulation. (If a frame is calculated faster than the expected cycle_time, the simulation momentarily halts calculation to keep a consistent frame update rate.) If you are only using the simulation for fun, this usually will not create a major inconvenience. (...but don't quote me on that.)

Increasing output_rate increases the choppiness of UI updates. By adjusting output_rate, you trade between visual convencience and simulation progression speed.

### However!
You can only really lower cycle_time until you hit the limit of your machine's capabilities, and increasing output_rate beyond a certain point will not make much sense. You'll eventually have to increase delta_t for long space trips, such as a multiple day trip to Luna from Low Earth Orbit. (Or you'll have to keep the simulation running for a long time.)

To lower the inaccuracies and use delta_t responsibly, there are some rules you can follow.

## How to best use delta_t?


- **Decrease delta_t when flying-by gravity sources!**

High gravity itself is not the problem, this is mostly due to the increasing **change** in gravity with each frame. Let's take a look at a fancy graph to see why.

![riemann1](https://user-images.githubusercontent.com/80536083/134770036-054cbcd9-cb6e-4bc0-80ed-08a45b026af1.png)

This is a rough graph of the gravity experienced by a vessel that's rapidly moving away from a planet. The red line shows the real value of the experienced gravity at a given time, whereas the green rectangles show the Riemann sum representation of the simulated gravity. As you can see, while the vessel is moving away from the planet, there is some extra gravity applied that really shouldn't be there. An this is not it, the change is not only in the magnitude of the gravity but also the direction! Unfortunately, analytical solutions for n-body systems' behaviour isn't trivial, so we are basically stuck with numerical solutions. (If you are a genius who thinks otherwise, you are welcome to open a Pull Request with your code.) For that reason, to reduce the difference between the simulated and real-world values, we lower delta_t.

In another case, if you go ahead and draw the graph for a vessel approaching a gravity source, you'll see that we are in fact not applying enough gravity!

![riemann2](https://user-images.githubusercontent.com/80536083/134770490-377ba216-74d2-4958-834a-18ac62e0b69e.png)

So, conclusion: Lower delta_t when passing close-by a gravity source.


------------

- **Decrease delta_t when performing high-precision maneuvers!**

It's basically the Riemann sum problem described above, especially with the vehicle orientation while using dynamic-orientation maneuvers. If you need to make a 3.88 second long mid-course correction burn, use a delta_t <= 0.02 to get a proper amount of precision.

The simulation, by default, decreases delta_t to 1 second prior to any maneuvers if the delta_t is larger than 1 before the maneuver starts. (You can change this behaviour by modifying the configuration file.)
