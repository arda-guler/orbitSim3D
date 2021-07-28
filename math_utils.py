import math

# takes cartezian coords list
# gives spherical coords list
def cartesian2spherical(cart):
    
    x = cart[0]
    y = cart[1]
    z = cart[2]
    
    rho = (x**2 + y**2 + z**2)**0.5
    theta = math.degrees(math.atan(((x**2 + y**2)**0.5)/z))
    phi = math.degrees(math.atan(y/x))
    
    return [rho, theta, phi]

# takes spherical coords list
# gives cartezian coords list
def spherical2cartesian(sph):

    rho = sph[0]
    theta = math.radians(sph[1])
    phi = math.radians(sph[2])
    
    x = math.cos(theta) * math.sin(phi) * rho
    y = math.sin(theta) * math.sin(phi) * rho
    z = math.cos(phi) * rho
    
    return [x, y, z]

# cross product
def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]
