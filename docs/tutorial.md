# Introductory Tutorial
## Overview (Babbling)
Welcome to OS3D. Here, you can try your hand at navigating spacecraft in a 1:1 scale digital universe with true-to-real-life Newtonian Laws of Motion and find your way through some n-body chaos - all without putting billions of dollars of hardware at risk. *(General relativity will be none of our concern as long as we simulate spacecraft that travel far below the speed of light. If that sounds kind of sad, that's probably because it is.)*

Who knows, one day, you might come up with a brilliant low-energy trajectory which a space agency might use for their next robotic exploration mission. Or you could just start the simulation and admire the wireframe monochrome planet graphics. It's okay. I don't judge. Take your time.

Now, of course you could just dive in and mash random keys with no knowledge of or experience with orbital mechanics (or the Newton's Laws of Motion for that matter), and that could result in you getting what you want; however, that's  not the most efficient way to go about things and perhaps it would be a good idea to get some basic understanding about the workings of OS3D before  you take you first flight to distant worlds.

So, in this tutorial, I will introduce you to some basic simulation controls and show you how to operate this software. You can relax, I won't grade your performance.
## The Actual Tutorial

Let's get started. I will **type in bold letters like this** if I want you to do something, ***type in italic bold if there is something optional to do*** and type like this when I'm just explaining something and I don't expect you to do anything but pay attention.

### Getting Started
**If you haven't done so already, run main.py from your command prompt or terminal to see the initialization menu.**

You should be seeing three options - one for loading a scenario, one for starting an empty scene and the last one for configuring OS3D. ***You can configure your keyboard controls the way you like, but please don't touch any other configuration variables if you don't know what you are doing. Close the config editor window when you are done, and return to initialization menu.***

In order to simulate a system, OS3D first needs to know about the initial states of the celestial bodies and spacecraft you want to simulate. Such data is kept in .osf files (usually in the `scenarios/` folder) in plain text format, but creating a scenario from scratch can sometimes be a bit too much work due to the strict formatting requirements (I should do something about that sometime). I know you are eager to fly spaceships, so let's skip the boring part now and load one of the scenarios I prepared beforehand.

**Choose the first option in the initialization menu by either typing '1' or 'L' and pressing Enter, which will let you choose the scenario to load.**

The program will ask for the scenario filename next. You could of course type in the name of any scenario, but for the purposes of this tutorial, I will ask you to load a specific scenario.

**Type in 'two_mirrors' and press Enter to load the scenario.**

*Like this:*
[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or1.PNG?raw=true)](http://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or1.PNG?raw=true)

The program will quickly load the scenario, and a second window will appear. The command prompt (terminal) will act as the numerical output display as well as the command interpreter, whereas the OpenGL window will act as the 3D rendering canvas.

### A First Look at the Simulated Universe

![pict1](https://user-images.githubusercontent.com/80536083/178112594-01590b9e-3a9a-45fc-a5f5-3963555ecc53.PNG)

If you look at the OpenGL window, you will see a blue orb and two objects next to it leaving trails as they move around. The beautiful blue orb is planet Earth, and the two objects (one magenta and one cyan) are two imaginary satellites orbiting Earth.

***Try moving the camera around the scene, rotate and translate your viewpoint.***

If you get close enough to either one of the satellites, you will be able to see their 3D models. Note that there are no collision checks for the camera, and it might pass through the Earth, creating weird graphical effects. In that case, just translate your camera backwards until you are out of the planet.

Once you are done playing with the camera and pretending you are a WWII fighter in space, let's get to business. How about we start off by maneuvering one of these satellites into an elliptical orbit that takes it much higher above Earth? (In case you didn't notice, you have no choice but to agree since this is a non-interactive text tutorial.)

### Controlling the Simulation

The simulated spacecraft (actually the whole simulation) can be controlled via two methods, which are actually the same method but with different aesthetics;
- Using the command line (makes you look cool)
- Using the command panel (helps you keep your cool)

Notice the only difference between the above options are the words 'line' and 'panel' - they do the same thing in different ways. The command line is, well, a command line, just like the one in, say, DOS. Command panel is a graphical tool; so if the command line is analogous to MS-DOS, the command panel is analogous to Windows 3. I think you get the idea.

Now, you can use whichever one of these options you like, but I suggest that you go with the command panel since it will make your life a hundred times easier. It is many times faster and more convenient, and you won't have to memorize command syntax! (I hope you are convinced about the superiority of the command panel, because that is what I will use for this tutorial.)

**Open the command panel window by pressing P.**

A new window should appear, and the simulation should pause. On the window, you will see three text fields, titled "Simulation Items", "Simulation Variables" and "Command Buffer". Let's go through each one of them:
- Simulation Items: Everything that exists in the simulated universe can be seen here. The format is \<TYPE\>: \<name\>
- Simulation Variables: Some important and common simulation variables such as time step length (Delta T) can be seen here.
- Command Buffer: All commands scheduled for execution by the command panel once the simulation resumes can be seen here.

[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or3.PNG?raw=true)](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or3.PNG?raw=true)

Your `Command Buffer` window should be clear, and you should be able to see 3 items in the `Simulation Items` box - the planet Earth, and the vessels Yin and Yang. This window makes it easier to keep track of things, especially in large scenarios, so even if you won't enter a command, you could refer to the command panel for reference.

### Creating a Maneuver

But, we DO want to enter a command.

**Click the Enter Command button on the command panel.**

You should now see another window popping up, one with many buttons for the numerous commands available in OS3D. We will shortly be using one of these buttons.

Changing a satellite's orbit usually involves performing an orbital maneuver to change its velocity vector. Let's start planning this orbital maneuver.

**Press Create Maneuver button on the Commands window.**

Yet another window should pop up. There are several entry fields with buttons on the sides, but there is no big red button that reads "Go Higher" or something similar, is there? Of course things aren't that simple - you are here for the mechanics behind going higher (and sometimes lower), not for a joyride. (Once you are comfortable with OS3D and Python, implementing your "Go Higher" button shouldn't be that much of a trouble.)

