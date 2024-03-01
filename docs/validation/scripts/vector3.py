class vec3:
    def __init__(self, x=0, y=0, z=0, *, lst=None):
        
        if lst:
            try:
                self.x = lst[0]
                self.y = lst[1]
                self.z = lst[2]
            except:
                print("ERROR: Incorrect list format for Vector3 initialization!")
            
        else:
            self.x = x
            self.y = y
            self.z = z

    def __getitem__(self, idx):
        if idx==0:
            return self.x
        elif idx==1:
            return self.y
        elif idx==2:
            return self.z
        else:
            raise IndexError

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, val):
        return vec3(self.x * val, self.y * val, self.z * val)

    def __truediv__(self, val):
        try:
            return vec3(self.x / val, self.y / val, self.z / val)
        except ZeroDivisionError:
            print("ERROR: Attempt to divide vector by zero!")
            return None

    def __neg__(self):
        return self * (-1)

    def __repr__(self):
        output = "Vector3(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
        return output

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**(0.5)

    def cross(self, other):
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalized(self):
        m = self.mag()
        if not m == 0:
            return vec3(self.x/m, self.y/m, self.z/m)
        else:
            return vec3(0,0,0)

    def tolist(self):
        return [self.x, self.y, self.z]

