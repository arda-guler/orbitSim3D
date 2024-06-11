from datetime import datetime, timedelta
import requests
import re

from math_utils import grav_const
from body_class import *
from solver import *
from vector3 import *

def parseJPL(input_string):
    # Regular expressions to match the lines containing the vector components
    position_pattern = re.compile(r'\bX\s*=\s*([+-]?\d+\.\d+E[+-]\d+)\s*Y\s*=\s*([+-]?\d+\.\d+E[+-]\d+)\s*Z\s*=\s*([+-]?\d+\.\d+E[+-]\d+)')
    velocity_pattern = re.compile(r'\bVX\s*=\s*([+-]?\d+\.\d+E[+-]\d+)\s*VY\s*=\s*([+-]?\d+\.\d+E[+-]\d+)\s*VZ\s*=\s*([+-]?\d+\.\d+E[+-]\d+)')

    # Finding all matches in the input string
    position_match = position_pattern.search(input_string)
    velocity_match = velocity_pattern.search(input_string)
    
    if position_match and velocity_match:

        position = vec3(lst=[float(position_match.group(1)),
                             float(position_match.group(2)),
                             float(position_match.group(3))])

        velocity = vec3(lst=[float(velocity_match.group(1)),
                             float(velocity_match.group(2)),
                             float(velocity_match.group(3))])
        
        return [position * 1000, velocity * 1000]
    
    else:
        return None

def getPlanetsJPL(start_time):
    dt_stop_time = start_time + timedelta(days=1)
    stop_time = dt_stop_time.strftime("%Y-%m-%d")
    start_time = start_time.strftime("%Y-%m-%d")
    
    state_vectors = []
    
    for i in range(1, 11): # 1 to 10 for Mercury - Neptune and Sol (10)
        bodyid = i

        url = "https://ssd.jpl.nasa.gov/api/horizons.api"

        url += "?format=text&EPHEM_TYPE=VECTORS&OBJ_DATA=NO&VEC_TABLE=2&CENTER='500@0'"
        url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'&STEP_SIZE='3d'".format(bodyid, start_time, stop_time)

        response = requests.get(url)

        if response.status_code == 200:
            state_vectors.append(parseJPL(response.text))

        elif response.status_code == 400:
            print("Error 400 Bad Request")

        elif response.status_code == 405:
            print("Error 400 Method Not Allowed")

        elif response.status_code == 500:
            print("Error 400 Internal Server Error")

        elif response.status_code == 503:
            print("Error 400 Server Unavailable")

    # print("OK! Got planet state vectors from JPL!")
    return state_vectors

