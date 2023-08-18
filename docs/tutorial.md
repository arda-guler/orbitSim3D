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

![TUT1](https://github.com/arda-guler/orbitSim3D/assets/80536083/14861563-8c34-4eea-9fb8-06a2a85ad5a6)

You should be seeing four options - one for resuming the latest scenario, one for loading a scenario, one for starting an empty scene and the last one for configuring OS3D. 

***You can configure your keyboard controls the way you like, but please don't touch any other configuration variables if you don't know what you are doing. Close the config editor window when you are done, and return to initialization menu.***

In order to simulate a system, OS3D first needs to know about the initial states of the celestial bodies and spacecraft you want to simulate. Such data is kept in .osf files (usually in the `scenarios/` folder) in plain text format, but creating a scenario from scratch can sometimes be a bit too much work due to the strict formatting requirements (I should do something about that sometime). I know you are eager to fly spaceships, so let's skip the boring part now and load one of the scenarios I prepared beforehand.

**Choose the first option in the initialization menu by either typing '1' or 'L' and pressing Enter, which will let you choose the scenario to load.**

![tut4](https://github.com/arda-guler/orbitSim3D/assets/80536083/82a7207a-2319-4259-9666-3c5395151648)

The program will ask for the scenario filename next. You could of course type in the name of any scenario, but for the purposes of this tutorial, I will ask you to load a specific scenario.

**Type in 'two_mirrors' and press Enter to load the scenario.**

![tut5](https://github.com/arda-guler/orbitSim3D/assets/80536083/01bf9bdb-3e48-4054-91c9-1c90750a5b92)

The program will quickly load the scenario, and a second window will appear. The command prompt (terminal) will act as the numerical output display as well as the command interpreter, whereas the OpenGL window will act as the 3D rendering canvas.

### A First Look at the Simulated Universe

![tut6](https://github.com/arda-guler/orbitSim3D/assets/80536083/ef7ed75f-8630-489b-9769-d3d6c25fef6e)

If you look at the OpenGL window, you will see a blue orb and two objects next to it leaving trails as they move around. The beautiful blue orb is planet Earth, and the two objects (one magenta and one cyan) are two imaginary satellites orbiting Earth.

***Arrange (drag & resize) the two windows the way you like. I personally did it like the one above.***

***Try moving the camera around the scene, rotate and translate your viewpoint.***

If you get close enough to either one of the satellites, you will be able to see their 3D models. Note that there are no collision checks for the camera, and it might pass through the Earth, creating weird graphical effects. In that case, just translate your camera backwards until you are out of the planet.

Once you are done playing with the camera and pretending you are a WWII fighter in space, let's get to business.

### Controlling the Simulation

The simulated spacecraft (actually the whole simulation) can be controlled via two methods, which are actually the same method but with different aesthetics;
- Using the command line (makes you look cool)
- Using the command panel (helps you keep your cool)

Notice the only difference between the above options are the words 'line' and 'panel' - they do the same thing in different ways. The command line is, well, a command line, just like the one in, say, DOS. Command panel is a graphical tool; so if the command line is analogous to MS-DOS, the command panel is analogous to Windows 3. I think you get the idea.

Now, you can use whichever one of these options you like, but I suggest that you go with the command panel since it will make your life a hundred times easier. It is many times faster and more convenient, and you won't have to memorize command syntax! (I hope you are convinced about the superiority of the command panel, because that is what I will use for this tutorial.)

**Open the command panel window by pressing P.**

![tut7](https://github.com/arda-guler/orbitSim3D/assets/80536083/48a02add-7c39-46cd-87ed-055102670157)

A new window should appear, and the simulation should pause. On the window, you will see three text fields, titled "Simulation Items", "Simulation Variables" and "Command Buffer". Let's go through each one of them:
- Simulation Items: Everything that exists in the simulated universe can be seen here. The format is \<TYPE\>: \<name\>
- Simulation Variables: Some important and common simulation variables such as time step length (Delta T) can be seen here.
- Command Buffer: All commands scheduled for execution by the command panel once the simulation resumes can be seen here.

Your `Command Buffer` window should be clear, and you should be able to see 4 items in the `Simulation Items` box - the planet Earth, and the vessels Yin and Yang, and a resource named 'target_signal' - don't worry about what the latter is right now. This window makes it easier to keep track of things, especially in large scenarios, so even if you won't enter a command, you could refer to the command panel for reference.

### Displaying Output

We wish to enter commands using the command panel. You see, on the bottom output window, we have no outputs displayed other than the simulated time. Let's populate that space with some useful things, by displaying a satellite's velocity and altitude above Earth.

**Press the Enter Command button on the command panel.**

![tut8](https://github.com/arda-guler/orbitSim3D/assets/80536083/58983fb6-3158-47d3-beb9-2e2a232e4666)

This will open a new window named 'Commands'. That is a list of all commands we can enter using the command panel. The first command we will use is an output management command, and is therefore placed in the Output Management category. The 'show' command is what we are looking for. (At any time you wish to learn what a command does, you can click on the button and read the info text about it. Apart from a few, a lot of the command names are self-explanatory.)

**Press the Show button on the 'Commands' window.**

![tut9](https://github.com/arda-guler/orbitSim3D/assets/80536083/a96032f9-c170-4663-8c2e-dbdeb4a660fe)

Now, yet another window will pop-up. Don't worry, this is the highest number of windows you will have to have open at any time.

The 'show' command is a pretty universal command, so there are a lot of alternative syntax options to use it. Currently, we will use it to display a relative variable, so we will use the appropriate row on inputs next to the 'Show Relative Variable' button.

**Enter 'Yin' in Object field.** This is the object about which we wish to display information.

**Enter 'vel_mag' in Variable field.** This is the variable we wish to display. If we typed 'vel', we would display the velocity in three vector components. 'vel_mag' just shows the velocity magnitude.

**Enter 'Earth' in Frame of Ref. field.** This is the Frame of Reference relative to which the variable is calculated. In this case, that is the planet Earth.

**Enter any name you wish in Display Label field.** Avoid spaces and special characters. This will be the title of the variable in the output display.

**Press once on the Show Relative Variable button.**

In the command buffer field, a new command should appear.

![tut10](https://github.com/arda-guler/orbitSim3D/assets/80536083/7e47d252-247f-410c-a749-4c61655f88e0)

This command should display the satellite Yin's velocity relative to Earth on the output display. We also wanted to see its altitude above Earth, so let's also do that.

**Delete 'vel_mag' in Variable field and enter 'alt'.** This means we now want to display the altitude (above sea level).

**Clear the Display Label field and enter a new name for the new variable.** Avoid using the same display label for multiple variables.

**Press once on the Show Relative Variable button.**

On the command buffer window, a second command should appear.

![tut11](https://github.com/arda-guler/orbitSim3D/assets/80536083/0fc366f2-6e24-4d1b-8ba7-64bf972807a6)

Now that we have entered our commands, we should resume the simulation so that they will be executed and the output display will be modified.

**Close 'show' window.**

**Close 'Commands' window.**

**Click on 'Confirm Commands and Close' button.**

![tut12](https://github.com/arda-guler/orbitSim3D/assets/80536083/f46d52fc-720a-477b-84a6-f2c56b66e87d)

As soon as the simulation resumes, we will see the outputs on the output display.

![tut13](https://github.com/arda-guler/orbitSim3D/assets/80536083/1bc8867f-b8bc-41ab-bf5f-181294e891a8)

The standard variables are all displayed in SI units - meaning that the velocity output is in meters per second and the altitude output is in meters. If you make use of the simulation items called 'resources', you can also output variables in different units, but that's a bit too advanced for an introductory tutorial. 

Speaking of resources, we have a resource called 'target_signal' in this scenario that's already set up for you. Using the knowledge you learned just now on entering commands, how would you display the value of 'target_signal'?

***Enter a new command using the command panel and display the value of 'target_signal' resource.***

![tut14](https://github.com/arda-guler/orbitSim3D/assets/80536083/3b06e7f7-cf0d-4d70-9021-203789c0ec6c)

### Performing an Orbital Maneuver

We don't simply want to look at satellites and see them going on in their orbits. OS3D is made to be a space mission simulator after all, and we wish to control the spacecraft. Let's perform an orbital maneuver and modify Yin's orbit around Earth.

**Open the 'create_maneuver' command window.** You can do this the same way you opened the 'show' command window.

![tut15](https://github.com/arda-guler/orbitSim3D/assets/80536083/33117c3e-aef1-4fa4-9364-3e9ec6149287)

I wish to increase the altitude of Yin's orbit around Earth. How do we go about that? There is no "Go Higher" button in here! How do we "Go Higher" then?

*(Feel more than free to skip the following 3 paragraphs if you are already familiar with orbital mechanics.)* If you paid enough attention, you would have noticed that our satellites were following a circle around planet Earth. That's because the satellites have some sideways speed, but the gravity of Earth is constantly pulling them inwards, curving their path into a circle (actually an ellipse, but in this case it's almost a circle). 

Now, imagine if the satellites had more sideways speed. Earth's gravity wouldn't be enough to curve the trajectory of the satellite inwards in time and the satellite's trajectory would be curved less than before. That would result in the satellite being flung a bit outwards, to a higher altitude. So, what we need to do is to increase the speed of the satellite.

[![](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/speed.png?raw=true)](https://github.com/arda-guler/arda-guler.github.io/blob/master/extrn_storage/OS3D/intro_tutorial/speed.png?raw=true)

We can increase the sideways speed of the satellite by orienting it into the direction its travelling in, and applying thrust using its engines. The direction the satellite is travelling in is called "prograde". (Yes, start learning some terms.) We need to tell the satellite to rotate into that orientation and use its engines to change its orbital velocity. Let's do that!

We will be creating an impulsive maneuver (because that's the simplest type), so we will use the entry fields near the "Create Impulsive Mnv." button.

**Enter any name for "Maneuver Name" field.** Try to avoid special characters, and use only letters.

**Enter "Yin" for "Vessel Name" field.** That tells OS3D that the vessel that will be performing this maneuver is the satellite named "Yin".

**Enter "Earth" for "Frame of Ref." field.** This tells OS3D what point in space the maneuver calculations will be made relative to, in this case, planet Earth. You will usually use the planet your vessel is orbiting for this field.

**Enter "prograde" in "Orientation" field.** This tells OS3D in which direction the vessel should apply thrust. You could also enter a vector value in here if you wanted.

**Enter "1500" in "Delta-v" field.** This sets by how much we want to modify our orbital velocity. The unit is in meters per second, of course.

For "Perform Time" field, you will have to enter when you want the vessel to execute the maneuver. For this, you will have to refer to `Sim. Time` value which can be found in the command panel main window, in the `Simulation Variables` box.

**Enter your current Sim. Time + 150 seconds into "Perform Time" field.** For example, if your `Sim. Time` value is 850, you should enter 1000. This value is in seconds. 

As a Perform Time value, you could technically enter any value above your current time, but if you don't put a delay, you would have to rush to the 3D scene to see the maneuver happening. I'm just putting a 150 second delay for convenience.

Once you make sure you've filled all the entry fields, **click once on the "Create Impulsive Mnv." button**. Now go and look at the Command Buffer box - it should no longer be empty since your command should now be queued.

![tut16](https://github.com/arda-guler/orbitSim3D/assets/80536083/1da501fa-5eae-4742-9d89-1494c709fd54)

**Close the "create_maneuver" window.**

This command will schedule an impulsive maneuver to be executed by the satellite Yin, but the output display won't display any information about it since we didn't tell it to. Let's tell it to.

**Show maneuver parameters using the 'show' command.** Look at the screenshot below if you are stuck.

![tut17](https://github.com/arda-guler/orbitSim3D/assets/80536083/78f2bdbb-0aa1-4c7f-abd6-25a2e5947dd2)

**Show maneuver state, again using the 'show' command.** Look at the screenshot below if you are stuck.

![tut18](https://github.com/arda-guler/orbitSim3D/assets/80536083/c0f331d7-08dd-4c3a-8586-53011f3d57bc)

**Close 'show' and 'Commands' windows.**

**'Confirm Commands and Close' the command panel.** As before, like we did the first time when we learned how to use the 'show' command.

The output window will be further modified to display the information regarding the scheduled impulsive maneuver.

![tut19](https://github.com/arda-guler/orbitSim3D/assets/80536083/328709f5-bc6f-480e-a889-d74c7cde0093)

The maneuver state will read 'Pending' until simulation time hits 1000 (or whatever time you have set), after which, the satellite Yin will leave a magenta square on its trajectory line and the maneuver state will switch to 'Completed'. You will also see a dramatic increase in Yin's velocity, from about 7500 m/s to something over 9000 m/s.

![tut20](https://github.com/arda-guler/orbitSim3D/assets/80536083/0ecfce59-9d1a-4387-9baa-f801416a6a3b)

We can now wait until the n-body propagator computes a whole orbit and Yin completes a full elliptical orbit around the Earth. But, since this is a two-body problem (in this particular scenario, no distant bodies are in the simulation and Earth is assumed a uniform mass), we can also use a Keplerian two-body model. This is called an "orbit projection". Let's create one.

**Open the command panel and open the window for the command 'create_projection'.**

![tut21](https://github.com/arda-guler/orbitSim3D/assets/80536083/6919dcc8-9414-4fd1-9a84-93536723aa35)

**Enter any name for the projection.** Again, avoid spaces and special characters.

**Enter 'Yin' for Satellite field.**

**Enter 'Earth' for Parent Body field.**

**Press once onto Create Projection button.**

![tut22](https://github.com/arda-guler/orbitSim3D/assets/80536083/5039072f-3dd8-43a1-a662-ae1794872d7e)

**Close the 'create_projection' window.**

This will project the two-body orbit onto the 3D scene, but we could also use some orbital parameters on the numerical output display.

**Use the 'show' command to display orbit projection parameters.** Refer to the screenshot below if you are stuck.

![tut23](https://github.com/arda-guler/orbitSim3D/assets/80536083/af84a016-4c47-4e59-b89d-9e674c172c0f)

**Close the command windows, 'Confirm Commands and Close' the command panel.** ...as we did before.

When the simulation resumes, a dashed orbit will appear in the 3D rendering scene, along with ascending/descending nodes and apoapsis/periapsis. (Since Yin's orbit has 0 inclination, ascending and descending nodes are arbitrary.)

![tut24](https://github.com/arda-guler/orbitSim3D/assets/80536083/4faf407d-b144-4f1d-964d-498fa19193e6)

While reading apoapsis and periapsis, it is important to distinguish the R and Alt values - former being the distance from the center of mass of the parent body and the latter being the altitude above sea level.

We have learned how to display a lot of information on the screen, but how do we get rid of the unnecessary stuff? We use the 'hide' command!

**Use the 'hide' command to hide the output elements related to the impulsive maneuver.** Refer to the screenshot below if you are stuck.

![tut25](https://github.com/arda-guler/orbitSim3D/assets/80536083/54e735bc-60b4-4ec1-956e-39cc1bc03b84)

When you confirm the commands, the output display will be modified so that some information is no longer displayed, reducing clutter.

### Timed Commands

Let's do one last thing. All the commands we entered so far were executed as soon as we confirmed them and resumed the simulation. What do we do if we want to set a specific time for their execution?

**Open the 'show' command window.**

**Press once on 'Show Grid' button.** This command requires no text inputs, simply pressing on the button is enough.

**Close the 'show' command window and the 'Commands' window. DO NOT CONFIRM THE COMMANDS YET!**

![tut26](https://github.com/arda-guler/orbitSim3D/assets/80536083/e7882c9c-d715-4702-a459-8c33163e9a04)

**Press the 'Asgn. Exec. Time' button.** This will open a new window.

**Enter 0 into the Cmd. Index field.** Since there is only one command in the command buffer, it will be at index 0. You can see the index of each command on the buffer as the leftmost character.

**Enter any time above the current simulation time into Exec. Time field.**

**Press Assign Time button.** This should modify the command on the command buffer so that it will have a leading 't=' expression in front of it. That expression shows at what simulation time the command will be executed.

![tut27](https://github.com/arda-guler/orbitSim3D/assets/80536083/7c946b53-0467-4e7b-93aa-044e69d76809)

**Close 'Assign Command Execution Time' window.**

**'Confirm Commands and Close' the command panel.**

When the assigned execution time is reached, the 3D scene should start displaying a grid on the XZ plane, with lines to show objects' elevation in the Y axis.

![tut28](https://github.com/arda-guler/orbitSim3D/assets/80536083/346bfb12-5f78-4f00-97a0-cfe6f80c66f6)

### What's Next?

With that, the introductory tutorial is complete. ***Now, you are free to set your own challenges. Here are three suggestions***:

- If you are a newbie, figure out how to "circularize" Yin's orbit (turn the elliptic orbit into a circle) when it reaches the highest altitude it can in its orbit. *Hint: The maneuver you are about to execute will complete what is known as a "Hohmann transfer"! https://en.wikipedia.org/wiki/Hohmann_transfer_orbit*

- If you are a KSP or Orbiter veteran (or a flight dynamics officer), try to rendezvous Yin with Yang, spending the least amount of Delta-V possible! 

- If you are feeling particularly adventurous, program an autopilot to rendezvous Yin with Yang in orbit!

Check out the [Example Scenarios](https://github.com/arda-guler/orbitSim3D/blob/master/docs/MANUAL_SCENARIOS.md#example-scenarios) with your favorite text editor - load in the ones you like and try your skills with the challenge scenarios, or sit back and watch some demo space missions!

Try to discover efficient transfer routes for robotic spacecraft, or fast ways to get people to other planets in the Solar System. Create your own planetary systems and curse imaginary civilizations to three-body problems. Write your own calculators to extend OS3D, and even open a few Pull Requests while you are at it :)
