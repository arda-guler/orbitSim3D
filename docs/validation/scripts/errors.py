import matplotlib.pyplot as plt
from vector3 import *

# 1000 seconds step time
# 31580001 second total simulation time
# Yoshida 4th order solver

errors_1 = []

print("Validation 1: Yoshida8, dt=1e3, t=31580001")
# neptune
o = vec3(2789067214512.079, -3534979223828.3657, 8519379978.046341)
j = vec3(2788885248756.336, -3535125337454.775, 8526582469.79332)

percent_error = (o-j).mag()/j.mag() * 100
print("Neptune position error: ", percent_error, "%")
errors_1.append(percent_error)

# uranus
o = vec3(2428902638950.004, -1744089364070.5247, -37950326552.61882)
j = vec3(2428733974024.8896, -1744313590807.525, -37948974543.52105)

percent_error = (o-j).mag()/j.mag() * 100
print("Uranus position error: ", percent_error, "%")
errors_1.append(percent_error)

# saturn
o = vec3(406671021977.5133, 1291824178208.865, -38660400064.47563)
j = vec3(407089165759.04083, 1291700311281.2312, -38674884589.528984)

percent_error = (o-j).mag()/j.mag() * 100
print("Saturn position error: ", percent_error, "%")
errors_1.append(percent_error)

# jupiter
o = vec3(-142925756858.69147, 759472419089.8153, 48227348.45285048)
j = vec3(-142366551703.1861, 759549407369.1082, 35393837.29743958)

percent_error = (o-j).mag()/j.mag() * 100
print("Jupiter position error: ", percent_error, "%")
errors_1.append(percent_error)

# mars
o = vec3(190750142724.27002, 94041330142.17424, -2693840946.3693166)
j = vec3(191170783785.0864, 93017918832.48232, -2725613710.134409)

percent_error = (o-j).mag()/j.mag() * 100
print("Mars position error: ", percent_error, "%")
errors_1.append(percent_error)

# earth
o = vec3(-27979185986.772083, 143625072724.8678, 11424873.401037496)
j = vec3(-26699407658.071312, 143866032238.2885, 11434931.332379581)

percent_error = (o-j).mag()/j.mag() * 100
print("Earth position error: ", percent_error, "%")
errors_1.append(percent_error)

# venus
o = vec3(6574840572.087595, -109394585547.7853, -1864721670.9855866)
j = vec3(5079584881.556118, -109473191238.0248, -1779519318.029396)

percent_error = (o-j).mag()/j.mag() * 100
print("Venus position error: ", percent_error, "%")
errors_1.append(percent_error)

# mercury
o = vec3(53030349963.334656, -19996498579.272472, -6441168470.113907)
j = vec3(52693155692.55486, -22050074935.34043, -6578024568.097363)

percent_error = (o-j).mag()/j.mag() * 100
print("Mercury position error: ", percent_error, "%")
errors_1.append(percent_error)

print("")
# 500 seconds constant step time
# 31579501 second total simulation time (1 year)
# Yoshida 4th order solver

errors_2 = []

print("Validation 2: Yoshida4, dt=5e2, t=31579501")
# neptune
o = vec3(2789067214505.7344, -3534979223833.533, 8519379978.298835)
j = vec3(2788885248756.336, -3535125337454.775, 8526582469.79332)

percent_error = (o-j).mag()/j.mag() * 100
print("Neptune position error: ", percent_error, "%")
errors_2.append(percent_error)

# uranus
o = vec3(2428902638944.024, -1744089364078.3171, -37950326552.57344)
j = vec3(2428733974024.8896, -1744313590807.525, -37948974543.52105)

percent_error = (o-j).mag()/j.mag() * 100
print("Uranus position error: ", percent_error, "%")
errors_2.append(percent_error)

# saturn
o = vec3(406671021992.1337, 1291824178204.5535, -38660400064.98214)
j = vec3(407089165759.04083, 1291700311281.2312, -38674884589.528984)

percent_error = (o-j).mag()/j.mag() * 100
print("Saturn position error: ", percent_error, "%")
errors_2.append(percent_error)

# jupiter
o = vec3(-142925756839.18246, 759472419092.5338, 48227348.005186036)
j = vec3(-142366551703.1861, 759549407369.1082, 35393837.29743958)

percent_error = (o-j).mag()/j.mag() * 100
print("Jupiter position error: ", percent_error, "%")
errors_2.append(percent_error)

# mars
o = vec3(190750142739.01932, 94041330106.51439, -2693840947.478943)
j = vec3(191170783785.0864, 93017918832.48232, -2725613710.134409)

