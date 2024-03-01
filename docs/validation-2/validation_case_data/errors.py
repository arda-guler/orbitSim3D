import numpy as np
import matplotlib.pyplot as plt

errors_euler_no_harmonics = []
errors_euler_w_harmonics = []
errors_Y8_no_harmonics = []
errors_Y8_w_harmonics = []

errors_euler_w_harmonics_fast = []
errors_Y8_w_harmonics_fast = []

# DAY 0.5 data
jpl_horizons = np.array([-3.867065644022405E+06, 3.120883355379895E+06, -4.623456266143041E+06])
euler_no_harmonics = np.array([-4048840, 3092437, -4484887])
euler_w_harmonics = np.array([-3862814, 3108569, -4641735])
Y8_no_harmonics = np.array([-4044629, 3086574, -4486958])
Y8_w_harmonics = np.array([-3858595, 3102830, -4643489])

euler_w_harmonics_fast = np.array([-3464966, 2687960, -5056544])
Y8_w_harmonics_fast = np.array([-4088042, 3998740, -2790325])

error_euler_no_harmonics = np.linalg.norm(euler_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_euler_w_harmonics = np.linalg.norm(euler_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_no_harmonics = np.linalg.norm(Y8_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics = np.linalg.norm(Y8_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)

error_euler_w_harmonics_fast = np.linalg.norm(euler_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics_fast = np.linalg.norm(Y8_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)

errors_euler_no_harmonics.append(error_euler_no_harmonics)
errors_euler_w_harmonics.append(error_euler_w_harmonics)
errors_Y8_no_harmonics.append(error_Y8_no_harmonics)
errors_Y8_w_harmonics.append(error_Y8_w_harmonics)

errors_euler_w_harmonics_fast.append(error_euler_w_harmonics_fast)
errors_Y8_w_harmonics_fast.append(error_Y8_w_harmonics_fast)

orbits = 43200 / 5574
print("0.5 days (43200 seconds) integration (around " + str(int(orbits)) + " orbits):")
print("dt=1s")
print("Error: Euler w/out J2:", error_euler_no_harmonics * 100, "%")
print("Error: Euler w/ J2:", error_euler_w_harmonics * 100, "%")
print("Error: Yoshida8 w/out J2:", error_Y8_no_harmonics * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics * 100, "%")
print("\ndt=100s")
print("Error: Euler w/ J2:", error_euler_w_harmonics_fast * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics_fast * 100, "%")

# DAY 1 Data
jpl_horizons = np.array([1940112, -3887283, -5220947])
euler_no_harmonics = np.array([1539995, -3935463, -5314065])
euler_w_harmonics = np.array([1963949, -3909382, -5197810])
Y8_no_harmonics = np.array([1510394, -3942587, -5305060])
Y8_w_harmonics = np.array([1971682, -3916295, -5188770])

euler_w_harmonics_fast = np.array([3742344, -5123108, -3600976])
Y8_w_harmonics_fast = np.array([1508935, -3000997, -6298194])

error_euler_no_harmonics = np.linalg.norm(euler_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_euler_w_harmonics = np.linalg.norm(euler_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_no_harmonics = np.linalg.norm(Y8_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics = np.linalg.norm(Y8_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)

error_euler_w_harmonics_fast = np.linalg.norm(euler_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics_fast = np.linalg.norm(Y8_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)

errors_euler_no_harmonics.append(error_euler_no_harmonics)
errors_euler_w_harmonics.append(error_euler_w_harmonics)
errors_Y8_no_harmonics.append(error_Y8_no_harmonics)
errors_Y8_w_harmonics.append(error_Y8_w_harmonics)

errors_euler_w_harmonics_fast.append(error_euler_w_harmonics_fast)
errors_Y8_w_harmonics_fast.append(error_Y8_w_harmonics_fast)

orbits = 86400 / 5574
print("\n\n1 day (86400 seconds) integration (around " + str(int(orbits)) + " orbits):")
print("dt=1s")
print("Error: Euler w/out J2:", error_euler_no_harmonics * 100, "%")
print("Error: Euler w/ J2:", error_euler_w_harmonics * 100, "%")
print("Error: Yoshida8 w/out J2:", error_Y8_no_harmonics * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics * 100, "%")
print("\ndt=100s")
print("Error: Euler w/ J2:", error_euler_w_harmonics_fast * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics_fast * 100, "%")

# DAY 2 Data
jpl_horizons = np.array([-1434906, 2870024, 5873599])
euler_no_harmonics = np.array([-526916, 3009896, 6050060])
euler_w_harmonics = np.array([-1506199, 2948630, 5914922])
Y8_no_harmonics = np.array([-526736, 3010350, 6051765])
Y8_w_harmonics = np.array([-1505013, 2947568, 5917245])

euler_w_harmonics_fast = np.array([-4029956, 4642344, -2464983])
Y8_w_harmonics_fast = np.array([-1033966, 1868668, 6655742])

error_euler_no_harmonics = np.linalg.norm(euler_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_euler_w_harmonics = np.linalg.norm(euler_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_no_harmonics = np.linalg.norm(Y8_no_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics = np.linalg.norm(Y8_w_harmonics - jpl_horizons) / np.linalg.norm(jpl_horizons)

error_euler_w_harmonics_fast = np.linalg.norm(euler_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)
error_Y8_w_harmonics_fast = np.linalg.norm(Y8_w_harmonics_fast - jpl_horizons) / np.linalg.norm(jpl_horizons)

errors_euler_no_harmonics.append(error_euler_no_harmonics)
errors_euler_w_harmonics.append(error_euler_w_harmonics)
errors_Y8_no_harmonics.append(error_Y8_no_harmonics)
errors_Y8_w_harmonics.append(error_Y8_w_harmonics)

errors_euler_w_harmonics_fast.append(error_euler_w_harmonics_fast)
errors_Y8_w_harmonics_fast.append(error_Y8_w_harmonics_fast)

orbits = 172800 / 5574
print("\n\n2 days (172800 seconds) integration (around " + str(int(orbits)) + " orbits):")
print("dt=1s")
print("Error: Euler w/out J2:", error_euler_no_harmonics * 100, "%")
print("Error: Euler w/ J2:", error_euler_w_harmonics * 100, "%")
print("Error: Yoshida8 w/out J2:", error_Y8_no_harmonics * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics * 100, "%")
print("\ndt=100s")
print("Error: Euler w/ J2:", error_euler_w_harmonics_fast * 100, "%")
print("Error: Yoshida8 w/ J2:", error_Y8_w_harmonics_fast * 100, "%")

## PLOTS
xs = [0.5, 1, 2]
plt.scatter(xs, errors_euler_no_harmonics, label="Euler w/out J2")
plt.scatter(xs, errors_euler_w_harmonics, label="Euler w/ J2")
plt.scatter(xs, errors_Y8_no_harmonics, label="Yoshida8 w/out J2")
plt.scatter(xs, errors_Y8_w_harmonics, label="Yoshida8 w/ J2")
plt.scatter(xs, errors_euler_w_harmonics_fast, label="Euler w/ J2, dt=100 J2")
plt.scatter(xs, errors_Y8_w_harmonics_fast, label="Yoshida8 2/ J2, dt=100 J2")

plt.plot(xs, errors_euler_no_harmonics, linestyle="--")
plt.plot(xs, errors_euler_w_harmonics, linestyle="--")
plt.plot(xs, errors_Y8_no_harmonics, linestyle="--")
plt.plot(xs, errors_Y8_w_harmonics, linestyle="--")
plt.plot(xs, errors_euler_w_harmonics_fast, linestyle="--")
plt.plot(xs, errors_Y8_w_harmonics_fast, linestyle="--")

plt.legend()
plt.grid()
plt.title("Position Errors for Geocentric ISS Orbit Propagation")
plt.xlabel("Sim. Time (days)")
plt.ylabel("Position Error rel. to JPL Horizons")
plt.show()
