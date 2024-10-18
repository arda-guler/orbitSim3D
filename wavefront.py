class Wavefront3D:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load()

    def load(self):
        with open(self.file_path, "r") as f:
            self.vertices = []
            self.texture_coords = []
            self.normals = []
            self.faces = []
            
            lines = f.readlines()
            for line in lines:
                if line.startswith("v "):
                    line = line.strip().split()
                    v_x = float(line[1])
                    v_y = float(line[2])
                    v_z = float(line[3])
                    self.vertices.append([v_x, v_y, v_z])

                elif line.startswith("vt "):
                    line = line.strip().split()
                    u = float(line[1])
                    v = float(line[2])
                    self.texture_coords.append([u, v])

                elif line.startswith("vn "):
                    line = line.strip().split()
                    vn_x = float(line[1])
                    vn_y = float(line[2])
                    vn_z = float(line[3])
                    self.normals.append([vn_x, vn_y, vn_z])

                elif line.startswith("f "):
                    line = line.strip().split()
                    
                    line[1] = line[1].split("/")
                    v1 = int(line[1][0])
                    vt1 = int(line[1][1])
                    vn1 = int(line[1][2])
                    
                    line[2] = line[2].split("/")
                    v2 = int(line[2][0])
                    vt2 = int(line[2][1])
                    vn2 = int(line[2][2])
                    
                    line[3] = line[3].split("/")
                    v3 = int(line[3][0])
                    vt3 = int(line[3][1])
                    vn3 = int(line[3][2])
                    
                    self.faces.append([[v1,v2,v3],
                                       [vt1,vt2,vt3],
                                       [vn1,vn2,vn3]])
    
