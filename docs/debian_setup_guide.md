# Linux (Debian) Setup Guide

Setting up OS3D shouldn't be difficult enough to require a guide, but regardless, this guide will help you run OrbitSim3D on a Debian-based distro. For this tutorial, a fresh Linux Mint 21.2 MATE was used.

## 1 - Obtaining the Source Code

One can;
- Download the GitHub repository as a ZIP file from [this link](https://github.com/arda-guler/orbitSim3D/archive/refs/heads/master.zip). The source code download links are also available on the [GitHub repository page](https://github.com/arda-guler/orbitSim3D) and the [download page on OS3D website](https://arda-guler.github.io/OrbitSim3D-web/download.html).
- Clone the GitHub repository.

![1-download](https://github.com/arda-guler/orbitSim3D/assets/80536083/8ce0cf7f-1ba6-49f6-95ea-7f7a517b6afc)

![2-download2](https://github.com/arda-guler/orbitSim3D/assets/80536083/09a6ba9b-dde3-474b-bcd1-6e76acd45645)

If you download the source code as a ZIP file, extract it to a convenient location of your choosing.

## 2 - Installing Requirements

The steps below may require administrator access. (sudo)

In case you distro doesn't come with Python3 already installed, you can install it via:

```
apt-get install python3
```

Python3 itself is not enough as OS3D uses several Python packages. Using pip to install them is a convenient method. Install pip itself using:

```
apt-get install python3-pip
```

Python3 on Linux distros does not include the 'tkinter' package which normally comes together with Windows installations of Python. Install it via:

```
apt-get install python3-tk
```

Now we can move onto installing other packages. You can either:

- open a terminal on the orbitSim3D directory and use the requirements.txt file to auto-install them:

```
pip install -r requirements.txt
```

- if a problem occurs for any reason, install them one-by-one by hand, replacing package1 & package2 with package names and x.y.z & a.b.c with package versions as written in requirements.txt:

```
pip install package1==x.y.z
pip install package2==a.b.c
```

## 3 - First Run

Ensure you are in sudo mode and in OrbitSim3D directory.

Run the following to start OS3D.

```
python3 main.py
```

The first run will likely create a `__pycache__` directory in the same path. Leave it be.

If you do not see the main menu at this point, check whether all requirements are installed successfully.

![3-menu](https://github.com/arda-guler/orbitSim3D/assets/80536083/8e2e2746-8c95-4710-a941-cce154c7284f)

It is suggested (but not required) that you type C and press Enter on the first run to configure your keyboard controls and window size.

![4-config](https://github.com/arda-guler/orbitSim3D/assets/80536083/015ef24c-4ee7-4d72-9f38-04633932361b)

You are now ready to use OS3D. Try loading in a premade scenario and see if it works.

## 4- Troubleshooting Tips

- While working on the requirements, make sure you use 'python3' instead of 'python' and work in a case-sensitive manner to eliminate any typo doubts.
- Use the versions of the packages exactly as provided in requirements.txt. As the related packages are developed further, some key functionalities may undergo changes that may break how OS3D works.
- The 'keyboard' package in particular can be a little touchy. Try a default keyboard layout (like a US qwerty) if it throws out any errors.
- Make sure you are running main.py in sudo mode.
- Make sure your terminal display has enough character space per line to display the outputs correctly.
- `utilities` folder and its contents are not required for OS3D to function. It can safely be ignored, and a failure of any of the scripts in that folder will not affect OS3D.
- Trying to run OS3D in a Docker environment may result in PyOpenGL or glfw to not work properly.
