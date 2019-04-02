import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 0.1     # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
framerate = 100
steps_per_frame = 10
x_coordinates = []
y_coordinates = []

def f(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta)
    return np.array([ftheta, fomega], float)


def main():
    """
    """
    # Set up initial values
    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])
    
    ball = sphere(pos=vector(x, y, 0), radius=R, color=color.red)
    arm = cylinder(pos=vector(0, 0, 0), axis=vector(x, y, 0), radius=W)
    ceiling = box(pos=vector(0, 0, 0), size=vector(0.05, 0.001, 0.05))

    # Loop over some time interval
    dt = 0.01
    t = 0
    while t < 100:
            rate(100)
            # Use the 4'th order Runga-Kutta approximation
            # #       for i in range(steps_per_frame):
            r += h*f(r)

            t += dt
            # Update positions
            x = l*np.sin(r[0])
            y = -l*np.cos(r[0])

            ball.pos = vector(x, y, 0)
            arm.axis = vector(x, y, 0)

            x_coordinates.append(x)
            y_coordinates.append(y)
                
            # Update the cylinder axis
            # Update the pendulum's bob

    plt.plot(x_coordinates, y_coordinates)
    plt.show()

if __name__ == "__main__":
    main()
   