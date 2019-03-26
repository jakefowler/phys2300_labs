from vpython import *
from math import sin, cos
import argparse
import math
import matplotlib.pyplot as plt



def set_scene(data):
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    
    # Set background: floor, table, etc
    box(pos=vector(500, 0, 0), size=vector(1100, 0.01, 100), color=color.green) # grass field
    box(pos=vector(500, 0, 0), size=vector(5, 0.02, 100), color=color.white) # middle line in field
    box(pos=vector(0, 0, 0), size=vector(5, 0.02, 100), color=color.white) # start line in field
    box(pos=vector(1000, 0, 0), size=vector(5, 0.02, 100), color=color.white) # end line in field
    box(pos=vector(250, 0, 0), size=vector(5, 0.02, 100), color=color.white) # 1/4 line in field
    box(pos=vector(750, 0, 0), size=vector(5, 0.02, 100), color=color.white) # 3/4 line in field


def calculate_y_coordinate(y_initial_velocity, time, gravity = 9.8):
    """
    Function to calculate the vertical projectile motion.
    Param: y_initial_velocity -> the velocity at the start
           time -> how long the projectile has been traveling
           gravity -> what is the acceleration of gravity in this environment? Defaults to -9.8. 
    Returns the calculation of the current velocity in the y direction.
    """
    return ((y_initial_velocity * time) - (0.5 * gravity * (time * time)))

def calculate_x_coordinate(x_velocity, time):
    """
    Function to calculate the horizontal projectile motion.
    Param: x_velocity -> velocity in the x direction
           time -> how long the projectile has been traveling 
    Returns the calculation of the current velocity in the x direction.
    """
    return x_velocity * time 

def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=data["ball_radius"], color=color.cyan, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Set initial velocity & position
    init_x_velocity = cos(math.radians(data['theta'])) * data['init_velocity']
    init_y_velocity = sin(math.radians(data['theta'])) * data['init_velocity']
    ball_nd.velocity = vector(init_x_velocity, init_y_velocity, 0)
    data["x_no_drag"] = [] # list to hold x coordinatates for graphing later
    data["y_no_drag"] = [] # list to hold y coordinatates for graphing later

    # Animate
    t = 0
    stopping_point = data["ball_radius"] + 0.12
    while t < 100:
        if(ball_nd.pos.y < stopping_point and ball_nd.pos.x > 1):
            break
        rate(1000)
        ball_nd.pos.x = calculate_x_coordinate(init_x_velocity, t)
        ball_nd.pos.y = calculate_y_coordinate(init_y_velocity, t)
        data["x_no_drag"].append(ball_nd.pos.x)
        data["y_no_drag"].append(ball_nd.pos.y)
        t = t + data['deltat']

def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=data["ball_radius"], color=color.red, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Set initial velocity & position
    init_x_velocity = cos(math.radians(data['theta'])) * data['init_velocity']
    init_y_velocity = sin(math.radians(data['theta'])) * data['init_velocity']
    ball_nd.velocity = vector(init_x_velocity, init_y_velocity, 0)
    data["x_with_drag"] = [] # list to hold x coordinatates for graphing later
    data["y_with_drag"] = [] # list to hold y coordinatates for graphing later

    # Animate
    g = vector(0, data["gravity"], 0) 
    t = 0
    stopping_point = data["ball_radius"] + 0.12 # keeps the ball from going through the floor
    while t < 100:
        if(ball_nd.pos.y < stopping_point and ball_nd.pos.x > 1):
            break
        rate(1000)
        net_force = data["ball_mass"] * g - (ball_nd.velocity * data["alpha"])
        ball_nd.velocity = ball_nd.velocity + (net_force/data["ball_mass"] * data['deltat'])
        ball_nd.pos = ball_nd.pos + ball_nd.velocity * data['deltat']
        data["x_with_drag"].append(ball_nd.pos.x)
        data["y_with_drag"].append(ball_nd.pos.y)

        t = t + data['deltat']

def plot_data(data):
    """
    Plot the drag vs no drag projectile motion graphs
    param:
        data: holds all the data on the projectile motion
    returns: 
        nothing
    """
    plt.title("Projectile Motion Drag vs No Drag")
    plt.xlabel("Distance in Meters")
    plt.ylabel("Height in Meters")
    plt.plot(data["x_no_drag"], data["y_no_drag"], label="No Drag")
    plt.plot(data["x_with_drag"], data["y_with_drag"], label="With Drag")
    plt.legend()
    plt.show()

def main():
    """
    Function that gets everything going
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Projectile Motion")

    parser.add_argument("--velocity", "-v", action="store", dest="velocity", type=float, required=True, help="velocity in m/s --velocity 20")
    parser.add_argument("--angle", "-a", action="store", dest="angle", type=float, required=True, help="angle in degrees --angle 45")
    parser.add_argument("--height", action="store", dest="height", type=float, required=False, default=1.2, help="height in meters --height 1.2")

    args = parser.parse_args()
    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['theta'] = 45 
    data['init_height'] = args.height   # y-axis
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees
    # Constants
    data['rho'] = 1.225  # kg/m^3 air density
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)

if __name__ == "__main__":
    main()
    exit(0)
