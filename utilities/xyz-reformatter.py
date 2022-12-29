# Reformats JPL Horizons cartezian coordinates to OS3D visualization coordinates
# saves modified scenario as 'formatted.osf'

scn_file = open(input("Scenario filepath: "), "r")
scn_lines = scn_file.readlines()

result_text = ""
for line in scn_lines:
    result_line = ""
    if line.startswith("B"):
        print("Body")
        line = line[:-1].split("|")
        result_line += "B|"
        result_line += line[1] + "|" # name
        result_line += line[2] + "|" # model
        result_line += line[3] + "|" # mass
        result_line += line[4] + "|" # radius
        result_line += line[5] + "|" # color

        # line[6] is pos in meters
        line[6] = line[6][1:-1].split(",")
        result_line += "[" + line[6][1] + "," + line[6][2] + "," + line[6][0] + "]|"

        # line[7] is vel in meters per second
        line[7] = line[7][1:-1].split(",")
        result_line += "[" + line[7][1] + "," + line[7][2] + "," + line[7][0] + "]|"

        result_line += line[8] + "|" # orientation
        result_line += line[9] + "|"
        result_line += line[10] + "|"
        result_line += line[11] + "|"
        result_line += line[12] + "|"
        result_line += line[13]

    result_text += result_line + "\n"

output_file = open("formatted.osf", "w")
output_file.write(result_text)
scn_file.close()
output_file.close()
        
        

    
