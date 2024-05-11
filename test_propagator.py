import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from skyfield.api import load, PlanetaryConstants

from math_utils import grav_const
from body_class import *
from solver import *
from vector3 import *

def get_state_vectors(date_time):
    planets = load('data/ephemeris/de421.bsp')

    ts = load.timescale()
    t = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)
    
    sun = planets['sun']
    mercury = planets['mercury barycenter']
    venus = planets['venus barycenter']
    earth = planets['earth barycenter']
    mars = planets['mars barycenter']
    jupiter = planets['jupiter barycenter']
    saturn = planets['saturn barycenter']
    uranus = planets['uranus barycenter']
    neptune = planets['neptune barycenter']

    km_to_m = 1000  # Convert kilometers to meters
    km_per_s_to_m_per_s = 1000  # Convert kilometers per second to meters per second

    sun_pos, sun_vel = sun.at(t).position.km * km_to_m, sun.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    mercury_pos, mercury_vel = mercury.at(t).position.km * km_to_m, mercury.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    venus_pos, venus_vel = venus.at(t).position.km * km_to_m, venus.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    earth_pos, earth_vel = earth.at(t).position.km * km_to_m, earth.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    mars_pos, mars_vel = mars.at(t).position.km * km_to_m, mars.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    jupiter_pos, jupiter_vel = jupiter.at(t).position.km * km_to_m, jupiter.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    saturn_pos, saturn_vel = saturn.at(t).position.km * km_to_m, saturn.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    uranus_pos, uranus_vel = uranus.at(t).position.km * km_to_m, uranus.at(t).velocity.km_per_s * km_per_s_to_m_per_s
    neptune_pos, neptune_vel = neptune.at(t).position.km * km_to_m, neptune.at(t).velocity.km_per_s * km_per_s_to_m_per_s

    state_vectors = [
        (sun_pos, sun_vel),
        (mercury_pos, mercury_vel),
        (venus_pos, venus_vel),
        (earth_pos, earth_vel),
        (mars_pos, mars_vel),
        (jupiter_pos, jupiter_vel),
        (saturn_pos, saturn_vel),
        (uranus_pos, uranus_vel),
        (neptune_pos, neptune_vel)
    ]

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
    print("Getting state vectors...")
    sv_SolarSystem = get_state_vectors(t_0)

    print("Generating bodies...")
    ss_body_names = ["Sun",
                     "Mercury",
                     "Venus",
                     "Earth",
                     "Mars",
                     "Jupiter",
                     "Saturn",
                     "Uranus",
                     "Neptune"]

    sun = body("Sol", None, None, 1.3271244004193938e11 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[0][0])), vec3(lst=list(sv_SolarSystem[0][1])), # pos, vel
                   None, None, None, None, None, None, None)

    mercury = body("Mercury", None, None, 2.2031780000000021E+04 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[1][0])), vec3(lst=list(sv_SolarSystem[1][1])), # pos, vel
                   None, None, None, None, None, None, None)

    venus = body("Sol", None, None, 3.2485859200000006E+05 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[2][0])), vec3(lst=list(sv_SolarSystem[2][1])), # pos, vel
                   None, None, None, None, None, None, None)

    earth = body("Sol", None, None, 4.0350323550225981E+05 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[3][0])), vec3(lst=list(sv_SolarSystem[3][1])), # pos, vel
                   None, None, None, None, None, None, None)

    mars = body("Sol", None, None, 4.2828375214000022E+04 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[4][0])), vec3(lst=list(sv_SolarSystem[4][1])), # pos, vel
                   None, None, None, None, None, None, None)

    jupiter = body("Sol", None, None, 1.2671276480000021E+08 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[5][0])), vec3(lst=list(sv_SolarSystem[5][1])), # pos, vel
                   None, None, None, None, None, None, None)

    saturn = body("Sol", None, None, 3.7940585200000003E+07 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[6][0])), vec3(lst=list(sv_SolarSystem[6][1])), # pos, vel
                   None, None, None, None, None, None, None)

    uranus = body("Sol", None, None, 5.7945486000000080E+06 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[7][0])), vec3(lst=list(sv_SolarSystem[7][1])), # pos, vel
                   None, None, None, None, None, None, None)

    neptune = body("Sol", None, None, 6.8365271005800236E+06 * 1e9 / grav_const, None, None,
                   vec3(lst=list(sv_SolarSystem[8][0])), vec3(lst=list(sv_SolarSystem[8][1])), # pos, vel
                   None, None, None, None, None, None, None)

    bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
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
    final_sv = get_state_vectors(t_f_actual)
    errors = []
    for idx_b, b in enumerate(bodies):
            error = vec3(lst=list(final_sv[idx_b][0])) - body_trajs[idx_b][-1]
            errors.append(error)

    print("Planetary position errors:\n")
    for idx_e, e in enumerate(errors):
        print(ss_body_names[idx_e] + ": ", e.mag(), "m")
        print("Mean error accumulation:", e.mag() / (N_cycles * dt), "meter error/second\n")

    input("Test program finished. Press Enter to return...")

##if __name__ == "__main__":
##    test_propagator()
    