def test_propagator():
    minute = 60
    hour = 60 * 60
    day = 60 * 60 * 24
    year = 365 * day

    ## system setup
    t_0 = datetime(2017, 1, 1, 0, 0, 0)
    t_f = datetime(2022, 1, 1, 0, 0, 0)
    dt = 2 * day
    solvertype = "Yoshida8"

    print("\nORBIT PROPAGATOR TEST - SETUP\n")
    print("Total propagator test run is 5 simulated years long and runs an n-body simulation of major Solar System planets.")
    solvertype = input("Solver type to test (SymplecticEuler, VelocityVerlet, Yoshida4, Yoshida8 (default)): ")
    if not solvertype:
        solvertype = "Yoshida8"

    dt = input("delta_t (seconds, default is 172800): ")
    if not dt:
        dt = 2 * day
    else:
        dt = float(dt)
    
    print("\n\n= = RUNNING ORBIT PROPAGATOR TEST = =")
    print("Solver:", solvertype)
    print("Time Start:", str(t_0))
    print("Time End:", str(t_f))
    print("dt:", dt, "s")
    print("")

    print("Constructing the Solar System at", str(t_0), "...")
    print("Getting state vectors using JPL Horizons API...")
    sv_SolarSystem = getPlanetsJPL(t_0)

    print("Generating bodies...")
    ss_body_names = ["Mercury",
                     "Venus",
                     "Earth",
                     "Mars",
                     "Jupiter",
                     "Saturn",
                     "Uranus",
                     "Neptune",
                     "Sol"]

    sun = body("Sol", None, None, 1.3271244004193938e11 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[9][0], sv_SolarSystem[9][1], # pos, vel
                   None, None, None, None, None, None, None)

    mercury = body("Mercury", None, None, 2.2031780000000021E+04 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[0][0], sv_SolarSystem[0][1], # pos, vel
                   None, None, None, None, None, None, None)

    venus = body("Venus", None, None, 3.2485859200000006E+05 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[1][0], sv_SolarSystem[1][1], # pos, vel
                   None, None, None, None, None, None, None)

    earth = body("Earth", None, None, 4.0350323550225981E+05 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[2][0], sv_SolarSystem[2][1], # pos, vel
                   None, None, None, None, None, None, None)

    mars = body("Mars", None, None, 4.2828375214000022E+04 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[3][0], sv_SolarSystem[3][1], # pos, vel
                   None, None, None, None, None, None, None)

    jupiter = body("Jupiter", None, None, 1.2671276480000021E+08 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[4][0], sv_SolarSystem[4][1], # pos, vel
                   None, None, None, None, None, None, None)

    saturn = body("Saturn", None, None, 3.7940585200000003E+07 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[5][0], sv_SolarSystem[5][1], # pos, vel
                   None, None, None, None, None, None, None)

    uranus = body("Uranus", None, None, 5.7945486000000080E+06 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[6][0], sv_SolarSystem[6][1], # pos, vel
                   None, None, None, None, None, None, None)

    neptune = body("Neptune", None, None, 6.8365271005800236E+06 * 1e9 / grav_const, None, None,
                   sv_SolarSystem[7][0], sv_SolarSystem[7][1], # pos, vel
                   None, None, None, None, None, None, None)

    bodies = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, sun]
    print("Solar System constructed successfully.")

    timeinterval = (t_f - t_0).total_seconds()
    N_cycles = int(timeinterval // dt) + 1;
    t_f_actual = t_0 + timedelta(seconds=N_cycles * dt)
    print("Simulation end time:", str(t_f_actual))

    body_trajs = [[] for b in bodies]
    ts = []

    print("Beginning propagation computations...")
    ## main loop
    for cycle in range(N_cycles):
        t = dt * cycle

        if solvertype == "SymplecticEuler":
            SymplecticEuler(bodies, [], [], [], [], [], [], [], t, dt)

        elif solvertype == "VelocityVerlet":
            VelocityVerlet(bodies, [], [], [], [], [], [], [], t, dt)

        elif solvertype == "Yoshida4":
            Yoshida4(bodies, [], [], [], [], [], [], [], t, dt)

        elif solvertype == "Yoshida8":
            Yoshida8(bodies, [], [], [], [], [], [], [], t, dt)

        for idx_b, b in enumerate(bodies):
            body_trajs[idx_b].append(b.pos)

        ts.append(t)

        if cycle % 100 == 0:
            print("Cycle: ", cycle)
            print("Solution is", str(round(cycle / N_cycles * 100, 2)), "% done.")

    print("Propagation computations done.\n\n")

    ## plotting
##    print("Plotting...")
##    fig = plt.figure()
##    ax = fig.add_subplot(111, projection='3d')
##    for idx_bp, bp in enumerate(body_trajs):
##        x = [pos[0] for pos in bp]
##        y = [pos[1] for pos in bp]
##        z = [pos[2] for pos in bp]
##
##        ax.plot(x, y, z)
##
##    ax.set_xlabel('X')
##    ax.set_ylabel('Y')
##    ax.set_zlabel('Z')
##    ax.set_title('3D Trajectory')
##
##    ax.set_xlim(-5e9, 5e9)
##    ax.set_ylim(-5e9, 5e9)
##    ax.set_zlim(-5e9, 5e9)
##
##    plt.show()

    ## errors
    print("Getting final positions from JPL Horizons to compare...")
    final_sv = getPlanetsJPL(t_f_actual)
    print("Calculating errors...")
    errors = []
    for idx_b, b in enumerate(bodies[:-1]):
            error = vec3(lst=list(final_sv[idx_b][0])) - body_trajs[idx_b][-1]
            errors.append(error)

    print("Planetary position errors:\n")
    for idx_e, e in enumerate(errors):
        print(ss_body_names[idx_e] + ": ", e.mag(), "m")
        print("Mean error accumulation:", e.mag() / (N_cycles * dt), "meter error/second\n")

    input("Test program finished. Press Enter to return...")