percent_error = (o-j).mag()/j.mag() * 100
print("Mars position error: ", percent_error, "%")
errors_2.append(percent_error)

# earth
o = vec3(-27979185942.23553, 143625072733.45483, 11424873.401555413)
j = vec3(-26699407658.071312, 143866032238.2885, 11434931.332379581)

percent_error = (o-j).mag()/j.mag() * 100
print("Earth position error: ", percent_error, "%")
errors_2.append(percent_error)

# venus
o = vec3(6574840520.025574, -109394585550.88002, -1864721668.023783)
j = vec3(5079584881.556118, -109473191238.0248, -1779519318.029396)

percent_error = (o-j).mag()/j.mag() * 100
print("Venus position error: ", percent_error, "%")
errors_2.append(percent_error)

# mercury
o = vec3(53030349953.048256, -19996498650.862885, -6441168475.019621)
j = vec3(52693155692.55486, -22050074935.34043, -6578024568.097363)

percent_error = (o-j).mag()/j.mag() * 100
print("Mercury position error: ", percent_error, "%")
errors_2.append(percent_error)

print("")
# 1000 seconds constant step time
# 31580001 second total simulation time
# Symplectic Euler solver

errors_3 = []

print("Validation 3: Symplectic Euler, dt=1e3, t=31580001")
# neptune
o = vec3(2789067153552.279, -3534979140221.3228, 8519379660.803269)
j = vec3(2788885248756.336, -3535125337454.775, 8526582469.79332)

percent_error = (o-j).mag()/j.mag() * 100
print("Neptune position error: ", percent_error, "%")
errors_3.append(percent_error)

# uranus
o = vec3(2428902457426.5913, -1744089213814.097, -37950323640.98611)
j = vec3(2428733974024.8896, -1744313590807.525, -37948974543.52105)

percent_error = (o-j).mag()/j.mag() * 100
print("Uranus position error: ", percent_error, "%")
errors_3.append(percent_error)

# saturn
o = vec3(406670432180.8586, 1291823190042.995, -38660359318.116394)
j = vec3(407089165759.04083, 1291700311281.2312, -38674884589.528984)

percent_error = (o-j).mag()/j.mag() * 100
print("Saturn position error: ", percent_error, "%")
errors_3.append(percent_error)

# jupiter
o = vec3(-142927048004.7651, 759468627922.8118, 48271937.768065)
j = vec3(-142366551703.1861, 759549407369.1082, 35393837.29743958)

percent_error = (o-j).mag()/j.mag() * 100
print("Jupiter position error: ", percent_error, "%")
errors_3.append(percent_error)

# mars
o = vec3(190738862203.2322, 94078329600.0746, -2692788855.3500624)
j = vec3(191170783785.0864, 93017918832.48232, -2725613710.134409)

percent_error = (o-j).mag()/j.mag() * 100
print("Mars position error: ", percent_error, "%")
errors_3.append(percent_error)

# earth
o = vec3(-27978933793.731216, 143625062145.75592, 11424827.530161917)
j = vec3(-26699407658.071312, 143866032238.2885, 11434931.332379581)

percent_error = (o-j).mag()/j.mag() * 100
print("Earth position error: ", percent_error, "%")
errors_3.append(percent_error)

# venus
o = vec3(6630698126.854786, -109404202868.80249, -1868077328.037723)
j = vec3(5079584881.556118, -109473191238.0248, -1779519318.029396)

percent_error = (o-j).mag()/j.mag() * 100
print("Venus position error: ", percent_error, "%")
errors_3.append(percent_error)

# mercury
o = vec3(52995719114.08836, -20143542799.92522, -6450002220.067493)
j = vec3(52693155692.55486, -22050074935.34043, -6578024568.097363)

percent_error = (o-j).mag()/j.mag() * 100
print("Mercury position error: ", percent_error, "%")
errors_3.append(percent_error)

plt.bar(["Neptune", "Uranus", "Saturn", "Jupiter", "Mars", "Earth", "Venus", "Mercury"], errors_1, label="Y4,dt=1e3", width=0.8)
plt.bar(["Neptune", "Uranus", "Saturn", "Jupiter", "Mars", "Earth", "Venus", "Mercury"], errors_2, label="Y4,dt=5e2", width=0.7)
plt.bar(["Neptune", "Uranus", "Saturn", "Jupiter", "Mars", "Earth", "Venus", "Mercury"], errors_3, label="SE,dt=1e3", width=0.6)

plt.xlabel("Bodies")
plt.ylabel("% Error")
plt.title("Position Error Compared to JPL Horizons System Data\nSimulated Time ~1 year")
plt.grid()
plt.legend()
plt.show()
