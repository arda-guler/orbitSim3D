# JPL_SolarSystem.py
#
# Grabs state vectors for major Solar System planets (planet-moon system barycenters) and Sol
# Turns it into a scenario file solar_system.osf

import sys
import requests
import json
from datetime import datetime
from datetime import timedelta
import re

filenames = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Sol"]

headers = ["B|Mercury|data/models/minimercury.obj|330200000000000000000000|2440000|[0.87,0.80,0.77]|",
           "B|Venus|data/models/minivenus.obj|4868500000000000000000000|6051840|[1.0,0.93,0.69]|",
           "B|Earth|data/models/miniearth.obj|5972190000000000000000000|6371000|[0.04,0.15,0.85]|",
           "B|Mars|data/models/minimars.obj|641710000000000000000000|3389920|[0.91,0.31,0.23]|",
           "B|Jupiter|data/models/minijupiter.obj|1898187220000000000000000000|69911000|[0.90,0.79,0.72]|",
           "B|Saturn|data/models/minisaturn.obj|568340000000000000000000000|60268000|[0.97,0.89,0.84]|",
           "B|Uranus|data/models/miniuranus.obj|86813000000000000000000000|25362000|[0.60,0.76,0.71]|",
           "B|Neptune|data/models/minineptune.obj|102409000000000000000000000|24624000|[0.50,0.64,0.85]|",
           "B|Sol|data/models/minisol.obj|1988500000000000000000000000000|695700000|[1.0,0.94,0.12]|"]

footers = ["|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0",
           "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|3.9E26|0|0"]

total_text = ""

start_time = input("Ephemeris time: ")
dt_start_time = datetime.fromisoformat(start_time)
dt_stop_time = dt_start_time + timedelta(days=1)
stop_time = dt_stop_time.strftime("%Y-%m-%d")

for i in range(1, 10): # 1 to 10 for Mercury - Neptune and Sol (10)
    try:
        print("Requesting ephemeris for", filenames[i-1])
        bodyid = i

        url = "https://ssd.jpl.nasa.gov/api/horizons.api"

        url += "?format=text&EPHEM_TYPE=VECTORS&OBJ_DATA=NO&VEC_TABLE=2&CENTER='500@0'"
        url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'&STEP_SIZE='3d'".format(bodyid, start_time, stop_time)

        response = requests.get(url)

        if response.status_code == 200:
            #print(response.text)
            fname = filenames[i-1] + ".txt"

            useful_text = response.text.split("$$SOE")
            useful_text = useful_text[1]
            useful_text = useful_text.split("$$EOE")
            useful_text = useful_text[0]

            useful_text = useful_text.split("\n")[2] + useful_text.split("\n")[3]
            #useful_text = useful_text.split("=")
            useful_text = re.findall("-?[\d.]+(?:a-?\d+)?", useful_text)

            useful_text = eval(str(useful_text))
            print(useful_text)

            if filenames[i-1] == "Sol":
                useful_text[0] = float(useful_text[0])
                useful_text[2] = float(useful_text[2])
                useful_text[4] = float(useful_text[4])
                useful_text[1] = float(useful_text[1])
                useful_text[3] = float(useful_text[3])
                useful_text[5] = float(useful_text[5])

                useful_text[6] = float(useful_text[6])
                useful_text[8] = float(useful_text[8])
                useful_text[10] = float(useful_text[10])
                useful_text[7] = float(useful_text[7]) + 3
                useful_text[9] = float(useful_text[9]) + 3
                useful_text[11] = float(useful_text[11]) + 3
            else:
                useful_text[0] = float(useful_text[0])
                useful_text[2] = float(useful_text[2])
                useful_text[4] = float(useful_text[4])
                useful_text[1] = float(useful_text[1]) + 3
                useful_text[3] = float(useful_text[3]) + 3
                useful_text[5] = float(useful_text[5]) + 3

                useful_text[6] = float(useful_text[6])
                useful_text[8] = float(useful_text[8])
                useful_text[10] = float(useful_text[10])
                useful_text[7] = float(useful_text[7]) + 3
                useful_text[9] = float(useful_text[9]) + 3
                useful_text[11] = float(useful_text[11]) + 3

            print(useful_text)

            positions = [useful_text[0]*10**useful_text[1],
                         useful_text[2]*10**useful_text[3],
                         useful_text[4]*10**useful_text[5]]

            velocities = [useful_text[6]*10**useful_text[7],
                          useful_text[8]*10**useful_text[9],
                          useful_text[10]*10**useful_text[11]]
            
            print(positions)
            print(velocities)
            
            f = open(fname, "w")
            #f.write(str(actual_data))
            f.write(headers[i-1] + str(positions) + "|" + str(velocities) + footers[i-1])
            f.close()

            total_text += headers[i-1] + str(positions) + "|" + str(velocities) + footers[i-1] + "\n"

        elif response.status_code == 400:
            print("Error 400 Bad Request")

        elif response.status_code == 405:
            print("Error 400 Method Not Allowed")

        elif response.status_code == 500:
            print("Error 400 Internal Server Error")

        elif response.status_code == 503:
            print("Error 400 Server Unavailable")

    except:
        print(useful_text)
        
print("Done.")

f = open("solar_system.osf", "w")
f.write(total_text)
f.close()
print("")
print(total_text)