Anyway, so how do we "go higher" then?

*(Feel more than free to skip the following 3 paragraphs if you are already familiar with orbital mechanics.)* If you paid enough attention, you would have noticed that our satellites were following a circle around planet Earth. That's because the satellites have some sideways speed, but the gravity of Earth is constantly pulling them inwards, curving their path into a circle (actually an ellipse, but in this case it's almost a circle). 

Now, imagine if the satellites had more sideways speed. Earth's gravity wouldn't be enough to curve the trajectory of the satellite inwards in time and the satellite's trajectory would be curved less than before. That would result in the satellite being flung a bit outwards, to a higher altitude. So, what we need to do is to increase the speed of the satellite.

[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/speed.png?raw=true)](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/speed.png?raw=true)

We can increase the sideways speed of the satellite by orienting it into the direction its travelling in, and applying thrust using its engines. The direction the satellite is travelling in is called "prograde". (Yes, start learning some terms.) We need to tell the satellite to rotate into that orientation and use its engines for some time. Let's do that!

We will be creating a constant acceleration maneuver (because that's the simpler type), so we will use the entry fields on the top, those near the "Create Const. Accel. Mnv." button.

While entering things into the entry fields, do NOT use the space character!

**Enter any name for "Maneuver Name" field.** Try to avoid special characters, and use only letters.

**Enter "Yin" for "Vessel Name" field.** That tells OS3D that the vessel that will be performing this maneuver is the satellite named "Yin".

**Enter "Earth" for "Frame of Ref." field.** This tells OS3D what point in space the maneuver calculations will be made relative to, in this case, planet Earth. You will usually use the planet your vessel is orbiting for this field.

**Enter "prograde" in "Orientation" field.** This tells OS3D in which direction the vessel should apply thrust. You could also enter a vector value in here if you wanted.

**Enter "10" in "Acceleration" field.** This sets how much acceleration the vessel should experience due to its engine for the duration of the maneuver. It's unit is [m s-2], meters per second per second. 

For "Start Time" field, you will have to enter when you want the vessel to start executing the maneuver. For this, you will have to refer to `Sim. Time` value which can be found in the command panel main window, in the `Simulation Variables` box.

**Enter your current time + 100 seconds into "Start Time" field.** For example, if your `Sim. Time` value is 253, you should enter 353. This value is in seconds. 

As a Start Time value, you could technically enter any value above your current time, but if you don't put a delay, you would have to rush to the 3D scene to see the maneuver happening. I'm just putting a 100 second delay for convenience.

**Enter "70" in "Duration" field.** Self explanatory - this value tells for how long you want the engines to apply thrust. Unit is, again, seconds.

Once you make sure you've filled all the entry fields, **click once on the "Create Const. Accel. Mnv." button**. Now go and look at the Command Buffer box - it should no longer be empty since your command should now be queued.

[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or4.PNG?raw=true)](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or4.PNG?raw=true)

**Close the "create_maneuver" window.**

### Using the Output Display

We are about to schedule our maneuver to be executed, but the program won't give us much of a feedback since we didn't tell it to. Let's tell it to.

**On the "Commands" window, click on "Show" button.**

Another window should appear, this time for the "show" command. Next to the button that reads "Show Maneuver Data", you will see 3 entry fields. Using that command, we can see the data related to the maneuver we created on the output display.

**Enter the maneuver name in the "Maneuver" field.** Make sure you type in the exact same maneuver name that you used in the create_maneuver command!

**Enter 'params' in the "Data" field.** This will tell OS3D to show us the maneuver parameters.

**Enter anything into "Display Label" field.** This is the name with which the output will appear on the output display. Again, avoid special characters.

**Click once on the Show Maneuver Data button.**

We are not done yet. We don't want to just see the maneuver parameters, we also want to see the state of the maneuver.

**Erase what you've written in "Data" and "Display Label" fields.**

**Enter "state" in "Data" field.**

**Enter something else into "Display Label" field.** Do not use the same display label as the one you already used.

**Click once on the Show Maneuver Data button.**

[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or5.PNG?raw=true)](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/or5.PNG?raw=true)

We are done entering our commands.

**Close the "show" and "Commands" windows.**

As soon as we confirm our commands, the simulation will execute the commands and resume.

**On the main command panel window, click "Confirm Commands and Close".**

The command panel should disappear and the simulation should continue. (If the simulation doesn't resume, it is either processing your commands or you forgot to close some of the command panel windows.) 

You will now see some output on the output display. When the simulation time hits the maneuver start time, the maneuver will begin. The maneuver state will change from "Pending" to "Performing" for 70 simulation seconds, and finally report "Completed" once the maneuver is finished.

![tutogif3](https://user-images.githubusercontent.com/80536083/178112732-74b1c235-8f05-46d7-84d6-5d82a6772a72.gif)

Feel free to roam around the 3D scene as the maneuver happens. While performing the maneuver, you can see that the satellite "Yin" will leave a yellow trail instead of a trail of its own color (which is cyan).

![Imag3](https://user-images.githubusercontent.com/80536083/178112812-bf0b1102-e386-4fbf-8644-3335d4af0add.png)

After a while, you will see "Yin" being flung outwards to a higher altitude, and eventually it will come back to its starting point, completing one orbit, having drawn an ellipse around Earth.

With that, the introductory tutorial is complete. ***Now, you are free to set your own challenges. Here are three suggestions***:

- If you are a newbie, figure out how to "circularize" Yin's orbit (turn the elliptic orbit into a circle) when it reaches the highest altitude it can in its orbit. *Hint: The maneuver you are about to execute will complete what is known as a "Hohmann transfer"! https://en.wikipedia.org/wiki/Hohmann_transfer_orbit*

- If you are a KSP or Orbiter veteran (or a flight dynamics officer), try to rendezvous Yin with Yang, spending the least amount of Delta-V possible! 

- If you are feeling particularly adventurous, program an autopilot to rendezvous Yin with Yang in orbit!

## Cool, what next?

Well, I don't know. It's up to you.

Check out the .osf files in the scenarios folder with your favorite text editor - load in the ones you like and try your skills with the challenge scenarios, or sit back and watch some demo space missions!

Try to discover efficient transfer routes for robotic spacecraft, or fast ways to get people to other planets in the Solar System. Create your own planetary systems and curse imaginary civilizations to three-body problems. Write your own calculators to extend OS3D, and even open a few Pull Requests while you are at it :)
